from aiogram import Router, F
from Instruments.Config import (SettingsStates, States, get_translation as gt,
                                get_language as gl)
from Instruments.CGM import game_id, game_id_errors as gie, cause, request_sent as rs
from Instruments.DB import (check_game_id as sgi, check_relevance_game as crg,
                            get_opponent_id as goi)
from .ComplaintMessage import accused_msg, complaint_info, player_ids

rsc = Router()


@rsc.callback_query(SettingsStates.confirm)
async def confirm_handler(callback, state):
    user_id = callback.from_user.id
    lc = await gl(user_id)
    choice = callback.data
    message_id = callback.message.message_id

    if choice == "yes":
        await game_id(lc, callback.message.chat.id, message_id, state)
        complaint_info[user_id] = [message_id]
    elif choice == "no":
        await callback.message.delete()
        await state.set_state(States.settings)


@rsc.callback_query(SettingsStates.game_id)
async def back_handler(callback, state):
    await callback.message.delete()
    await state.set_state(States.settings)


@rsc.callback_query(SettingsStates.reason)
async def back_handler(callback, state):
    user_id = callback.from_user.id
    lc = await gl(user_id)
    await game_id(lc, callback.message.chat.id, callback.message.message_id, state)


@rsc.message(F.text, SettingsStates.game_id)
async def game_id_handler(message, state):
    user_id = message.from_user.id
    lc = await gl(user_id)
    message_id = complaint_info[user_id][0]
    txt = message.text

    if txt.isdigit():
        await message.delete()
        game_id = int(txt)
        exists = await sgi(game_id)
        if exists:
            relevance_game = await crg(game_id, user_id)
            if relevance_game:
                accused_id = await goi(game_id, user_id)
                complaint_info[user_id].extend([accused_id, game_id])
                player_ids[accused_id] = [user_id]

                text = (f"{await gt(lc, 'Settings', 'user_id')}{accused_id}.\n"
                        f"{await gt(lc, 'Settings', 'enter_cause')}")
                await cause(message.chat.id, message_id, text, state)
            else:
                await gie(lc, 'invalid_game', message.chat.id, message_id)
        else:
            await gie(lc, 'no_exists', message.chat.id, message_id)

    elif (txt == await gt(lc, 'Settings', 'my_id') or
          txt == await gt(lc, 'Settings', 'change_language') or
          txt == await gt(lc, 'Settings', 'support_button') or
          txt == await gt(lc, 'Settings', 'complaint') or
          txt == await gt(lc, 'Common', 'return_menu')):
        await message.answer(await gt(lc, 'Subcommon', 'rb_first'))

    else:
        await gie(lc, 'enter_int_id', message.chat.id, message_id)


@rsc.message(F.text, SettingsStates.reason)
async def cause_handler(message, state):
    user_id = message.from_user.id
    lc = await gl(user_id)

    if (message.text == await gt(lc, 'Settings', 'my_id') or
            message.text == await gt(lc, 'Settings', 'change_language') or
            message.text == await gt(lc, 'Settings', 'support_button') or
            message.text == await gt(lc, 'Settings', 'complaint') or
            message.text == await gt(lc, 'Common', 'return_menu')):
        await message.answer(await gt(lc, 'Subcommon', 'rb_first'))

    else:
        message_id, accused_id, game_id = complaint_info[user_id]
        reason = message.text
        complaint_info[user_id].append(reason)
        await rs(lc, message.chat.id, message_id, state)
        await accused_msg(accused_id, game_id)


@rsc.message(F.text, SettingsStates.confirm)
async def confirm_handler(message):
    user_id = message.from_user.id
    lc = await gl(user_id)
    txt = message.text

    if (txt == await gt(lc, 'Settings', 'my_id') or
            txt == await gt(lc, 'Settings', 'change_language') or
            txt == await gt(lc, 'Settings', 'support_button') or
            txt == await gt(lc, 'Settings', 'complaint') or
            txt == await gt(lc, 'Common', 'return_menu')):
        await message.answer(await gt(lc, 'Subcommon', 'rb_first'))
