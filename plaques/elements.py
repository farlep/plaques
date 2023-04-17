"""Basic classes for plaques."""
import logging
from wcwidth import wcswidth

class CharCell():
    """Representation of a single character-cell in terminal.

    Attributes:
    char: a character to be printed (space if not specified);
    color, bgcol: character and background colors if specified;
    bold, u[nder]lined, italic: styles if specified.
    """

    COLORNUM = { #Correct color names for `color` and `bgcol` attributes
        "k": "0", #blacK
        "r": "1", #Red
        "g": "2", #Green
        "y": "3", #Yellow
        "b": "4", #Blue
        "m": "5", #Magenta
        "c": "6", #Cyan
        "w": "7", #White
        "n": "9", #Normal
        None: None,
        } #numbers correspond to ANSI SGR codes to use in ansi_transition()

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
        Raise TypeError if value is not of the correct type or None.
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
                if value in self.COLORNUM:
                    object.__setattr__(self, name, value)
                else:
                    _msg = "Incorrect color name"
                    raise ValueError(_msg)
            case "bold" | "ulined" | "italic":
                if type(value) != bool and value is not None:
                    _msg = "Incorrect type for style"
                    raise TypeError(_msg)
                object.__setattr__(self, name, value)

    def __eq__(self, other: "CharCell") -> bool:
        """Compare 2 CharCells using `==`.

        This compares how CharCells look _visually_, so None is equal
        to space for char attribute. Also if char is None or space, bold
        and italic attributes are not compared since they are not visible
        on a space.
        """
        _chars_are_spaces = False
        if self.bgcol != other.bgcol or self.ulined != other.ulined:
            return False
        if self.char in [" ", None] and other.char in [" ", None]:
            return True #characters are spaces
        if self.char != other.char or self.bold != other.bold or self.ulined \
            != other.ulined or self.color != other.color:
            return False
        return True

    def __ne__(self, other: "CharCell") -> bool:
        """Compare 2 CharCells using `!=`.

        Refer to __eq__() for details on the logic.
        """
        return not self == other

    def copy(self) -> "CharCell":
        """Return an identical CharCell."""
        return CharCell(
            char = self.char,
            color = self.color,
            bgcol = self.bgcol,
            bold = self.bold,
            ulined = self.ulined,
            italic = self.italic,
            )

    def ansi_transition(self, other: "CharCell") -> str:
        """Change style and color between `self` and `other`.

        Return a sequence of ANSI SGR escape codes necessary to transition
        from the colors and styles of CharCell `self` to the colors and
        styles of CharCell `other`. The codes are to be printed in between
        the characters form char attributes of the CharCells.

        If the CharCell colors and styles are the same, an empty string is
        returned.

        See en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
        for details.
        """
        _escseq = "\033["
        if self.color != other.color:
            _colorcode = other.color if other.color else "n"
            #return to normal color if the next char's color is unspecified
            _escseq = _escseq + "3" + str(self.COLORNUM[_colorcode]) + ";"
        if self.bgcol != other.bgcol:
            _bgcolcode = other.bgcol if other.bgcol else "n" #see above
            _escseq = _escseq + "4" + str(self.COLORNUM[_bgcolcode]) + ";"
        if self.bold != other.bold:
            _escseq = _escseq + "1;" if other.bold else _escseq + "21;"
        if self.ulined != other.ulined:
            _escseq = _escseq + "4;" if other.bold else _escseq + "24;"
        if self.italic != other.italic:
            _escseq = _escseq + "3;" if other.bold else _escseq + "23;"
        if _escseq == "\033[": #if no colors and styles were changed,
            return ""          #return an empty string
        return _escseq[:-1] + "m" #replace the trailing semicolon with SGR `m`


def render(chrlist: list[CharCell]) -> str:
    """Turn a list of CharCells into a printable string.

    Uses ANSI SGR codes in between characters where necessary.
    """
    pass
