from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import BotCommand
from Instruments.Config import (bot, get_translation as gt,
                                get_language as gl, set_language as sl, States)
from Instruments.CGM import languages, menu
from Instruments.DB import add_new_user as anu, language_set as ls

rl = Router()


@rl.message(Command(commands=["start", "instructions"]))
async def commands_handler(message, state):
    user_id = message.from_user.id

    if message.text == "/start":
        chat_id = message.chat.id
        await anu(user_id)
        await languages(chat_id, state)

    elif message.text == "/instructions":
        lc = await gl(user_id)
        await message.answer(await gt(lc, 'Commands', 'instructions_info'))


@rl.callback_query(States.languages)
async def language_handler(callback, state):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    lc = callback.data
    await sl(user_id, lc)
    await callback.message.delete()
    await callback.answer(await gt(lc, 'Languages', 'language_chosen'), show_alert=True)
    await set_commands(lc)
    await menu(lc, chat_id, state)
    await ls(user_id, lc)


async def set_commands(lc):
    commands = [
        BotCommand(command="/start", description=await gt(lc, 'Commands', 'start')),
        BotCommand(command="/instructions", description=await gt(lc, 'Commands', 'instructions'))
    ]
    await bot.set_my_commands(commands)
