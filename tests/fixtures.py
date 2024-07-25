import asyncio
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from rabbitmq_clients import RabbitConsumer, RabbitProducer


env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture
def rabbit_host() -> str:
    return os.getenv('RABBIT_HOST')


@pytest.fixture
def rabbit_user() -> str:
    return os.getenv('RABBIT_USER')


@pytest.fixture
def rabbit_password() -> str:
    return os.getenv('RABBIT_PASSWORD')


@pytest.fixture
def producer(
    rabbit_user: str,
    rabbit_password: str,
    rabbit_host: str,
) -> RabbitProducer:
    return RabbitProducer(
        login=rabbit_user,
        password=rabbit_password,
        host=rabbit_host,
    )


@pytest.fixture
def consumer(
    rabbit_user: str,
    rabbit_password: str,
    rabbit_host: str,
) -> RabbitConsumer:
    return RabbitConsumer(
        login=rabbit_user,
        password=rabbit_password,
        host=rabbit_host,
    )


@pytest.fixture
def dataset() -> dict:
    return {"result": True}


@pytest.fixture
def queue_name() -> str:
    return 'test_queue'
