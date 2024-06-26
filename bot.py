import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import common, exchange_request
from config_reader import config
from handlers.exchange_functions import schedule_exchange_retrieve_request
from classes.logger import Logger

logger = Logger()

async def main():

    logger.basic_config()

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(common.router, exchange_request.router)
    asyncio.create_task(schedule_exchange_retrieve_request())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
