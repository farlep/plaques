"""Basic classes for plaques."""
import logging
from wcwidth import wcswidth

class CharCell():
    """Representation of a single character-cell in terminal."""

    COLORNUMS = { #Correct color names for `color` and `bgcol` attributes
        "k": 0, #blacK
        "r": 1, #Red
        "g": 2, #Green
        "y": 3, #Yellow
        "b": 4, #Blue
        "m": 5, #Magenta
        "c": 6, #Cyan
        "w": 7, #White
        "n": 9, #Normal
        None: None,
        } #numbers correspond to ANSI SGR codes to use in XXX...

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

    def __setattr__(self, name: str, value: str | bool | None) -> None:
        """Validate attributes.

        Assign `value` to attribute `name` if validation is successful.
        Raise TypeError if value is not of the correct type or None
        Raise ValueError if character is not 1 cell-wide
        or color name is wrong.
        """
        match name:
            case "char":
                if type(value) != str and value is not None:
                    _msg = "Incorrect type for character"
                    raise TypeError(_msg)
                if value is None:
                    object.__setattr__(self, name, value)
                    return
                if wcswidth(value) == 1:
                    object.__setattr__(self, name, value)
                else:
                    _msg = "CharCell.char must have printable length of 1"
                    raise ValueError(_msg)
            case "color" | "bgcol":
                if type(value) != str and value is not None:
                    _msg = "Incorrect type for color"
                    raise TypeError(_msg)
                if value in self.COLORNUMS:
                    object.__setattr__(self, name, value)
                else:
                    _msg = "Incorrect color name"
                    raise ValueError(_msg)
            case "bold" | "ulined" | "italic":
                if type(value) != bool and value is not None:
                    _msg = "Incorrect type for style"
                    raise TypeError(_msg)
                object.__setattr__(self, name, value)


def render(chrlist: list[CharCell]) -> str:
    """Turn a list of CharCells into a printable string.

    Uses ANSI SGR codes in between characters where necessary.
    """
    pass
