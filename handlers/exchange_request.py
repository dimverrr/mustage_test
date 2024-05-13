from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from .exchange_processing import write_to_file

router = Router()


@router.message(Command(commands=["get_exchange_rate"]))
async def exchange_comman(message: Message, state: FSMContext):
    file = write_to_file()
    if not file:
        pass
    await message.answer_document(FSInputFile(file))
