from aiogram import Router, F
from Instruments.Config import States, PlayStates, get_translation as gt, get_language as gl
from Instruments.CGM import (host_info, account_type as at, create_join as cj, bet,
                             new_game as ng, send_games as sg, choose_game as chg, start_game as s_g)
from Instruments.DB import get_games as gg, cancel_game as cg
from Categories.Menu import menu_handler

game_info = {}
host_guest = {}
guest_bet = {}
msgs_to_del = {}

rp = Router()


@rp.callback_query(PlayStates.account_type)
async def account_type_handler(callback, state):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    lc = await gl(user_id)
    choice = callback.data

    if choice in ("real", "demo"):
        await cj(lc, callback.message.chat.id, message_id, state)
        game_info[user_id] = [message_id, choice]
    elif choice == "back":
        await callback.message.delete()
        await state.set_state(States.menu)


@rp.callback_query(PlayStates.create_join)
async def create_join_handler(callback, state):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    lc = await gl(user_id)
    choice = callback.data

    if choice == "create":
        host_guest[user_id] = True
        await bet(lc, 'choose_bet', chat_id, message_id, state)
    elif choice == "join":
        host_guest[user_id] = False
        await bet(lc, 'bet_range', chat_id, message_id, state)
    elif choice == "back":
        await at(lc, chat_id, state, message_id)


@rp.callback_query(PlayStates.bet)
async def bet_handler(callback, state):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    account = game_info[user_id][1]
    lc = await gl(user_id)
    call = callback.data

    if "-" in call or ">" in call:
        if "-" in call:
            lower, upper = map(int, call.split("-"))
        elif ">" in call:
            lower, upper = 1000, None
        guest_bet[user_id] = (lower, upper)
        games = await gg(account, lower, upper)
        if games:
            await sg(chat_id, message_id, lc, games, state)
        else:
            await bet(lc, 'no_games', chat_id, message_id, state)

    elif call == "back":
        await cj(lc, chat_id, message_id, state)

    else:
        stake = int(call)
        account = game_info[user_id][1]
        host_info[user_id] = (message_id, state)
        await ng(user_id, chat_id, message_id, lc, stake, account, state)


@rp.message(F.text, PlayStates.bet)
async def custom_bet_handler(message, state):
    user_id = message.from_user.id
    lc = await gl(user_id)
    chat_id = message.chat.id
    message_id, account = game_info[user_id]
    txt = message.text

    if txt.isdigit():
        await message.delete()
        stake = int(txt)
        if host_guest[user_id]:
            await ng(user_id, chat_id, message_id, lc, stake, account, state)
        else:
            games = await gg(account, bet=stake)
            if games:
                await sg(chat_id, message_id, lc, games, state)
            else:
                await bet(lc, 'no_games', chat_id, message_id, state)

    else:
        send = await menu_handler(message, state, True)
        if send:
            await message.delete()
        await bet(lc, 'enter_int_bet', message.chat.id, message_id, state, user_id)


@rp.callback_query(PlayStates.room_created)
async def back_handler(callback, state):
    user_id = callback.from_user.id
    lc = await gl(user_id)
    chat_id = callback.message.chat.id
    await cg(user_id)
    await bet(lc, 'room_canceled', chat_id, callback.message.message_id, state)


@rp.callback_query(PlayStates.rooms)
async def join_handler(callback, state):
    call = callback.data
    user_id = callback.from_user.id
    lc = await gl(user_id)
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    if call == "join":
        await chg(lc, chat_id, 'enter_id', message_id, state)
    elif call == "refresh":
        account = game_info[user_id][1]
        lower, upper = guest_bet[user_id]
        games = await gg(account, lower, upper)
        repeat = await sg(chat_id, message_id, lc, games, state)
        if repeat:
            await callback.answer(await gt(lc, 'Play', 'no_changes'), show_alert=True)
    elif call == "back":
        await bet(lc, 'bet_range', chat_id, message_id, state)


@rp.message(F.text, PlayStates.game_id)
async def game_id_handler(message, state):
    user_id = message.from_user.id
    guest_chat_id = message.chat.id
    lc = await gl(user_id)
    message_id = game_info[user_id][0]
    txt = message.text

    if txt.isdigit():
        await message.delete()
        game_id = int(txt)
        await s_g(lc, guest_chat_id, game_id, message_id, state)

    else:
        send = await menu_handler(message, state, True)
        if send:
            await message.delete()
            await chg(lc, guest_chat_id, 'enter_int_id', message_id, state)



@rp.callback_query(PlayStates.game_id)
async def back_handler(callback, state):
    user_id = callback.from_user.id
    lc = await gl(user_id)
    account = game_info[user_id][1]
    lower, upper = guest_bet[user_id]
    games = await gg(account, lower, upper)
    await sg(callback.message.chat.id, callback.message.message_id,
             lc, games, state, True)


@rp.message(F.text, PlayStates.account_type)
@rp.message(F.text, PlayStates.create_join)
@rp.message(F.text, PlayStates.room_created)
@rp.message(F.text, PlayStates.rooms)
async def return_handler(message, state):
    await menu_handler(message.chat.id, state)
