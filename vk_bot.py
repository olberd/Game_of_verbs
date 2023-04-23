import os
import random
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from intent_utils import detect_intent_texts


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            answer = detect_intent_texts('game-of-vebs-bssh', event.user_id, [event.text], 'ru-RU')
            if answer:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=answer,
                    random_id=random.randint(1, 1000)
                )


if __name__ == "__main__":
    main()
