import aio_pika
import asyncio
import json
import uuid
from .disp import disp
from types import FunctionType
from .async_util import call


class AsyncClient:
    event_loop = None
    connection = None
    url = None
    queues = {}
    channels = {}
    exchanges = {}
    verbose = False
    correlation_id = uuid.uuid4()

    def __init__(self, event_loop=None, verbose: bool = False):
        if event_loop is None:
            self.event_loop = asyncio.get_event_loop()
        else:
            self.event_loop = event_loop
        self.verbose = verbose

    # General tasks

    async def connect(self, host: str = "localhost", username: str = "guest", password: str = "guest",
                      protocol: str = "amqp", custom_url: str = None):
        if custom_url is None:
            self.url = f"{protocol}://{username}:{password}@{host}/"
        else:
            self.url = custom_url

        disp(f"Connecting to {host} as {username}", do_print=self.verbose)
        self.connection = await aio_pika.connect(self.url, loop=self.event_loop)
        return self.connection

    async def register_channel(self, channel_number: int = None):
        if channel_number in self.channels.keys():
            raise ValueError(f"Channel number \"{channel_number}\" is has already been registered!")
        channel = await self.connection.channel(channel_number=channel_number)
        self.channels.update({channel_number: channel})

        if channel_number is None:
            report = "Registering default channel"
        else:
            report = f"Registered channel number {channel_number}"

        disp(report, do_print=self.verbose)
        return await self.get_channel(channel_number=channel_number)

    async def get_channel(self, channel_number: int = None):
        if channel_number is None:
            return await self.connection.channel()
        else:
            return self.channels[channel_number]

    async def register_queue(self, routing_key: str, channel_number: int = None):
        if channel_number not in self.channels.keys():
            channel = await self.register_channel(channel_number=channel_number)
        else:
            channel = await self.get_channel(channel_number)
        queue = await channel.declare_queue(routing_key)
        self.queues.update({routing_key: queue})

        disp(f"Registered queue \"{routing_key}\"")
        return await self.get_queue(routing_key)

    async def get_queue(self, routing_key: str):
        return self.queues[routing_key]

    async def register_exchange(self, exchange_name: str, channel_number: int = None, auto_delete: bool = True):
        channel = await self.get_channel(channel_number=channel_number)
        exchange = channel.declare_exchange(exchange_name, auto_delete=auto_delete)
        self.exchanges.update({exchange_name: exchange})

        disp(f"Registered exchange \"{exchange_name}\"")
        return await self.get_exchange(exchange_name)

    async def get_exchange(self, exchange_name: str):
        return self.exchanges[exchange_name]

    def run_loop(self):
        disp("Running event loop. Ctrl+C to exit")
        self.event_loop.run_forever()

    # Sender tasks

    async def send_bytes(self, message: bytes, routing_key: str, channel_number: int = None, exchange_name: str = None,
                         reply: dict = None):
        channel = await self.get_channel(channel_number=channel_number)

        exchange = channel.default_exchange if exchange_name is None else await self.get_exchange(exchange_name)
        sent = message if len(message) <= 100 else "<Too large to display>"

        if reply is not None:
            reply_key = reply["routing_key"]
            reply_callback = reply["callback"]
            corr_id = self.correlation_id
            await self.create_listener(reply_key, reply_callback, auto_ack=True, channel_number=channel_number)
        else:
            reply_key = None
            corr_id = None

        disp(f"Sending message: \"{sent}\"", do_print=self.verbose)
        message = aio_pika.Message(body=message, reply_to=reply_key, correlation_id=corr_id)
        await exchange.publish(message, routing_key=routing_key)

    async def send_json(self, message: dict, routing_key: str, channel_number: int = None, exchange_name: str = None,
                        encoding="utf-8", reply: dict = None):
        disp("Converting dict to JSON string...", do_print=self.verbose)
        s_message = json.dumps(message)
        await self.send_string(s_message, routing_key, channel_number=channel_number, exchange_name=exchange_name,
                               encoding=encoding, reply=reply)

    async def send_string(self, message: str, routing_key: str, channel_number: int = None, exchange_name: str = None,
                          encoding="utf-8", reply: dict = None):
        disp(f"Encoding string to bytes message with {encoding}")
        b_message = message.encode(encoding)
        await self.send_bytes(b_message, routing_key, channel_number=channel_number, exchange_name=exchange_name,
                              reply=reply)

    # Receiver tasks

    async def create_listener(self, routing_key: str, callback: FunctionType, auto_ack: bool = True,
                              channel_number: int = None):
        if routing_key not in self.queues.keys():
            queue = await self.register_queue(routing_key, channel_number=channel_number)
        else:
            queue = await self.get_queue(routing_key)
        cc = _CallbackClass(callback)
        await queue.consume(cc.callback_function, no_ack=not auto_ack)


class _CallbackClass:
    func = None

    def __init__(self, func):
        self.func = func

    async def callback_function(self, message: aio_pika.IncomingMessage):
        await call(self.func, message)


# Utility functions

def get_json(message: aio_pika.IncomingMessage, encoding="utf-8"):
    string = get_string(message, encoding=encoding)
    return json.loads(string)


def get_string(message: aio_pika.IncomingMessage, encoding="utf-8"):
    return message.body.decode(encoding)


def reply_args(routing_key, callback):
    return {
        "routing_key": routing_key,
        "callback": callback
    }
