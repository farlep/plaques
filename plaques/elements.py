"""Basic classes for plaques."""
import logging

class CharCell():
    """Representation of a single character-cell in terminal."""

    COLORNUMS = {
        "k": 0, #
        "r": 1, #
        "g": 2, #
        "y": 3, #
        "b": 4, #
        "m": 5, #
        "c": 6, #
        "w": 7, #
        "n": 9, #
        }

    def __init__(self, *,
            char: str | None = None,
            color: str | None = None,
            bgcol: str | None = None,
            bold: bool | None = None,
            ulined: bool | None = None,
            italic: bool | None = None,
            ) -> None:
        """Receive optional arguments."""
        self.char, self.color, self.bgcol, self.bold, self.ulined, \
            self.italic = char, color, bgcol, bold, ulined, italic
        msg = "Charcell made: " + str(char)
        logging.debug(msg)
