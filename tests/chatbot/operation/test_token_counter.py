from unittest import TestCase

from chatbot.model.open_ai_model import OpenAiModel
from chatbot.operation.token_counter import count


class TestTokenCounter(TestCase):

    def test_count_success(self):
        model = OpenAiModel.get_default().model()
        prompt = 'You are a product categorizer and must only answer the name of the product category entered.'

        response = count(model, prompt)

        self.assertEqual(18, response)

    def test_count_fail(self):
        model = 'fake-gpt'
        prompt = 'You are a product categorizer and must only answer the name of the product category entered.'

        response = count(model, prompt)

        self.assertEqual(0, response)