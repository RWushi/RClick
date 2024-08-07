from .Keyboards import (languages_kb, menu_kb, account_type_kb, create_join_kb,
                        bet_kb, bet_range_kb, click_kb, about_kb, join_kb,
                        account_kb, settings_kb, confirm_kb, back_kb)
from .Config import bot, get_translation as gt, States, PlayStates, SettingsStates
from .DB import create_game as cg, check_game as chg
import asyncio

guest_repeats = {}
host_repeats = {}
host_info = {}


async def languages(chat_id, state):
    text = (
        "Choose your language\n"
        "选择语言\n"
        "Elige tu idioma\n"
        "اختر لغتك\n"
        "अपनी भाषा चुनें\n"
        "Выберите язык\n"
        "Виберіть мову\n"
        "Тілді таңдаңыз"
    )
    await bot.send_message(chat_id, text, reply_markup=languages_kb)
    await state.set_state(States.languages)


async def menu(lc, chat_id, state):
    text = await gt(lc, 'Menu', 'menu')
    kb = await menu_kb(lc)
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(States.menu)


async def account_type(lc, chat_id, state, message_id=None):
    text = await gt(lc, 'Play', 'play')
    kb = await account_type_kb(lc)
    if message_id:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb)
    else:
        await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(PlayStates.account_type)


async def create_join(lc, chat_id, message_id, state):
    text = await gt(lc, 'Play', 'create_join')
    kb = await create_join_kb(lc)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb)
    await state.set_state(PlayStates.create_join)


async def bet(lc, key, chat_id, message_id, state, user_id=None):
    text = await gt(lc, 'Play', key)
    if key == 'choose_bet':
        kb = await bet_kb(lc)
        await state.set_state(PlayStates.bet)
    elif key == 'bet_range':
        kb = await bet_range_kb(lc)
        await state.set_state(PlayStates.bet)
    elif key == 'enter_int_bet':
        if (guest_repeats[user_id] is not None and guest_repeats[user_id]
                and guest_repeats[user_id][0] == key):
            await bot.delete_message(chat_id, message_id)
            await bot.send_message(chat_id, text)
            return
        kb = None
    elif key == 'room_canceled':
        kb = await bet_kb(lc)
        await state.set_state(PlayStates.bet)
    elif key == 'no_games':
        kb = await bet_range_kb(lc)
    guest_repeats[user_id] = [key]
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb)


async def new_game(user_id, chat_id, message_id, lc, bet, account, state):
    if await cg(user_id, bet, account):
        text = await gt(lc, 'Play', 'room_created')
        kb = await back_kb(lc)
        await state.set_state(PlayStates.room_created)
    else:
        key = 'not_enough'
        text = await gt(lc, 'Play', key)
        kb = await bet_kb(lc)
        if (host_repeats[user_id] is not None and guest_repeats[user_id]
                and guest_repeats[user_id][0] == key):
            await bot.delete_message(chat_id, message_id)
            await bot.send_message(chat_id, text, reply_markup=kb)
            return

    host_repeats[user_id] = [key]
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb)


async def send_games(chat_id, message_id, lc, games, state, edit_anyway=False):
    game_list = []
    for index, game in enumerate(games, start=1):
        room_id = game['id']
        room_bet = game['bet']
        game_str = (f"{await gt(lc, 'Play', 'game_header')}{index}: "
                    f"{await gt(lc, 'Play', 'id')}{room_id}, "
                    f"{await gt(lc, 'Play', 'bet')}{room_bet}")
        game_list.append(game_str)
    text = f"{await gt(lc, 'Play', 'game_list')}{'\n'.join(game_list)}"

    kb = await join_kb(lc)
    if not edit_anyway:
        if len(guest_repeats[chat_id]) > 1 and guest_repeats[chat_id][1] == text:
            return 'repeat'
    guest_repeats[chat_id].append(text)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb)
    await state.set_state(PlayStates.rooms)


async def choose_game(lc, chat_id, key, message_id, state):
    text = await gt(lc, 'Play', key)
    kb = await back_kb(lc)
    if len(guest_repeats[chat_id]) > 2 and guest_repeats[chat_id][2] == key:
        await bot.send_message(chat_id, text, reply_markup=kb)
    else:
        guest_repeats[chat_id].append(key)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb)
        await state.set_state(PlayStates.game_id)


async def start_game(lc, guest, game_id, msg_id_guest, state_guest):
    result = await chg(game_id, guest)

    if result in ('not_exists', 'not_free'):
        if result == 'not_exists':
            key = 'enter_valid_id'
        elif result == 'not_free':
            key = 'game_full'
        guest_text = await gt(lc, 'Play', key)
        kb = await back_kb(lc)
        if len(guest_repeats[guest]) > 2 and guest_repeats[guest][2] == key:
            await bot.send_message(guest, guest_text, reply_markup=kb)
        else:
            await bot.edit_message_text(guest_text, None, guest, msg_id_guest, reply_markup=kb)

    else:
        host = result
        msg_id_host, state_host = host_info[host]
        guest_text = await gt(lc, 'About', 'game_full_guest')
        host_text = await gt(lc, 'About', 'game_full_host')
        kb = await click_kb
        await bot.edit_message_text(guest_text, None, guest, msg_id_guest, reply_markup=kb)
        await bot.edit_message_text(host_text, None, host, msg_id_host, reply_markup=kb)
        await state_guest.set_state(PlayStates.clicks)
        await state_host.set_state(PlayStates.clicks)
        await starting_game(guest, msg_id_guest, host, msg_id_host)

    guest_repeats[guest].append(key)


async def starting_game(guest, msg_id_guest, host, msg_id_host):
    countdown = ["3️⃣", "2️⃣", "1️⃣", "🚀"]
    await asyncio.sleep(5)
    for symbol in countdown:
        await asyncio.sleep(1)
        await bot.edit_message_text(symbol, None, guest, msg_id_guest)
        await bot.edit_message_text(symbol, None, host, msg_id_host)


async def about(lc, chat_id, state):
    text = await gt(lc, 'About', 'about')
    kb = await about_kb(lc)
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(States.about)


async def account(lc, chat_id, state):
    text = await gt(lc, 'Account', 'account')
    kb = await account_kb(lc)
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(States.account)


async def settings(lc, chat_id, state):
    text = await gt(lc, 'Settings', 'settings')
    kb = await settings_kb(lc)
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(States.settings)


async def confirm(lc, chat_id, state):
    text = await gt(lc, 'Settings', 'warning')
    kb = await confirm_kb(lc)
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(SettingsStates.confirm)


async def game_id(lc, chat_id, message_id, state):
    text = await gt(lc, 'Settings', 'enter_game_id')
    kb = await back_kb(lc)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb)
    await state.set_state(SettingsStates.game_id)


async def game_id_errors(lc, key, chat_id, message_id):
    text = await gt(lc, 'Settings', key)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text)


async def cause(chat_id, message_id, text, state):
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text)
    await state.set_state(SettingsStates.reason)


async def request_sent(lc, chat_id, message_id, state):
    text = await gt(lc, 'Settings', 'request_sent')
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text)
    await state.set_state(States.settings)
