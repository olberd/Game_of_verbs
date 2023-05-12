import os
import random
import logging
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from intent_utils import detect_intent_texts
from logging_bot import TelegramLogsHandler

logger = logging.getLogger(__name__)


def start_bot():
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            answer = detect_intent_texts(project_id, event.user_id, [event.text], 'ru-RU')
            if answer:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=answer,
                    random_id=random.randint(1, 1000)
                )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram_token, chat_id))
    logger.info('VK bot started!')

    try:
        start_bot()
    except Exception as ex:
        logger.exception(ex)
