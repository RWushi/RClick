from aiogram.types import (ReplyKeyboardMarkup as rkm, KeyboardButton as rkb,
                           InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb)
from .Config import get_translation as gt, admin_nickname

languages_kb = ikm(inline_keyboard=[
    [
        ikb(text="English🇺🇸", callback_data="EN"),
        ikb(text="中文🇨🇳", callback_data="ZH")
    ],
    [
        ikb(text="Español🇪🇸", callback_data="ES"),
        ikb(text="العربية🇸🇦", callback_data="AR")
    ],
    [
        ikb(text="हिन्दी🇮🇳", callback_data="HI"),
        ikb(text="Русский🇷🇺", callback_data="RU")
    ],
    [
        ikb(text="Українська🇺🇦", callback_data="UK"),
        ikb(text="Қазақша🇰🇿", callback_data="KZ")
    ]
])


async def menu_kb(lc):
    kb = rkm(keyboard=[
        [rkb(text=await gt(lc, "Menu", "play"))],
        [rkb(text=await gt(lc, "Menu", "about_bot"))],
        [
            rkb(text=await gt(lc, "Menu", "account")),
            rkb(text=await gt(lc, "Menu", "settings"))
        ],
        [rkb(text=await gt(lc, "Menu", "made_by_rtools"))]
        ], resize_keyboard=True)
    return kb


async def rtools_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Menu", "contact"), url="https://t.me/basfn")]])
    return kb


async def account_type_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Play", "real"), callback_data="real")],
        [ikb(text=await gt(lc, "Play", "demo"), callback_data="demo")],
        [ikb(text=await gt(lc, "Subcommon", "return_back"), callback_data="back")]])
    return kb


async def create_join_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Play", "create"), callback_data="create")],
        [ikb(text=await gt(lc, "Play", "join"), callback_data="join")],
        [ikb(text=await gt(lc, "Subcommon", "return_back"), callback_data="back")]])
    return kb


async def bet_kb(lc):
    kb = ikm(inline_keyboard=[
        [
            ikb(text="1", callback_data="1"),
            ikb(text="2", callback_data="2"),
            ikb(text="3", callback_data="3"),
            ikb(text="5", callback_data="5"),
        ],
        [
            ikb(text="10", callback_data="10"),
            ikb(text="15", callback_data="15"),
            ikb(text="20", callback_data="20"),
            ikb(text="30", callback_data="30")
        ],
        [
            ikb(text="50", callback_data="50"),
            ikb(text="75", callback_data="75"),
            ikb(text="100", callback_data="100"),
            ikb(text="150", callback_data="150")
        ],
        [
            ikb(text="250", callback_data="250"),
            ikb(text="500", callback_data="500"),
            ikb(text="750", callback_data="750"),
            ikb(text="1000", callback_data="1000")
        ],
        [ikb(text=await gt(lc, "Subcommon", "return_back"), callback_data="back")]])
    return kb


async def bet_range_kb(lc):
    kb = ikm(inline_keyboard=[
        [
            ikb(text="1-10", callback_data="1-10"),
            ikb(text="10-25", callback_data="10-50")
        ],
        [
            ikb(text="25-50", callback_data="25-50"),
            ikb(text="50-100", callback_data="50-100")
        ],
        [
            ikb(text="100-250", callback_data="100-250"),
            ikb(text="250-500", callback_data="250-500")
        ],
        [
            ikb(text="500-1000", callback_data="500-1000"),
            ikb(text=">1000", callback_data=">1000")
        ],
        [ikb(text=await gt(lc, "Subcommon", "return_back"), callback_data="back")]])
    return kb


click_kb = rkm(keyboard=[[rkb(text="📲")]], resize_keyboard=False)


async def join_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Play", "join_game"), callback_data="join")],
        [ikb(text=await gt(lc, "Play", "refresh"), callback_data="refresh")],
        [ikb(text=await gt(lc, "Subcommon", "return_back"), callback_data="back")]])
    return kb


async def about_kb(lc):
    kb = rkm(keyboard=[
        [rkb(text=await gt(lc, "About", "about_product"))],
        [rkb(text=await gt(lc, "About", "about_rules"))],
        [rkb(text=await gt(lc, "About", "about_fair_game"))],
        [rkb(text=await gt(lc, "Common", "return_menu"))]
        ], resize_keyboard=True)
    return kb


async def account_kb(lc):
    kb = rkm(keyboard=[
        [rkb(text=await gt(lc, "Account", "deposit"))],
        [
            rkb(text=await gt(lc, "Account", "top_up")),
            rkb(text=await gt(lc, "Account", "withdraw"))
        ],
        [
            rkb(text=await gt(lc, "Account", "statistics")),
            rkb(text=await gt(lc, "Account", "history"))
        ],
        [rkb(text=await gt(lc, "Common", "return_menu"))]
        ], resize_keyboard=True)
    return kb


async def settings_kb(lc):
    kb = rkm(keyboard=[
        [rkb(text=await gt(lc, "Settings", "my_id"))],
        [
            rkb(text=await gt(lc, "Settings", "change_language")),
            rkb(text=await gt(lc, "Settings", "support_button"))
        ],
        [rkb(text=await gt(lc, "Settings", "complaint"))],
        [rkb(text=await gt(lc, "Common", "return_menu"))]
        ], resize_keyboard=True)
    return kb


async def support_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Settings", "contact"), url=f"https://t.me/{admin_nickname}")]])
    return kb


async def confirm_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Settings", "continue"), callback_data="yes")],
        [ikb(text=await gt(lc, "Subcommon", "return_back"), callback_data="no")]])
    return kb


async def back_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Subcommon", "return_back"), callback_data="back")]])
    return kb


async def confirmation_kb(lc):
    kb = ikm(inline_keyboard=[
        [ikb(text=await gt(lc, "Complaint", "confirm"), callback_data="guilty")],
        [ikb(text=await gt(lc, "Complaint", "no_confirm"), callback_data="not_guilty")]])
    return kb


async def confirmation_admin_kb(accused_id):
    kb = ikm(inline_keyboard=[
        [ikb(text="Подтвердить✅", callback_data=f"{accused_id}:conf")],
        [ikb(text="Отклонить❌", callback_data=f"{accused_id}:no_conf")]])
    return kb
