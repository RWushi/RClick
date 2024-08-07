from aiogram import Router, F
from Instruments.Config import States, get_translation as gt, get_language as gl
from Instruments.CGM import menu

ra = Router()


@ra.message(F.text, States.about)
async def about_handler(message, state):
    user_id = message.from_user.id
    chat_id = message.chat.id
    lc = await gl(user_id)

    if message.text == await gt(lc, 'About', 'about_product'):
        await message.answer(await gt(lc, 'About', 'product'))

    elif message.text == await gt(lc, 'About', 'about_rules'):
        await message.answer(await gt(lc, 'About', 'rules'))

    elif message.text == await gt(lc, 'About', 'about_fair_game'):
        await message.answer(await gt(lc, 'About', 'fair_game'))

    elif message.text == await gt(lc, 'Common', 'return_menu'):
        await menu(lc, chat_id, state)

    else:
        await message.answer(await gt(lc, 'Common', 'wrong_text'))
