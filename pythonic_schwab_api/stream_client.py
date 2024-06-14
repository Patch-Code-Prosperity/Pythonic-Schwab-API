import json
import asyncio
import threading
import websockets
from datetime import datetime, time
from multi_terminal import MultiTerminal
from api_client import APIClient
from stream_utilities import basic_request  # Importing utility functions
from color_print import ColorPrint


class StreamClient:
    def __init__(self, client: APIClient):
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
        response = self.client.get_user_preferences()
        if 'error' in response:  # Assuming error handling is done inside get_user_preferences
            self.color_print.print("error", f"Failed to get streamer info: {response['error']}")
            exit(1)
        self.streamer_info = response['streamerInfo'][0]
        login = self._construct_login_message()
        await self.connect()
        await self.send(login)

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.streamer_info.get('streamerSocketUrl'))
            self.active = True
            self.color_print.print("info", "Connection established.")
        except Exception as e:
            self.color_print.print("error", f"Failed to connect: {e}")

    async def send(self, message):
        if not self.active:
            await self.connect()
        try:
            await self.websocket.send(json.dumps(message))
            self.color_print.print("info", f"Message sent: {json.dumps(message)}")
            response = await self.websocket.recv()
            await self.handle_response(response)
        except Exception as e:
            self.color_print.print("error", f"Failed to send message: {e}")

    async def handle_response(self, message):
        message = json.loads(message)
        self.color_print.print("info", f"Received: {message}")
        if "Login" in message.get('command', '') and message.get('content', {}).get('code') == 0:
            self.login_successful = True
            self.color_print.print("info", "Login successful.")

    async def receive(self):
        try:
            return await self.websocket.recv()
        except Exception as e:
            self.color_print.print("error", f"Error receiving message: {e}")
            return None

    def _construct_login_message(self):
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
        try:
            async with websockets.connect(self.streamer_info.get('streamerSocketUrl')) as websocket:
                self.websocket = websocket
                await websocket.send(json.dumps(login))
                while True:
                    message = await websocket.recv()
                    await self.handle_message(json.loads(message))
        except websockets.exceptions.ConnectionClosedOK:
            self.color_print.print("info", "Stream has closed.")
        except Exception as e:
            self.color_print.print("error", f"{e}")
            self._handle_stream_error(e)

    async def handle_message(self, message):
        if "response" in message and any(
                resp.get("code") == "0" for resp in message["response"]):  # Check if login is successful
            self.color_print.print("info", "Logged in successfully, sending subscription requests...")
        else:
            self.color_print.print("info", f"Received: {message}")

    async def reconnect(self):
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
        self.active = False
        if isinstance(error, RuntimeError) and str(error) == "Streaming window has been closed":
            self.color_print.print("warning", "Streaming window has been closed.")
        else:
            if (datetime.now() - self.start_timestamp).seconds < 70:
                self.color_print.print("error", "Stream not alive for more than 1 minute, exiting...")
            else:
                self.terminal.print("[WARNING]: Connection lost to server, reconnecting...")

    def stop(self):
        if self.active:
            self.active = False
            asyncio.create_task(self.websocket.close())
            self.color_print.print("info", "Connection closed.")
