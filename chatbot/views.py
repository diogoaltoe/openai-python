import json

from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

from chatbot.operation.chat_use_case import answer_question as chat_answer
from chatbot.operation.assistant_use_case import answer_question as assistant_answer


def index(request):
    current_time = datetime.now().strftime("%H:%M")
    return render(request, 'chatbot/index.html', {'current_time': current_time})


def bot(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            bot_type = json_data.get('bot', '')
            user_message = json_data.get('message', '')

            if bot_type == 'chat':
                bot_message = chat_request(user_message)
            else:
                thread = json_data.get('thread', '')
                thread_id = None if len(thread) == 0 else thread
                bot_message = assistant_request(user_message, thread_id)

            return JsonResponse(bot_message)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'message': 'Invalid Operation'}, status=400)


def chat_request(prompt):
    bot_message = chat_answer(prompt)
    return {'message': bot_message}


def assistant_request(prompt, thread_id):
    bot_message, thread_id = assistant_answer(prompt, thread_id)
    return {'message': bot_message, 'thread': thread_id}
