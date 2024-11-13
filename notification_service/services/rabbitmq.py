from __future__ import annotations
from typing import TYPE_CHECKING
import json
from enum import Enum
import ast
import asyncio

import aio_pika

from utils.email_utils import (
    send_welcome_new_user_email,
    send_reset_password_token_email,
)
from core.config import settings


if TYPE_CHECKING:
    from aio_pika import Connection, Channel, Exchange, Queue
    from aio_pika.abc import (
        AbstractIncomingMessage,
        AbstractRobustConnection,
    )


class UserActivityExchange(Enum):
    EXCHANGE_NAME = 'user-reporting'
    REGISTRATION_ACTIVITY_ROUTING_KEY = 'user-reporting.v1.registered'
    EDITING_INFO_ACTIVITY_ROUTING_KEY = 'user-reporting.v1.edited'
    DELETING_ACTIVITY_ROUTING_KEY = 'user-reporting.v1.deleted'
    PASSWORD_RESET_ACTIVITY_ROUTING_KEY = 'user-reporting.v1.password_reset'


async def send_welcome_new_user_email_callback(
    message: AbstractIncomingMessage,
) -> None:
    async with message.process():
        message = ast.literal_eval(message.body.decode())
        await send_welcome_new_user_email(message)


async def send_reset_password_token_email_callback(
    message: AbstractIncomingMessage,
) -> None:
    async with message.process():
        message = ast.literal_eval(message.body.decode())
        await send_reset_password_token_email(message)


async def get_rabbitmq_connection(
    username: str = settings.rabbitmq_username,
    password: str = settings.rabbitmq_password,
    host: str = settings.rabbitmq_host,
    port: int = settings.rabbitmq_port
) -> AbstractRobustConnection:
    connection: Connection = await aio_pika.connect_robust(
        host=host,
        port=port,
        login=username,
        password=password,
    )
    return connection


async def setup() -> None:
    connection = await get_rabbitmq_connection()
    channel: Channel = await connection.channel()

    await channel.set_qos(prefetch_count=5)

    _: Exchange = await channel.declare_exchange(
        UserActivityExchange.EXCHANGE_NAME.value,
        type=aio_pika.ExchangeType.DIRECT,
    )

    # User registered queue
    user_registered_queue: Queue = await channel.declare_queue(
        name=UserActivityExchange.REGISTRATION_ACTIVITY_ROUTING_KEY.value,
        durable=True
    )

    await user_registered_queue.bind(
        exchange=UserActivityExchange.EXCHANGE_NAME.value,
        routing_key=UserActivityExchange.REGISTRATION_ACTIVITY_ROUTING_KEY.value
    )

    await user_registered_queue.consume(
        send_welcome_new_user_email_callback
    )

    # User reset password queue
    user_password_reset_queue: Queue = await channel.declare_queue(
        name=UserActivityExchange.PASSWORD_RESET_ACTIVITY_ROUTING_KEY.value,
        durable=True
    )

    await user_password_reset_queue.bind(
        exchange=UserActivityExchange.EXCHANGE_NAME.value,
        routing_key=UserActivityExchange.PASSWORD_RESET_ACTIVITY_ROUTING_KEY.value
    )

    await user_password_reset_queue.consume(
        send_reset_password_token_email_callback
    )

    try:
        await asyncio.Future()
    finally:
        await channel.close()
        await connection.close()


async def send_message_using_routing_key(
    exchange_name: str,
    routing_key: str,
    message: dict,
):
    connection = await get_rabbitmq_connection()

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            exchange_name, type=aio_pika.ExchangeType.DIRECT,
        )
        message = aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await exchange.publish(message, routing_key=routing_key)

        channel.close()
        connection.close()
