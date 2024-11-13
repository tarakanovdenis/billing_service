import asyncio

from core.config import settings
from services import rabbitmq


if __name__ == '__main__':
    asyncio.run(rabbitmq.setup())
