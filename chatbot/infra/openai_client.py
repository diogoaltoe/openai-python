import os
from time import sleep

from openai import OpenAI, AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError, BadRequestError, \
    ConflictError, NotFoundError, InternalServerError, PermissionDeniedError, UnprocessableEntityError
from dotenv import load_dotenv

load_dotenv()


class OpenAiClient:
    OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL = "gpt-4-1106-preview"

    def chat_request(self, system_prompt, user_prompt):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }, {
                "role": "user",
                "content": user_prompt
            }
        ]

        return self.__perform_request(messages, 0, 5)

    def __perform_request(self, messages, attempt, wait_in_seconds):
        if attempt > 4:
            return 'Error with the OpenAI API. All attempts failed.'

        try:
            response = self.OPENAI_CLIENT.chat.completions.create(
                messages=messages,
                model=self.MODEL)

            return response.choices[0].message.content
        except APIConnectionError as e:
            return self.__prepare_new_attempt(messages, attempt, wait_in_seconds, 'Maybe we have a connection issue.')
        except (APITimeoutError, InternalServerError) as e:
            return self.__prepare_new_attempt(messages, attempt, wait_in_seconds, 'API is not responding.')
        except (AuthenticationError, PermissionDeniedError) as error:
            return 'Error with OpenAI API Key. ' + error.message
        except RateLimitError as e:
            return self.__prepare_new_attempt(messages, attempt, wait_in_seconds, 'Rate limit reached.')
        except (BadRequestError, ConflictError, NotFoundError, UnprocessableEntityError) as error:
            return 'Something went wrong with the OpenAI API. Received the Status Code: ' + str(
                error.status_code) + ' with Message: ' + error.message

    def __prepare_new_attempt(self, messages, attempt, wait_in_seconds, warning_message):
        print(warning_message + 'A new attempt will be made soon.')
        sleep(wait_in_seconds)

        return self.__perform_request(messages, attempt + 1, wait_in_seconds * 2)