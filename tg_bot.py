import os
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import logging
from intent_utils import detect_intent_texts
from logging_bot import TelegramLogsHandler


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!'
    )


def send_answer(update: Update, context: CallbackContext):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    answer = detect_intent_texts(
        project_id,
        update.effective_chat.id,
        [update.message.text],
        'ru-RU'
    )
    while True:
        if answer:
            context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


def run_bot(telegram_token):
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), send_answer))

    updater.start_polling()


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram_token, chat_id))

    try:
        run_bot(telegram_token)
        logger.info('Telegram bot started!')
    except Exception as ex:
        logger.exception(ex)


if __name__ == '__main__':
    main()
