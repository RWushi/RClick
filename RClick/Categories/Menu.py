from aiogram import Router, F
from Instruments.Config import States, get_translation as gt, get_language as gl
from Instruments.Keyboards import rtools_kb
from Instruments.CGM import account_type, about, account, settings

rm = Router()


@rm.message(F.text, States.menu)
async def menu_handler(message, state, digit_check=False):
    user_id = message.from_user.id
    chat_id = message.chat.id
    lc = await gl(user_id)

    if message.text == await gt(lc, 'Menu', 'play'):
        await account_type(lc, chat_id, state)

    elif message.text == await gt(lc, 'Menu', 'about_bot'):
        await about(lc, chat_id, state)

    elif message.text == await gt(lc, 'Menu', 'account'):
        await account(lc, chat_id, state)

    elif message.text == await gt(lc, 'Menu', 'settings'):
        await settings(lc, chat_id, state)

    elif message.text == await gt(lc, 'Menu', 'made_by_rtools'):
        await message.answer(await gt(lc, 'Menu', 'rtools'), reply_markup=await rtools_kb(lc))

    else:
        if digit_check:
            return True
        else:
            await message.answer(await gt(lc, 'Common', 'wrong_text'))
