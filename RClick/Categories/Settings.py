from aiogram import Router, F
from Instruments.Keyboards import languages_kb, support_kb
from Instruments.Config import States, get_translation as gt, get_language as gl, set_language as sl
from Instruments.CGM import menu, confirm
from Instruments.DB import language_set as ls

rs = Router()


@rs.message(F.text, States.settings)
async def settings_handler(message, state):
    user_id = message.from_user.id
    chat_id = message.chat.id
    lc = await gl(user_id)

    if message.text == await gt(lc, 'Settings', 'my_id'):
        text = f"{await gt(lc, 'Settings', 'your_id')}`{user_id}`\n{await gt(lc, 'Settings', 'id_info')}"
        await message.answer(text, parse_mode='Markdown')

    elif message.text == await gt(lc, 'Settings', 'change_language'):
        await message.answer(await gt(lc, 'Settings', 'choose_language'), reply_markup=languages_kb)

    elif message.text == await gt(lc, 'Settings', 'support_button'):
        await message.answer(await gt(lc, 'Settings', 'contact_text'), reply_markup=await support_kb(lc))

    elif message.text == await gt(lc, 'Settings', 'complaint'):
        await confirm(lc, chat_id, state)

    elif message.text == await gt(lc, 'Common', 'return_menu'):
        await menu(lc, chat_id, state)

    else:
        await message.answer(await gt(lc, 'Common', 'wrong_text'))


@rs.callback_query(States.settings)
async def language_change_handler(callback):
    user_id = callback.from_user.id
    lc = callback.data
    await sl(user_id, lc)
    await ls(user_id, lc)
    await callback.message.delete()
    await callback.answer(await gt(lc, 'Settings', 'language_changed'), show_alert=True)
