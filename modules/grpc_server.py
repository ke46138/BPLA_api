import asyncio
import logging
from concurrent import futures
from typing import AsyncIterator

import grpc

from generated import max_bridge_pb2, max_bridge_pb2_grpc
from modules.broadcast_manager import BroadcastManager

from config import GRPC_HOST, GRPC_PORT


class GrpcAPIServicer(max_bridge_pb2_grpc.MaxBridgeServicer):
    def __init__(self, broadcast_manager: BroadcastManager):
        self.broadcast_manager = broadcast_manager
        self.logger = logging.getLogger("grpc-servicer")

    async def Subscribe(
        self,
        request,
        context: grpc.ServicerContext
    ) -> AsyncIterator[max_bridge_pb2.Message]:
        queue = await self.broadcast_manager.add_subscriber()

        try:
            while True:
                try:
                    msg = await asyncio.wait_for(queue.get(), timeout=1.0)
                    yield msg
                except asyncio.TimeoutError:
                    continue
        except Exception:
            self.logger.exception(f"Ошибка стриминга")
        finally:
            await self.broadcast_manager.remove_subscriber(queue)


class GrpcAPIServer:
    def __init__(self, broadcast_manager: BroadcastManager):
        self.broadcast_manager = broadcast_manager
        self.grpc_server = None
        self.logger = logging.getLogger("grpc-service")

    async def start(self):
        self.grpc_server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=10)
        )
        max_bridge_pb2_grpc.add_MaxBridgeServicer_to_server(
            GrpcAPIServicer(self.broadcast_manager), self.grpc_server
        )
        self.grpc_server.add_insecure_port(f"{GRPC_HOST}:{GRPC_PORT}")
        await self.grpc_server.start()
        self.logger.info(f"gRPC сервер запущен на {GRPC_HOST}:{GRPC_PORT}")

    async def stop(self):
        if self.grpc_server:
            await self.grpc_server.stop(5)
