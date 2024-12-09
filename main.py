
import argparse
import logging
import random
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from chat import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def schedule(context, chat_id):
    due = random.randint(100, 500)
    context.job_queue.run_once(send_message, due, chat_id=chat_id, name=str(chat_id), data=due)

def get_message():
    message = chat_get_message('There is a girl which name is Helen, generate a less than 10 words kind message to her')
    logging.info(f'Chat message : {message}')
    return message

async def send_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    schedule(context, job.chat_id)
    message = get_message()
    await context.bot.send_message(job.chat_id, text=message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    schedule(context, update.effective_message.chat_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Alright")

def load_messages(fpath):
    with open(fpath, 'r') as f:
        messages = json.load(f)
        f.close()

    return messages

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--token', type=str, required=True)
    args.add_argument('--msg', type=str, required=False, default='messages.json')

    args = args.parse_args()
    token = args.token

    msg_fpath = args.msg

    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()