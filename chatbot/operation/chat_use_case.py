from chatbot.infra.open_ai_client import OpenAiClient


def answer_question(user_prompt):
    system_prompt = ('You are an ecommerce customer service chat-bot and must only answer questions related to '
                     'ecommerce.')
    client = OpenAiClient()
    return client.chat_request(system_prompt, user_prompt)


class ChatUseCase:
    pass
