import bs4 as _bs4
import lmstudio as _lmstudio
import urllib.request as _urllib_request

from googlesearch import search as _gsearch
from rich import print as _rich_print

from . import _common


def _google_search(query: str, num_pages: int = 10) -> dict[str, str]:
    """
    Perform a google search with the given query text.
    The tool will open first 'num_pages' pages and extract all possible text from each web page.
    The consumer of this tool must make sure to use only parts of the text relevant for the query.
    If a web page cannot be read, it is not included in the return dict.

    Args:
        query (str): Text to search on the Google search engine.
        num_pages (int, optional): Number of pages to visit from the search results. Adjust as needed. Defaults to 10.

    Returns:
        dict[str, str]: A dictionary of web page links to their text content.
    """

    results = {}
    _common.print_text(
        f"[_google_search] Searching for '{query}' and opening {num_pages} pages."
    )
    for link in _gsearch(query, num_results=num_pages, unique=True):
        try:
            _common.print_text(f"[_google_search] Opening: {link}", end=" ")

            html = _urllib_request.urlopen(str(link)).read()
            soup = _bs4.BeautifulSoup(html, features="html.parser")

            text = soup.get_text(separator="\n", strip=True)
            text_split = [t.strip() for t in text.split("\n")]
            text_stripped = " ".join(text_split)

            results[str(link)] = text_stripped
        except Exception as e:
            _common.print_text(f"({str(e)}).", end=" ")

        finally:
            _common.print_text(f"...done.")

    return results


def _on_round_complete(message: _lmstudio.PredictionRoundResult):
    _common.print_markdown(message.content)


def do(prompt: str) -> None:
    tokens = 0
    output = ""
    _rich_print("Mode: Action")
    selected_model = _common.select_model()
    model = _lmstudio.llm(selected_model.model_key)

    chat = _lmstudio.Chat(
        """
        You are a task focused AI assistant. 
        Use the tools provided to answer the query. 
        The tools provided are well tested and always give the correct answer.
        """
    )
    chat.add_user_message(prompt)

    model.act(
        prompt,
        [_google_search],
        on_prediction_completed=_on_round_complete,
        on_prediction_fragment=_common.print_reasoning_fragment,
    )
