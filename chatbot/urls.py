from django.urls import path
from chatbot.views import index, bot

urlpatterns = [
    path('', index),
    path('bot/', bot, name='bot')
]
