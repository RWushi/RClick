from aiogram import Router, F
from Instruments.Keyboards import confirmation_kb, confirmation_admin_kb, support_kb
from Instruments.Config import bot, get_translation as gt, get_language as gl, admin_id
from Instruments.DB import warning_check as wc, fine as f, full_fine as ff, full_fine_w as ffw

complaint_info = {}
player_ids = {}

rcm = Router()


async def accused_msg(accused_id, game_id, admin=False, guilty=False):
    lc = await gl(accused_id)

    if admin:
        if guilty:
            key, kb = 'guilty_a', await support_kb(lc)
        else:
            key, kb = 'not_guilty_a', None
        text = (f"{await gt(lc, 'Complaint', key)}\n"
                f"{await gt(lc, 'Complaint', 'game_id')}{game_id}.")

    else:
        warning = await wc(accused_id)
        player_ids[accused_id].append(warning)
        key = 'info_w' if warning else 'info'
        text = (f"{await gt(lc, 'Complaint', 'accusation')}{game_id}⚠️\n\n"
                f"{await gt(lc, 'Complaint', key)}")
        kb = await confirmation_kb(lc)

    await bot.send_message(accused_id, text, reply_markup=kb)


async def accuser_msg(accuser_id, guilty, key, game_id, accused_id=None, amount=None):
    lc = await gl(accuser_id)

    if guilty:
        text = (f"{await gt(lc, 'Accuser', key)}\n\n"
                f"{await gt(lc, 'Accuser', 'game_id')}{game_id}.\n"
                f"{await gt(lc, 'Accuser', 'accused_id')}{accused_id}.\n"
                f"{await gt(lc, 'Accuser', 'amount')}{amount}.")
        kb = None

    else:
        text = (f"{await gt(lc, 'Accuser', key)}\n"
                f"{await gt(lc, 'Accuser', 'game_id')}{game_id}.")
        kb = await support_kb(lc)

    await bot.send_message(accuser_id, text, reply_markup=kb)


@rcm.callback_query(F.data.endswith('guilty'))
async def confirmation_handler(callback):
    user_id = callback.from_user.id
    lc = await gl(user_id)
    choice = callback.data
    accuser_id, warning = player_ids[user_id]
    game_id = complaint_info[accuser_id][2]
    reason = complaint_info[accuser_id][3]

    if choice == "guilty":
        if warning:
            amount = await ffw(user_id, accuser_id)
            text_key = 'guilty_w'
        else:
            amount = await f(user_id, accuser_id, game_id)
            text_key = 'guilty'
        await callback.message.edit_text(await gt(lc, 'Complaint', text_key))
        await accuser_msg(accuser_id, True, 'guilty', game_id, user_id, amount)

    elif choice == "not_guilty":
        if warning:
            text_key = 'not_guilty_w'
        else:
            text_key = 'not_guilty'
        await callback.message.edit_text(await gt(lc, 'Complaint', text_key), reply_markup=await support_kb(lc))
        await admin_msg(warning, game_id, accuser_id, user_id, reason)
        await accuser_msg(accuser_id, False, 'not_guilty', game_id)


async def admin_msg(warning, game_id, accuser_id, accused_id, reason):
    info = ' и у него уже есть предупреждение' if warning else ''
    text = (f"Произошла отправка жалобы, обвиняемый не признал вину{info}.\n\n"
            f"ID игры: `{game_id}`\n"
            f"ID обвиняющего: `{accuser_id}`\n"
            f"ID обвиняемого: `{accused_id}`\n"
            f"Причина: `{reason}`")
    await bot.send_message(admin_id, text, reply_markup=await confirmation_admin_kb(accused_id), parse_mode='Markdown')


@rcm.callback_query(F.data.endswith('conf'))
async def confirmation_admin_handler(callback):
    data = callback.data.split(':')
    choice = data[1]
    accused_id = int(data[0])
    accuser_id = player_ids[accused_id][0]
    warning = player_ids[accused_id][1]
    game_id = complaint_info[accuser_id][2]

    if choice == "conf":
        if warning:
            amount = await ffw(accused_id, accuser_id)
        else:
            amount = await ff(accused_id, accuser_id)
        await accused_msg(accused_id, game_id, True, True)
        await accuser_msg(accuser_id, True, 'guilty_a', game_id, accused_id, amount)

    elif choice == "no_conf":
        await accused_msg(accused_id, game_id, True, False)
        await accuser_msg(accuser_id, False, 'not_guilty_a', game_id)
