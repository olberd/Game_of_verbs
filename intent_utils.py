import json
import os

from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        if not response.query_result.intent.is_fallback:
            return response.query_result.fulfillment_text
        else:
            return None


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def get_intents_from_json(json_file='questions.json'):
    with open(json_file, 'r', encoding='utf-8') as my_file:
        file_contents = my_file.read()
    intents = json.loads(file_contents)
    return intents


def main():
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    intents = get_intents_from_json()
    for key, item in intents.items():
        create_intent(project_id, key, item['questions'], [item['answer']])


if __name__ == '__main__':
    main()
