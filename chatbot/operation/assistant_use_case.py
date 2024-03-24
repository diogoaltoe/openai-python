from chatbot.infra.open_ai_client import OpenAiClient
from chatbot.operation.helpers import read_file


def answer_question(user_prompt, thread_id):
    client = OpenAiClient()
    return client.assistant_request(user_prompt, thread_id)


def answer_question_custom(user_prompt, thread_id):
    info = read_file("chatbot/data/info.md")
    policy = read_file("chatbot/data/policy.md")

    system_prompt = f"""
        You are an e-commerce customer service chatbot.
        You should not answer questions that are not informed ecommerce data!
        You must generate responses using the context below.
        The EcoMart company has three main documents that detail different aspects of the business:

        # Document 1:
        {info}

        # Document 2:
        {policy}
    """
    client = OpenAiClient()
    return client.new_assistant_request(system_prompt, user_prompt, thread_id)


class AssistantUseCase:
    pass
