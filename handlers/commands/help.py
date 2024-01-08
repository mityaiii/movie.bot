from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from handlers.loader import command_descriptions

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = "\n".join([f"{command.command} - {command.description}" for command in command_descriptions])

    help_text = f"""commands:
{help_text}
"""

    await message.answer(help_text)
