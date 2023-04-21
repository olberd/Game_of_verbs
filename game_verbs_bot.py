import os
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import logging
from intent_utils import detect_intent_texts


load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

telegram_token = os.getenv('TELEGRAM_TOKEN')
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте!')


def echo(update: Update, context: CallbackContext):
    answer = detect_intent_texts('game-of-vebs-bssh', update.effective_chat.id, [update.message.text], 'ru-RU')
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


if __name__ == '__main__':
    updater.start_polling()
