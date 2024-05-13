from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Choose what you want to do: "
        "Create workout (/workout) or calculate body mass index (BMI) (/bmi).",
        reply_markup=ReplyKeyboardRemove(),
    )
