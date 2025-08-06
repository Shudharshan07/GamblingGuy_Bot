import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
bot = Application.builder().token(TOKEN).build()
app = FastAPI()

users = {}

emojis = {
    "1" : "🎰",
    "2" : "🎲",
    "3" : "🎯",
    "4" : "⚽",
    "5" : "🏀"
}

KeyBoard = [
        [InlineKeyboardButton("🎰 Slot Machine", callback_data=1)],
        [InlineKeyboardButton("🎲 Dice", callback_data=2)],
        [InlineKeyboardButton("🎯 Dart", callback_data=3)],
        [InlineKeyboardButton("⚽ Football", callback_data=4)],
        [InlineKeyboardButton("🏀 BasketBall", callback_data=5)]
    ]

async def start(update, context):
    global KeyBoard
    reply = InlineKeyboardMarkup(KeyBoard)

    id = update.effective_chat.id
    await context.bot.send_message(chat_id = id, text = "Choose an emoji", reply_markup=reply)
    
    

async def ChooseEmoji(update, context):
    query = update.callback_query
    await query.answer()

    id = query.message.chat.id
    emo = emojis[query.data]
    
    task =  asyncio.create_task(emoji(update=update, context=context, id=id,emo=emo))
    users[id] = task

async def emoji(update, context, id, emo):
    while True:
        await context.bot.send_dice(chat_id=id, emoji=emo)
        await asyncio.sleep(2)


async def stop(update, context):
    id = update.effective_chat.id
    users[id].cancel()
    await update.message.reply_text("Quitter")



bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("stop", stop))
bot.add_handler(CallbackQueryHandler(ChooseEmoji))

@app.get("/")
async def root():
    return {"message": "working"}


@app.post("/webhook")
async def webhook(request):
    update = Update.de_json(await request.json(), bot.bot)
    await bot.process_update(update)

    return {"status" : "working"}


@app.on_event("startup")
async def startup():
    await bot.initialize()
    await bot.bot.set_webhook(url=URL)
    await bot.start()


