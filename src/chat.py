import lmstudio as _lmstudio

from rich import print as _rich_print

from . import _common


def ask(prompt: str) -> None:
    tokens = 0
    output = ""
    _rich_print("Mode: Chat")
    selected_model = _common.select_model()
    model = _lmstudio.llm(selected_model.model_key)

    for fragment in model.respond_stream(prompt):
        tokens += fragment.tokens_count
        output += _common.print_reasoning_fragment(fragment)

    _rich_print(flush=True)
    _rich_print("Tokens generated:", tokens, flush=True)

    _common.print_markdown(output)
