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
        self.websocket = None
        self.streamer_info = None
        self.start_timestamp = None
        self.terminal = MultiTerminal(title="Stream Output")
        self.color_print = ColorPrint()
        self.active = False
        self.request_id = 0
        self.client = client

    async def start(self):
        response = self.client.get_user_preferences()
        if not response:
            self.color_print.print("error", f"Failed to get streamer info: {response.text}")
            exit(1)
        self.streamer_info = response['streamerInfo'][0]
        login = self._construct_login_message()
        self.color_print.print("info", "Starting stream...")
        self.color_print.print("info", f"Streamer info: {self.streamer_info}")
        self.color_print.print("info", f"Login message: {login}")
        while True:
            try:
                await self._connect_and_stream(login)
            except websockets.exceptions.ConnectionClosedOK:
                self.color_print.print("info", "Stream has closed.")
                break
            except Exception as e:
                self.color_print.print("error", f"{e}")
                self._handle_stream_error(e)
                
    def _construct_login_message(self):
        self.request_id += 1
        return basic_request("ADMIN", "LOGIN", self.request_id, {
            "Authorization": self.client.token_info.get("access_token"),
            "SchwabClientChannel": self.streamer_info.get("schwabClientChannel"),
            "SchwabClientFunctionId": self.streamer_info.get("schwabClientFunctionId"),
            "SchwabClientCustomerId": self.streamer_info.get("schwabClientCustomerId"),
            "SchwabClientCorrelId": self.streamer_info.get("schwabClientCorrelId")
        })

    async def _connect_and_stream(self, login):
        self.start_timestamp = datetime.now()
        self.color_print.print("info", "Connecting to server...")
        self.color_print.print("info", f"Start timestamp: {self.start_timestamp}")
        self.color_print.print("info", f"Streamer socket URL: {self.streamer_info.get('streamerSocketUrl')}")
        async with websockets.connect(self.streamer_info.get('streamerSocketUrl'),
                                      ping_interval=None) as self.websocket:
            self.terminal.print("[INFO]: Connecting to server...")
            await self.websocket.send(json.dumps(login))
            self.terminal.print(f"[Login]: {await self.websocket.recv()}")
            self.active = True
            while True:
                received = await self.websocket.recv()
                self.terminal.print(received)

    def _handle_stream_error(self, error):
        self.active = False
        if isinstance(error, RuntimeError) and str(error) == "Streaming window has been closed":
            self.color_print.print("warning", "Streaming window has been closed.")
        else:
            if (datetime.now() - self.start_timestamp).seconds < 70:
                self.color_print.print("error", "Stream not alive for more than 1 minute, exiting...")
            else:
                self.terminal.print("[WARNING]: Connection lost to server, reconnecting...")

    async def send(self, listOfRequests):

        if not isinstance(listOfRequests, list):
            listOfRequests = [listOfRequests]
        if self.active:
            to_send = json.dumps({"requests": listOfRequests})
            await self.websocket.send(to_send)
        else:
            self.color_print.print("warning", "Stream is not active, nothing sent.")

    def stop(self):
        self.send(basic_request("ADMIN", "LOGOUT", self.request_id))
        self.active = False
