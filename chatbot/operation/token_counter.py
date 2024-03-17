import tiktoken


def count(model, prompt):
    try:
        encoder = tiktoken.encoding_for_model(model)
        tokens = encoder.encode(prompt)

        return len(tokens)
    except KeyError as error:
        print('TokenCounter unable to get a encoding for the model:', model)
        return 0


class TokenCounter:
    pass
