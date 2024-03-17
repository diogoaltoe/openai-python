import json

from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

from chatbot.operation.chat_use_case import answer_question


def index(request):
    current_time = datetime.now().strftime("%H:%M")
    return render(request, 'chatbot/index.html', {'current_time': current_time})


def chat(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            user_message = json_data.get('message', '')
            bot_message = chat_request(user_message)
            data = {'message': bot_message}
            return JsonResponse(data)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'message': 'Invalid Operation'}, status=400)


def chat_request(prompt):
    return answer_question(prompt)
