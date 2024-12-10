import argparse
import logging
import random
import json
import enum
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from chat import *
from deepl_api import *
from whisper_api import *
from gtts_api import text_to_speech_gtts
from tuser import TUser

languages = [
    'Polish',
    'English'
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def buildMainMenu():
    keyboard = [
        [
            InlineKeyboardButton("Translate", callback_data='Translate'),
            InlineKeyboardButton("Chat", callback_data='Chat'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup    

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    reply_markup = buildMainMenu()

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    user = TUser.get_user(update.effective_user)

    if query.data in languages:
        user.state = TUser.FunctionState.SelectLanguage    
    else:
        user.state = TUser.FunctionState[query.data]

    if user.state == TUser.FunctionState.Translate:
        keyboard = []
        for lang in languages:
            keyboard.append(
                [InlineKeyboardButton(lang, callback_data=lang)]
            )

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Please choose:", reply_markup=reply_markup)

    elif user.state == TUser.FunctionState.SelectLanguage:
        user.targetLanguage = query.data
        await query.edit_message_text(text=f"Selected option: {query.data}")
    elif user.state == TUser.FunctionState.Chat:
        await query.edit_message_text(text=f"Selected option: {query.data}")
    else:
        await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start_handler to test this bot.")

async def translate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.voice:
        fpath = await get_voice(update, context)
        message_text = transcribe_russian(fpath)
    else:
        message_text = update.message.text

    user = TUser.get_user(update.effective_user)

    translated_text = deepl_translate(message_text, user.targetLanguage)
    reply_markup = buildMainMenu()

    ogg_path = text_to_speech_gtts(translated_text, user.targetLanguage)
    await update.message.reply_voice(voice=open(ogg_path, 'rb'))
    os.remove(ogg_path)

    await update.message.reply_text(translated_text)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_text = chat_get_message(update.message.text)
    reply_markup = buildMainMenu()
    await update.message.reply_text(chat_text, reply_markup=reply_markup)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = TUser.get_user(update.effective_user)

    if user.state == TUser.FunctionState.SelectLanguage:
        await translate_handler(update, context)
    elif user.state == TUser.FunctionState.Chat:
        await chat_handler(update, context)

async def get_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = TUser.get_user(update.effective_user)
    downloadDir = os.path.join('downloads', 'users', f'{user.id}')

     # Create downloads directory if not exists
    if not os.path.exists(downloadDir):
        os.makedirs(downloadDir)

    # Get the voice message
    voice = update.message.voice
    if not voice:
        return None

    # Download the voice message
    file = await voice.get_file()
    ogg_path = os.path.join(downloadDir, f"{file.file_id}.ogg")
    await file.download_to_drive(ogg_path)
    await update.message.reply_text(f"Processing...")

    return ogg_path

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('--tokens', type=str, required=False)

    args = args.parse_args()
    tokens = args.tokens

    if args.tokens:
        tokens = args.tokens
    else:
        tokens = os.environ.get('TOKENS')
 
    with open(tokens, 'r') as f:
        tokens = json.load(f)
        f.close()

    deepl_set_auth(tokens['deepl'])

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(tokens['telegram']).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler((filters.VOICE | filters.TEXT) & ~filters.COMMAND, message_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)