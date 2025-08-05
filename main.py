import os
from dotenv import load_dotenv
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
TOKEN = os.getenv("TOKEN")

users = {}

emojis = {
    1 : "🎰",
    2 : "🎲",
    3 : "🎯",
    4 : "⚽",
    5 : "🏀"
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
    id = update.effective_user.id
    query = update.callback_query
    await query.answer()

    emo = emojis[int(query.data)]
    
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


bot = Application.builder().token(TOKEN).build()
bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("stop", stop))
bot.add_handler(CallbackQueryHandler(ChooseEmoji))

bot.run_polling(poll_interval=1, timeout=10)

