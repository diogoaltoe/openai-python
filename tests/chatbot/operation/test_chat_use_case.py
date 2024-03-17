from unittest import TestCase

from chatbot.operation.chat_use_case import answer_question


class TestChatUseCase(TestCase):

    def test_answer_question_success(self):
        prompt = 'sunglasses'
        response = answer_question(prompt)

        self.assertEqual(response, 'Apparel and Fashion')
