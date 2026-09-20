import asyncio
from typing import Set

from generated import max_bridge_pb2

class BroadcastManager:    
    def __init__(self):
        self.queues: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def add_subscriber(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        async with self._lock:
            self.queues.add(queue)
        return queue

    async def remove_subscriber(self, queue: asyncio.Queue):
        async with self._lock:
            self.queues.discard(queue)

    async def broadcast(self, message: max_bridge_pb2.Message):
        dead = []
        async with self._lock:
            for q in self.queues:
                try:
                    q.put_nowait(message)
                except asyncio.QueueFull:
                    dead.append(q)
            for q in dead:
                self.queues.discard(q)
