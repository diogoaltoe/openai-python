from unittest import TestCase

from chatbot.operation.assistant_use_case import answer_question


class TestAssistantUseCase(TestCase):

    def test_answer_question_with_retrieval_success(self):
        prompt = 'List one Home Products made with bamboo?'
        response, thread_id = answer_question(prompt, None)

        print(response)

        self.assertTrue(str(response).find('bamboo toothbrush') != -1)

    def test_answer_question_with_function_success(self):
        prompt = 'Is the COUPON_ECO Coupon valid?'
        response, thread_id = answer_question(prompt, None)

        print(response)

        self.assertTrue(str(response).find('COUPON_ECO coupon is valid') != -1)
