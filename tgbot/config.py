from dataclasses import dataclass
from typing import List

from aiogram.types import Message
from environs import Env


@dataclass
class API_data:
    ip: str
    port: str
    protocol: str
    url: str


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    warehouse_workers: List[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    api: API_data
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            warehouse_workers=list(map(int, env.list("WAREHOUSE_WORKER"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        api=API_data(
            ip=env.str('API_IP'),
            port=env.str('API_PORT'),
            protocol=env.str('API_PROTOCOL'),
            url=env.str('API_PROTOCOL') + env.str('API_IP') + ":" + env.str('API_PORT'),
        ),
        misc=Miscellaneous()
    )