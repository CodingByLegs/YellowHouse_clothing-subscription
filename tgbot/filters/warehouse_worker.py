import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class warehouseWorkerFilter(BoundFilter):
    key = 'is_wh_worker'

    def __init__(self, is_wh_worker: typing.Optional[bool] = None):
        self.is_wh_worker = is_wh_worker

    async def check(self, obj):
        if self.is_wh_worker is None:
            return False
        config: Config = obj.bot.get('config')
        return (obj.from_user.id in config.tg_bot.warehouse_workers) == self.is_wh_worker

