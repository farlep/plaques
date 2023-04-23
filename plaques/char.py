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

    def __eq__(self, other: object) -> bool:
        """Compare 2 CharCells using `==`.

        This compares how CharCells look _visually_, so None is equal
        to space for char attribute. Also if char is None or space, bold
        and italic attributes are not compared since they are not visible
        on a space.
        """
        if not isinstance(other, CharCell):
            return NotImplemented
        if self.bgcol != other.bgcol or self.ulined != other.ulined:
            return False
        if self.char in [" ", None] and other.char in [" ", None]:
            return True #characters are spaces
        if self.char != other.char or self.bold != other.bold or self.ulined \
            != other.ulined or self.color != other.color:
            return False
        return True

    def __ne__(self, other: object) -> bool:
        """Compare 2 CharCells using `!=`.

        Refer to __eq__() for details on the logic.
        """
        if not isinstance(other, CharCell):
            return NotImplemented
        return not self == other

    def __repr__(self) -> str:
        """Show attributes."""
        return (
            f"<CharCell: char:{self.char}, color:{self.color}, "
            f"bgcol:{self.bgcol}, bold:{self.bold}, underlined:{self.ulined},"
            f" italic:{self.italic}>"
        )

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

    def overlay(self, other: "CharCell") -> "CharCell":
        """Overlay `other` CharCell on this one and return a new CharCell.

        The new CharCell will have the attributes of `other`. If any of them
        is None, the attribute of `self` will be used.
        """
        return CharCell(
            char = other.char if other.char is not None else self.char,
            color = other.color if other.color is not None else self.color,
            bgcol = other.bgcol if other.bgcol is not None else self.bgcol,
            bold = other.bold if other.bold is not None else self.bold,
            ulined = other.ulined if other.ulined is not None else self.ulined,
            italic = other.italic if other.italic is not None else self.italic,
            )


class CharTable():
    """Representation of a 2-dimensional grid of CharCells.

    Attributes:
    __table: actual table containing CharCell objects.
    """

    NONECHARCELL = CharCell() #CharCell without attributes for method defaults

    def __init__(self, *,
        fill: CharCell = NONECHARCELL,
        h: int = 1,
        v: int = 1,
        ) -> None:
        """Initialize __table and fill it with copies of a given CharCell.

        `v` and `h` are vertical and horizontal dimensions of the CharTable.
        By default, `fill` is a CharCell with None for every attribute.
        """
        if type(fill) != CharCell or type(h) != int or type(v) != int:
            _msg = "Incorrect type for `fill`, `h` or `v` arguments."
            raise TypeError(_msg)
        self.__table: list[list[CharCell]] = \
            [[fill.copy() for _x in range(h)] for _y in range(v)]

    def getsize(self) -> tuple[int, int]:
        """Get horizontal and vertical size of the table."""
        return len(self.__table[0]), len(self.__table)

    def setcell(self, cell: CharCell, h: int, v: int) -> None:
        """Put a CharCell at a specified position on the grid."""
        self.__table[v][h] = cell.copy()

    def getcell(self, h: int, v: int) -> CharCell:
        """Get a copy of a CharCell at a specified position."""
        return self.__table[v][h].copy()

    def copy(self) -> "CharTable":
        """Return an identical CharTable."""
        result = CharTable()
        result.loadtable(table = self.__table)
        return result

    def loadtable(self, *,
        char: list[str], # TODO: other fields
        table: list[list[CharCell]] | None = None,
        ) -> None:
        """Write data

        Useful for loading raw ASCII art and other assets.
        XXX
        `table` is a 2-dimensional array of CharCells. This argument overrides
        all previous ones. The dimensions of __table will be changed if the
        array doesn't have the same dimensions.
        """
        if table:
            self.__table = table
            return
        #XXX

    def overlay(self, other: "CharTable") -> None:
        """Overlay another CharTable on this one.

        This method uses rules of CharCell.overlay() method, so if a CharCell
        from `other` has None for some of its attributes, the new cell will
        inherit these attributes from the original CharCell.
        """

    def render(self) -> list[str]:
        """Return an printable version of CharTable as a list of strings.

        The string are formatted using ansi_transition method of CharCell
        class.
        """

    def delta(self, other: "CharTable") -> dict[tuple[int, int], str]:
        """Calculate a diffence between 2 CharTables.

        This method accepts another CharTable of equal size and checks that
        every CharCell of `other` is the same as the CharCell of this one
        at the same position on the grid. When it finds ... XXX
        What needs to be printed ...XXX
        """
