import asyncio
import json

from libs.insta_auth import get_api
from libs.features import get_my_feed, process_data

class TCPclient(asyncio.Protocol):
    def __init__(self, loop, username, password):
        self.transport = None
        self.loop = loop
        self.queue = asyncio.Queue()
        self._ready = asyncio.Event()
        self.username = username
        self.password = password
        self.settings_file_path = "saved_auth.json"
        self.api = None
        asyncio.async(self._send_data())  # Or asyncio.ensure_future if using 3.4.3+

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()
    
    def connection_made(self, transport):
        """ Upon connection send the message to the server """
        self.transport = transport
        print("Connection made.")
        self.api = get_api(self.username, self.password, self.settings_file_path)
        self.password = None #you never know
        self._ready.set()

    def data_received(self, data):
        print('Message received: {!r}'.format(data.decode()))
        process_data(self.api, data.decode())

    @asyncio.coroutine
    def _send_data(self):
        """ Send messages to the server as they become available. """
        yield from self._ready.wait()
        print("Ready!")
        while True:
            pics = get_my_feed(self.api, self.username)
            if pics != None:
                self.transport.write(pics.encode('utf8'))
                print('Message sent: {!r}'.format(pics))
            yield from asyncio.sleep(10)