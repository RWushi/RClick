import os
from Instruments.Config import bot, dp, app
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from Categories.Languages import rl
from Categories.Menu import rm
from Categories.Play import rp
from Categories.About import ra
from Categories.Account import rac
from Categories.Settings import rs
from Categories.Complaint import rsc
from Categories.ComplaintMessage import rcm

for router in [rl, rm, rp, ra, rac, rs, rsc, rcm]:
    dp.include_router(router)


async def on_startup(app):
    await bot.set_webhook(os.getenv("WEBHOOK_URL"))


async def on_shutdown(app):
    await bot.delete_webhook()

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path='/')
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    web.run_app(app, port=8080)
