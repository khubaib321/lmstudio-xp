from src import chat as _chat, act as _act


if __name__ == "__main__":
    # _chat.ask("What is the meaning of life?")
    _act.do(
        """
        Perform a web search and compare the technical regulations of the 2026 Formula 1 season with the 2025 season.
        """
    )
