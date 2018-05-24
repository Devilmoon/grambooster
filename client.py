import asyncio
import json

class SubscriberClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.transport = None
        self.loop = loop
        self.queue = asyncio.Queue()
        self._ready = asyncio.Event()
        asyncio.async(self._send_messages())  # Or asyncio.ensure_future if using 3.4.3+

    @asyncio.coroutine
    def _send_messages(self):
        """ Send messages to the server as they become available. """
        yield from self._ready.wait()
        print("Ready!")
        while True:
            data = yield from self.queue.get()
            self.transport.write(data.encode('utf-8'))
            print('Message sent: {!r}'.format(message))

    def connection_made(self, transport):
        """ Upon connection send the message to the
        server

        A message has to have the following items:
            type:       subscribe/unsubscribe
            channel:    the name of the channel
        """
        self.transport = transport
        print("Connection made.")
        self._ready.set()

    @asyncio.coroutine
    def send_message(self, data):
        """ Feed a message to the sender coroutine. """
        yield from self.queue.put(data)

    def data_received(self, data):
        """ After sending a message we expect a reply
        back from the server

        The return message consist of three fields:
            type:           subscribe/unsubscribe
            channel:        the name of the channel
            channel_count:  the amount of channels subscribed to
        """
        print('Message received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

@asyncio.coroutine
def feed_messages(protocol):
    """ An example function that sends the same message repeatedly. """

    mex = 1
    while True:
        yield from protocol.send_message(message)
        yield from asyncio.sleep(1)

if __name__ == '__main__':
    message = "soka"

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: SubscriberClientProtocol(loop),
                                  '127.0.0.1', 3338)
    _, proto = loop.run_until_complete(coro)
    asyncio.async(feed_messages(proto))  # Or asyncio.ensure_future if using 3.4.3+
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()
