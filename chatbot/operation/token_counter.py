import tiktoken


def count(model, prompt):
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(prompt)
    return len(tokens)


class TokenCounter:
    pass
