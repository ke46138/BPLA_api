import logging

from pymax import WebClient, Message as MaxMessage

from generated import max_bridge_pb2
from modules.broadcast_manager import BroadcastManager
from config import MAX_CHANNEL_IDs

class MaxClient:
    def __init__(self, broadcast_manager: BroadcastManager):
        # WebClient, так как Client не хочет отсылать код при входе
        self.max_client = WebClient(
            work_dir="cache",
            session_name="main.db",
        )
        self.broadcast_manager = broadcast_manager
        self.logger = logging.getLogger("max-service")

        @self.max_client.on_message()
        async def on_message(message: MaxMessage, client: WebClient):
            """Хандлер сообщений из MAX"""
            channel_id = message.chat_id

            if not channel_id:
                self.logger.warning("chat_id отсутствует")

            if channel_id not in MAX_CHANNEL_IDs:
                return

            pb_message = max_bridge_pb2.Message( # type: ignore
                id=str(getattr(message, 'id', '')),
                text=str(getattr(message, 'text', ''))
            )

            await self.broadcast_manager.broadcast(pb_message)

    async def start(self):
        await self.max_client.start()
