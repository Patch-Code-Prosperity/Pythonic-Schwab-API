"""
StreamClient module for handling WebSocket connections to a streaming API.

This module provides the StreamClient class which manages the connection,
sending, and receiving of messages through a WebSocket. It also handles
reconnection logic and error handling.
"""

import json
import asyncio
from datetime import datetime
import sys
import websockets
from pythonic_schwab_api.multi_terminal import MultiTerminal
from pythonic_schwab_api.api_client import APIClient
from pythonic_schwab_api.stream_utilities import basic_request
from pythonic_schwab_api.color_print import ColorPrint


class StreamClient:
    """
    StreamClient class to manage WebSocket connections and message handling.

    Attributes:
        client (APIClient): The API client instance for making requests.
        websocket (WebSocket): The WebSocket connection instance.
        streamer_info (dict): Information about the streamer.
        start_timestamp (datetime): Timestamp when the stream started.
        terminal (MultiTerminal): Terminal instance for output.
        color_print (ColorPrint): Instance for colored printing.
        active (bool): Indicates if the connection is active.
        login_successful (bool): Indicates if login was successful.
        request_id (int): ID for tracking requests.
    """

    def __init__(self, client: APIClient):
        """
        Initialize the StreamClient with an API client.

        Args:
            client (APIClient): The API client instance.
        """
        self.client = client
        self.websocket = None
        self.streamer_info = None
        self.start_timestamp = None
        self.terminal = MultiTerminal(title="Stream Output")
        self.color_print = ColorPrint()
        self.active = False
        self.login_successful = False
        self.request_id = -1

    async def start(self):
        """
        Start the streaming client by getting user preferences and connecting
        to the WebSocket.
        """
        response = self.client.get_user_preferences()
        if 'error' in response:  # Assuming error handling is done inside get_user_preferences
            self.color_print.print("error", f"Failed to get streamer info: {response['error']}")
            sys.exit(1)
        self.streamer_info = response['streamerInfo'][0]
        login = self._construct_login_message()
        await self.connect()
        await self.send(login)

    async def connect(self):
        """
        Establish a WebSocket connection using the streamer info.
        """
        try:
            self.websocket = await websockets.connect(self.streamer_info.get('streamerSocketUrl'))
            self.active = True
            self.color_print.print("info", "Connection established.")
        except websockets.exceptions.InvalidURI as e:
            self.color_print.print("error", f"Invalid WebSocket URI: {e}")
        except websockets.exceptions.InvalidHandshake as e:
            self.color_print.print("error", f"Invalid WebSocket handshake: {e}")
        except Exception as e:
            self.color_print.print("error", f"Failed to connect: {e}")

    async def send(self, message):
        """
        Send a message through the WebSocket connection.

        Args:
            message (dict): The message to be sent.
        """
        if not self.active:
            await self.connect()
        try:
            await self.websocket.send(json.dumps(message))
            self.color_print.print("info", f"Message sent: {json.dumps(message)}")
            response = await self.websocket.recv()
            await self.handle_response(response)
        except websockets.exceptions.ConnectionClosed as e:
            self.color_print.print("error", f"Connection closed: {e}")
        except json.JSONDecodeError as e:
            self.color_print.print("error", f"JSON decode error: {e}")
        except Exception as e:
            self.color_print.print("error", f"Failed to send message: {e}")

    async def handle_response(self, message):
        """
        Handle the response received from the WebSocket.

        Args:
            message (str): The message received from the WebSocket.
        """
        message = json.loads(message)
        self.color_print.print("info", f"Received: {message}")
        if "Login" in message.get('command', '') and message.get('content', {}).get('code') == 0:
            self.login_successful = True
            self.color_print.print("info", "Login successful.")

    async def receive(self):
        """
        Receive a message from the WebSocket.

        Returns:
            str: The message received from the WebSocket.
        """
        try:
            return await self.websocket.recv()
        except websockets.exceptions.ConnectionClosed as e:
            self.color_print.print("error", f"Connection closed: {e}")
            return None
        except Exception as e:
            self.color_print.print("error", f"Error receiving message: {e}")
            return None

    def _construct_login_message(self):
        """
        Construct the login message for the WebSocket connection.

        Returns:
            dict: The constructed login message.
        """
        # Increment request ID for each new request
        self.request_id += 1

        # Prepare the parameters dictionary specifically for the parameters that need to be nested under 'parameters'
        parameters = {
            "Authorization": self.client.token_info.get("access_token"),
            "SchwabClientChannel": self.streamer_info.get("schwabClientChannel"),
            "SchwabClientFunctionId": self.streamer_info.get("schwabClientFunctionId")
        }

        # Call the basic_request function with customer ID and correlation ID at the top level of the request
        return basic_request(
            service="ADMIN",
            request_id=self.request_id,
            command="LOGIN",
            customer_id=self.streamer_info.get("schwabClientCustomerId"),
            correl_id=self.streamer_info.get("schwabClientCorrelId"),
            parameters=parameters
        )

    async def _connect_and_stream(self, login):
        """
        Connect to the WebSocket and start streaming messages.

        Args:
            login (dict): The login message to be sent.
        """
        try:
            async with websockets.connect(self.streamer_info.get('streamerSocketUrl')) as websocket:
                self.websocket = websocket
                await websocket.send(json.dumps(login))
                while True:
                    message = await websocket.recv()
                    await self.handle_message(json.loads(message))
        except websockets.exceptions.ConnectionClosedOK:
            self.color_print.print("info", "Stream has closed.")
        except websockets.exceptions.ConnectionClosedError as e:
            self.color_print.print("error", f"Connection closed with error: {e}")
        except json.JSONDecodeError as e:
            self.color_print.print("error", f"JSON decode error: {e}")
        except Exception as e:
            self.color_print.print("error", f"{e}")
            self._handle_stream_error(e)

    async def handle_message(self, message):
        """
        Handle a message received from the WebSocket.

        Args:
            message (dict): The message received from the WebSocket.
        """
        if "response" in message and any(
                resp.get("code") == "0" for resp in message["response"]):  # Check if login is successful
            self.color_print.print("info", "Logged in successfully, sending subscription requests...")
        else:
            self.color_print.print("info", f"Received: {message}")

    async def reconnect(self):
        """
        Attempt to reconnect to the WebSocket after a disconnection.

        Returns:
            bool: True if reconnection was successful, False otherwise.
        """
        self.terminal.print("[INFO]: Attempting to reconnect...")
        try:
            await asyncio.sleep(10)  # Wait before attempting to reconnect
            login = self._construct_login_message()  # Reconstruct login info
            await self._connect_and_stream(login)  # Attempt to reconnect
            return True
        except Exception as e:
            self.terminal.print(f"Reconnect failed: {e}")
            return False

    def _handle_stream_error(self, error):
        """
        Handle errors that occur during streaming.

        Args:
            error (Exception): The error that occurred.
        """
        self.active = False
        if isinstance(error, RuntimeError) and str(error) == "Streaming window has been closed":
            self.color_print.print("warning", "Streaming window has been closed.")
        else:
            if (datetime.now() - self.start_timestamp).seconds < 70:
                self.color_print.print("error", "Stream not alive for more than 1 minute, exiting...")
            else:
                self.terminal.print("[WARNING]: Connection lost to server, reconnecting...")

    def stop(self):
        """
        Stop the streaming client by closing the WebSocket connection.
        """
        if self.active:
            self.active = False
            asyncio.create_task(self.websocket.close())
            self.color_print.print("info", "Connection closed.")
