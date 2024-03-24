import json
import os
import re
from time import sleep

from openai import OpenAI, AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError, BadRequestError, \
    ConflictError, NotFoundError, InternalServerError, PermissionDeniedError, UnprocessableEntityError
from dotenv import load_dotenv

from chatbot.model.open_ai_model import OpenAiModel
from chatbot.model.open_ai_run_status import OpenAiRunStatus
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
        return model.model()

    print('The current model cannot handle the prompt.')

    most_tokens_model = OpenAiModel.most_tokens()
    if total_tokens > most_tokens_model.tokens():
        raise BadRequestError(f'The prompt has more tokens ({input_tokens}) than the Model with Most Tokens current '
                              f'available ({most_tokens_model.tokens()}).')

    print('Changed model to: ', most_tokens_model.model())
    return most_tokens_model.model()


class OpenAiClient:
    OPENAI_CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # CHAT

    def chat_request(self, system_prompt, user_prompt):
        prompt = system_prompt + '\n' + user_prompt
        model = select_model(prompt)
        messages = [
            {
                'role': 'system',
                'content': system_prompt
            }, {
                'role': 'user',
                'content': user_prompt
            }
        ]

        return self.__perform_chat_request(model, messages, 0, 5)

    def __perform_chat_request(self, model, messages, attempt, wait_in_seconds):
        if attempt > 4:
            return 'Error with the OpenAI API. All attempts failed.'

        try:
            response = self.OPENAI_CLIENT.chat.completions.create(
                messages=messages,
                model=model)

            return response.choices[0].message.content
        except APIConnectionError as e:
            return self.__prepare_new_chat_attempt(model, messages, attempt, wait_in_seconds,
                                                   'Maybe we have a connection issue.')
        except (APITimeoutError, InternalServerError) as e:
            return self.__prepare_new_chat_attempt(model, messages, attempt, wait_in_seconds, 'API is not responding.')
        except (AuthenticationError, PermissionDeniedError) as error:
            return 'Error with OpenAI API Key. ' + error.message
        except RateLimitError as e:
            return self.__prepare_new_chat_attempt(model, messages, attempt, wait_in_seconds, 'Rate limit reached.')
        except (BadRequestError, ConflictError, NotFoundError, UnprocessableEntityError) as error:
            return 'Something went wrong with the OpenAI API. Received the Status Code: ' + str(
                error.status_code) + ' with Message: ' + error.message

    def __prepare_new_chat_attempt(self, model, messages, attempt, wait_in_seconds, warning_message):
        print(warning_message + 'A new attempt will be made soon.')
        sleep(wait_in_seconds)

        return self.__perform_chat_request(model, messages, attempt + 1, wait_in_seconds * 2)

    # ASSISTANT

    def assistant_request(self, user_prompt, thread_id, available_functions):
        assistant_id = os.getenv('OPENAI_API_ASSISTANT_ID')
        print('Using the existing assistant:', assistant_id)

        return self.__prepare_assistant_request(user_prompt, thread_id, assistant_id, available_functions)

    def new_assistant_request(self, system_prompt, user_prompt, thread_id, available_functions, available_tools):
        assistant = self.__create_assistant(system_prompt, user_prompt, available_tools)
        assistant_id = assistant.id
        print('New assistant:', assistant_id)

        return self.__prepare_assistant_request(user_prompt, thread_id, assistant_id, available_functions)

    def __prepare_assistant_request(self, user_prompt, thread_id, assistant_id, available_functions):
        if thread_id is None:
            print('Creating a new thread for the assistant.')

            thread = self.__create_thread(user_prompt)
            thread_id = thread.id
            print('New thread for the assistant:', thread_id)
        else:
            print('Using the existing thread for the assistant:', thread_id)

        return self.__perform_assistant_request(assistant_id, thread_id, user_prompt, available_functions, 0, 5)

    def __create_assistant(self, system_prompt, user_prompt, available_tools):
        prompt = system_prompt + '\n' + user_prompt
        model = select_model(prompt)

        return self.OPENAI_CLIENT.beta.assistants.create(
            name='EcoMart Assistant',
            instructions=system_prompt,
            model=model,
            tools=available_tools
        )

    def __create_thread(self, user_prompt):
        return self.OPENAI_CLIENT.beta.threads.create(
            messages=[
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ]
        )

    def __create_message(self, thread_id, user_prompt):
        self.OPENAI_CLIENT.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content=user_prompt
        )

    def __create_run(self, thread_id, assistant_id):
        return self.OPENAI_CLIENT.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

    def __retrieve_run(self, thread_id, run_id):
        return self.OPENAI_CLIENT.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

    def __perform_assistant_request(self, assistant_id, thread_id, user_prompt, available_functions, attempt, wait_in_seconds):
        if attempt > 4:
            return 'Error with the OpenAI API. All attempts failed.'

        try:
            self.__create_message(thread_id, user_prompt)

            run = self.__create_run(thread_id, assistant_id)

            while run.status != OpenAiRunStatus.COMPLETED.value:
                run = self.__retrieve_run(thread_id, run.id)
                self.__prepare_required_action(run, thread_id, available_functions)
            print('Run is completed.')

            messages = list(self.OPENAI_CLIENT.beta.threads.messages.list(thread_id=thread_id).data)
            pattern = r'\u3010.*?\u3011'
            return re.sub(pattern, '', messages[0].content[0].text.value), messages[0].thread_id

        except APIConnectionError as e:
            return self.__prepare_new_assistant_attempt(assistant_id, thread_id, user_prompt, available_functions,
                                                        attempt, wait_in_seconds,'Maybe we have a connection issue.')
        except (APITimeoutError, InternalServerError) as e:
            return self.__prepare_new_assistant_attempt(assistant_id, thread_id, user_prompt, available_functions,
                                                        attempt, wait_in_seconds,'API is not responding.')
        except (AuthenticationError, PermissionDeniedError) as error:
            return 'Error with OpenAI API Key. ' + error.message
        except RateLimitError as e:
            return self.__prepare_new_assistant_attempt(assistant_id, thread_id, user_prompt, available_functions,
                                                        attempt, wait_in_seconds,'Rate limit reached.')
        except (BadRequestError, ConflictError, NotFoundError, UnprocessableEntityError) as error:
            return 'Something went wrong with the OpenAI API. Received the Status Code: ' + str(
                error.status_code) + ' with Message: ' + error.message

    def __prepare_new_assistant_attempt(self, assistant_id, thread_id, user_prompt, available_functions,
                                        attempt, wait_in_seconds, warning_message):
        print(warning_message + 'A new attempt will be made soon.')
        sleep(wait_in_seconds)

        return self.__perform_assistant_request(assistant_id, thread_id, user_prompt, available_functions,
                                                attempt + 1, wait_in_seconds * 2)

    def __prepare_required_action(self, run, thread_id, available_functions):
        if run.status != OpenAiRunStatus.REQUIRES_ACTION.value:
            return

        tool_calls_responses = []
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        for tool in tool_calls:
            function_name = tool.function.name
            selected_function = available_functions[function_name]
            args = json.loads(tool.function.arguments)
            print("Passing the arguments:", args)
            function_response = selected_function(args)
            tool_calls_responses.append({
                'tool_call_id': tool.id,
                'output': function_response
            })

        print("Function responses:", tool_calls_responses)
        self.OPENAI_CLIENT.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_calls_responses
        )