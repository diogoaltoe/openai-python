from django.urls import path
from chatbot.views import index, chat

urlpatterns = [
    path('', index),
    path('chat/', chat, name='chat')
]
