from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from .exchange_functions import write_to_file
from classes.logger import Logger


router = Router()
logger = Logger()


@router.message(Command(commands=["get_exchange_rate"]))
async def exchange_command(message: Message, state: FSMContext):
    file = write_to_file()
    if not file:
        logger.critical("File was not found")
    await message.answer_document(FSInputFile(file))
