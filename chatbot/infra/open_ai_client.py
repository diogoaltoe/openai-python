import os
from time import sleep

from openai import OpenAI, AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError, BadRequestError, \
    ConflictError, NotFoundError, InternalServerError, PermissionDeniedError, UnprocessableEntityError
from dotenv import load_dotenv

from chatbot.model.open_ai_model import OpenAiModel
from chatbot.operation.token_counter import count

load_dotenv()


def select_model(prompt):
    model = OpenAiModel.get_default()
    print('Using as default model: ', model.model())

    input_tokens = count(model.model(), prompt)
    print(f'The prompt has {input_tokens} tokens.')

    output_tokens = 2048
    total_tokens = input_tokens + output_tokens

    if total_tokens <= model.tokens():
        return model

    print('The current model cannot handle the prompt.')

    most_tokens_model = OpenAiModel.most_tokens()
    if total_tokens > most_tokens_model.tokens():
        raise BadRequestError(f'The prompt has more tokens ({input_tokens}) than the Model with Most Tokens '
                              f'current available ({most_tokens_model.tokens()}).')

    print('Changed model to: ', most_tokens_model.model())
    return most_tokens_model


class OpenAiClient:
    OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat_request(self, system_prompt, user_prompt):
        prompt = system_prompt + '\n' + user_prompt
        model = select_model(prompt)
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }, {
                "role": "user",
                "content": user_prompt
            }
        ]

        return self.__perform_request(model, messages, 0, 5)

    def __perform_request(self, model, messages, attempt, wait_in_seconds):
        if attempt > 4:
            return 'Error with the OpenAI API. All attempts failed.'

        try:
            response = self.OPENAI_CLIENT.chat.completions.create(
                messages=messages,
                model=model.model())

            return response.choices[0].message.content
        except APIConnectionError as e:
            return self.__prepare_new_attempt(model, messages, attempt, wait_in_seconds, 'Maybe we have a connection '
                                                                                         'issue.')
        except (APITimeoutError, InternalServerError) as e:
            return self.__prepare_new_attempt(model, messages, attempt, wait_in_seconds, 'API is not responding.')
        except (AuthenticationError, PermissionDeniedError) as error:
            return 'Error with OpenAI API Key. ' + error.message
        except RateLimitError as e:
            return self.__prepare_new_attempt(model, messages, attempt, wait_in_seconds, 'Rate limit reached.')
        except (BadRequestError, ConflictError, NotFoundError, UnprocessableEntityError) as error:
            return 'Something went wrong with the OpenAI API. Received the Status Code: ' + str(
                error.status_code) + ' with Message: ' + error.message

    def __prepare_new_attempt(self, model, messages, attempt, wait_in_seconds, warning_message):
        print(warning_message + 'A new attempt will be made soon.')
        sleep(wait_in_seconds)

        return self.__perform_request(model, messages, attempt + 1, wait_in_seconds * 2)