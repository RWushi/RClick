from aiogram import Router, F
from Instruments.Config import States, get_translation as gt, get_language as gl
from Instruments.CGM import menu
from Instruments.DB import show_account as sa

rac = Router()


@rac.message(F.text, States.account)
async def account_handler(message, state):
    user_id = message.from_user.id
    chat_id = message.chat.id
    lc = await gl(user_id)

    if message.text == await gt(lc, 'Account', 'deposit'):
        real, demo = await sa(user_id)
        text = f"{await gt(lc, 'Account', 'real')}{real}\n{await gt(lc, 'Account', 'demo')}{demo}"
        await message.answer(text)

    elif message.text == await gt(lc, 'Account', 'top_up'):
        await message.answer(await gt(lc, 'Subcommon', 'not_ready'))

    elif message.text == await gt(lc, 'Account', 'withdraw'):
        await message.answer(await gt(lc, 'Subcommon', 'not_ready'))

    elif message.text == await gt(lc, 'Account', 'statistics'):
        await message.answer(await gt(lc, 'Account', 'statistics_loading'))

    elif message.text == await gt(lc, 'Account', 'history'):
        await message.answer(await gt(lc, 'Subcommon', 'not_ready'))

    elif message.text == await gt(lc, 'Common', 'return_menu'):
        await menu(lc, chat_id, state)

    else:
        await message.answer(await gt(lc, 'Common', 'wrong_text'))
