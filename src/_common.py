import lmstudio as _lmstudio
from rich import (
    print as _rich_print,
    markdown as _markdown,
    console as _console,
    style as _style,
)


def select_model() -> _lmstudio.AnyDownloadedModel:
    downloaded_models = _lmstudio.list_downloaded_models()

    if not downloaded_models:
        _rich_print(
            "No models found. Download some models from LMStudio and run this program again."
        )
        exit()

    _rich_print("Available models: ")
    for _i, _dm in enumerate(downloaded_models):
        _rich_print("\t", _i + 1, end=". ")
        _rich_print(_dm.info.path.split("/")[-1], _dm.type, sep="; ")

    option = input("Select a model for this task: ")

    try:
        assert int(option) > 0
        return downloaded_models[int(option) - 1]

    except (KeyError, ValueError, AssertionError):
        _rich_print("Invalid option.")
        exit()


def print_text(text: str, end: str = "\n"):
    if not text.strip():
        return

    console = _console.Console()
    style = _style.Style(
        italic=True,
        color="light_yellow3",
    )
    console.print(
        text, end=end, width=640, style=style, soft_wrap=True, new_line_start=True
    )


def print_markdown(content: str) -> None:
    if not content.strip():
        return

    console = _console.Console()
    markdown = _markdown.Markdown(content)

    console.print(new_line_start=True)

    style = _style.Style(
        color="pale_green3",
    )
    console.print(markdown, width=640, style=style, soft_wrap=True, new_line_start=True)


def print_reasoning_fragment(
    fragment: _lmstudio.LlmPredictionFragment, *args, **kwargs
) -> str:
    answer = ""

    if fragment.reasoning_type == "none":
        # Answer fragment.
        _rich_print(".", end="")
        answer = fragment.content
    else:
        # Reasoning / CoT fragment.
        _rich_print(fragment.content, end="")
        if fragment.reasoning_type == "reasoningEndTag":
            _rich_print()

    return answer
