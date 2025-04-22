from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.web.router import router as web_router
# from app.tg.router import router as tg_router

from contextlib import asynccontextmanager
# from app.tg.bot import bot, dp, bot_settings
from fastapi.staticfiles import StaticFiles

# from aiogram.types import Update

# @asynccontextmanager
# async def lifespan(app: FastAPI):
    # Set webhook for telegram bot
    # webhook_url = bot_settings.get_webhook_url()
    # await bot.set_webhook(
    #     url=webhook_url,
    #     allowed_updates=dp.resolve_used_update_types(),
    #     drop_pending_updates=True
    # )
    # print(f"Webhook set to {webhook_url}")
    # yield  # app working
    # # Upon closing of application -> webhook remove, bot session close
    # await bot.delete_webhook()
    # print("Webhook removed")
    # await bot.session.close()



# Creating fastAPI App
# app = FastAPI(lifespan=lifespan)

app = FastAPI()

# adding router for web API
app.include_router(web_router, prefix="/api/v1/web", tags=["web API"])

# # adding router for telegram bot API
# app.include_router(tg_router, prefix="/api/v1/tg")

# # adding path to static files for telegram bot
# app.mount("/api/v1/tg/images", StaticFiles(directory="app/templates/tg/images"), name="tg-images")
# app.mount("/api/v1/tg/style", StaticFiles(directory="app/templates/tg/style"), name="tg-style")
# app.mount("/api/v1/tg/js", StaticFiles(directory="app/templates/tg/js"), name="tg-js")
# app.mount("/api/v1/tg/fonts", StaticFiles(directory="app/templates/tg/fonts"), name="tg-fonts")

# adding path to static files for website
app.mount("/api/v1/web/images", StaticFiles(directory="app/web/images"), name="web-images")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5050",
    "http://localhost:3000",
    "https://soapdesign.ru",
    "https://www.soapdesign.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# @app.post("/api/v1/tg/webhook")
# async def webhook(request: Request) -> None:
#     print("Received webhook request")
#
#     # convert request to update type from aiogram
#     update = Update.model_validate(await request.json(), context={"bot": bot})
#
#     print(update.message.text)
#     await dp.feed_update(bot, update)
#
#     print("Update processed")