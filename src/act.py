import bs4 as _bs4
import lmstudio as _lmstudio
import urllib.request as _urllib_request

from googlesearch import search as _gsearch
from rich import print as _rich_print

from . import _common


def _google_search(query: str) -> dict[str, str]:
    """
    Perform a google search with the given query and return text on each page.

    Args:
        query (str): Text to search on the Google search engine.

    Returns:
        dict[str, str]: A dictionary of web page links to their text content.
    """

    num_pages = 7
    _common.print_text(
        f"[_google_search] Searching for '{query}' and opening first {num_pages} results.",
        new_line=True,
    )
    results: dict[str, str] = {}

    for link in _gsearch(query, num_results=num_pages, unique=True):
        _common.print_text(f"[_google_search] Reading: {link}", end=" ")

        try:
            html = _urllib_request.urlopen(str(link)).read()
            soup = _bs4.BeautifulSoup(html, features="html.parser")

            text = soup.get_text(separator="\n", strip=True)
            text_split = [t.strip() for t in text.split("\n")]

            results[str(link)] = " ".join(text_split)
        except Exception as e:
            results[str(link)] = ""
            _common.print_text(f"({str(e)}).", end=" ")

        finally:
            _common.print_text(f"...done.")

    return results


_TOOL_DEFS = [
    _lmstudio.ToolFunctionDef(
        name="Google Search",
        description="""
            Perform a google search with the given query.
            The tool will open first 'num_pages' pages and extract all text from each web page.
            The consumer of this tool must make sure to use only parts of the web page text that are relevant for the query.
        """,
        parameters={
            "query": str,
        },
        implementation=_google_search,
    )
]


def _on_round_complete(message: _lmstudio.PredictionRoundResult):
    _common.print_markdown(message.content)


def _do(*, prompt: str, chat: _lmstudio.Chat, model: _lmstudio.LLM) -> None:
    chat.add_user_message(prompt)

    model.act(
        chat,
        _TOOL_DEFS,
        on_message=chat.append,
        on_prediction_completed=_on_round_complete,
        on_prediction_fragment=_common.print_reasoning_fragment,
    )


def do(prompt: str) -> None:
    _rich_print("Mode: Action")
    selected_model = _common.select_model()
    model = _lmstudio.llm(selected_model.model_key)

    try:
        chat = _lmstudio.Chat(
            """
            Only respond in English language.
            You are a task focused AI assistant. 
            Use the tools provided to answer the query. 
            The tools provided are well tested and always provide correct answers.
            At the end of each response, ask specific follow up questions to continue the conversion.
            """
        )

        while prompt != "exit":
            _do(prompt=prompt, chat=chat, model=model)
            prompt = input("You (continue chat): ")

    finally:
        model.unload()
