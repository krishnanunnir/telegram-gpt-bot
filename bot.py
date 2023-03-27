import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import openai
import os

token=os.environ("BOT_KEY")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
openai.api_key = os.environ("OPENAI_KEY")

async def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a my personal assistant"},
        {"role": "user", "content": prompt},
        ]
    )

    return response['choices'][0]['message']['content']
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_text = await generate_response(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(token=token).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.run_polling()