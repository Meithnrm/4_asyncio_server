import asyncio
import logging
import sys

SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


async def echo_client(address):
    log = logging.getLogger('echo_client')

    log.debug('connecting to {} port {}'.format(*address))
    reader, writer = await asyncio.open_connection(*address)
    await writer.drain()
    log.debug('waiting for response')
    while True:
        msg = input()
        if msg.lower() != 'exit' and msg != "":
            writer.write(msg.encode())
            await writer.drain()
            data = await reader.read(128)
            if data:
                log.debug('received {}'.format(data))
            else:
                log.debug('closing')
                writer.close()
                return
        else:
            log.debug('closing')
            writer.close()
            return

try:
    event_loop.run_until_complete(
        echo_client(SERVER_ADDRESS)
    )
finally:
    log.debug('closing event loop')
    event_loop.close()