import asyncio
import logging

from modules.broadcast_manager import BroadcastManager
from modules.grpc_server import GrpcAPIServer
from modules.max_client import MaxClient

logger = logging.getLogger("max-bridge")

async def main():
    broadcast_manager = BroadcastManager()
    server = GrpcAPIServer(broadcast_manager)
    max_client = MaxClient(broadcast_manager)
    try:
        await server.start()
        await max_client.start()
    except asyncio.CancelledError:
        logger.info("Завершение работы...")
    finally:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())
