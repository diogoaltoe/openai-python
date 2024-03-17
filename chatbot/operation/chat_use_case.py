from chatbot.infra.open_ai_client import OpenAiClient


def answer_question(user_prompt):
    system_prompt = ['You are an ecommerce customer service chat-bot and must only answer questions related to '
                     'ecommerce.',
                     'You are also a product categorizer and if customer inform a product name, you must to answer '
                     'the name of the product category entered.',
                     'Choose a category from the list below:\n'
                     '    Electronics\n'
                     '    Apparel and Fashion\n'
                     '    Home and Kitchen Appliances\n'
                     '    Beauty and Personal Care\n'
                     '    Automotive Parts and Accessories\n'
                     '    Sports and Outdoor Equipment\n'
                     '    Books and Media\n'
                     '    Toys and Games\n'
                     '    Health and Wellness Products\n'
                     '    Furniture and Home Decor\n'
                     '    Others']
    client = OpenAiClient()
    return client.chat_request(' '.join(system_prompt), user_prompt)


class ChatUseCase:
    pass
