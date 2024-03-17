from datetime import date
from decimal import Decimal
from enum import Enum


class OpenAiModel(Enum):
    GPT_4 = "gpt-4", 8192, date(2021, 9, 1), Decimal("0.03"), Decimal("0.06")
    GPT_4_0125_PREVIEW = "gpt-4-0125-preview", 128000, date(2023, 12, 1), Decimal("0.01"), Decimal("0.03")
    GPT_35_TURBO = "gpt-3.5-turbo", 4096, date(2021, 9, 1), Decimal("0.0030"), Decimal("0.0060")
    GPT_35_TURBO_0125 = "gpt-3.5-turbo-0125", 16385, date(2021, 9, 1), Decimal("0.0005"), Decimal("0.0015")

    def model(self):
        return self.value[0]

    def tokens(self):
        return self.value[1]

    def training_data(self):
        return self.value[2]

    def input_price(self):
        return self.value[3]

    def output_price(self):
        return self.value[4]

    @classmethod
    def most_updated(cls):
        return max(cls, key=lambda x: x.training_data())

    @classmethod
    def most_tokens(cls):
        return max(cls, key=lambda x: x.tokens())

    @classmethod
    def lowest_price(cls):
        return min(cls, key=lambda x: (x.input_price(), x.output_price()))

    @classmethod
    def get_default(cls):
        return cls.lowest_price()