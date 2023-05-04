"""Basic classes for plaques."""

from enum import Enum
from wcwidth import wcswidth


class Color(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    TRANSPARENT = 8
    NORMAL = 9

globals().update(Color.__members__)


class CharCell():
    """Representation of a single character-cell in terminal.

    Attributes:
    char: a character to be printed;
    color, bgcol: character and background colors (Color enum);
    bold, u[nder]lined, italic: styles.
    """

    DEFAULTS = {
        "char": " ",
        "color": NORMAL,
        "bgcol": NORMAL,
        "bold": False,
        "ulined": False,
        "italic": False,
    }

    def __init__(self, **kwargs) -> None:
        """Receive optional arguments."""
        for _key, _default in self.DEFAULTS.items():
            if _key in kwargs.keys():
                self.__setattr__(_key, kwargs[_key])
            else:
                self.__setattr__(_key, _default)

    def __setattr__(self, name: str, value: bool | str | Color) -> None:
        """Validate attributes.

        Raise ValueError if character is not 1 cell-wide.
        """
        if name == "char":
            if wcswidth(value) == 1:
                object.__setattr__(self, name, value)
            else:
                _msg = "CharCell.char must have printable length of 1"
                raise ValueError(_msg)
        elif name in ["color", "bgcol", "bold", "ulined", "italic"]:
            object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        """Compare 2 CharCells using `==`.

        This compares how CharCells look _visually_, so if char is space, bold
        and italic attributes are not compared since they are not visible.
        """
        if not isinstance(other, CharCell):
            return NotImplemented
        if self.bgcol != other.bgcol or self.ulined != other.ulined:
            return False
        if self.char == " " and other.char == " ":
            return True #characters are spaces, no need to check further
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

    def overlay(self, other: "CharCell") -> "CharCell":
        """Overlay `other` CharCell on this one and return a new CharCell.

        The new CharCell will have the attributes of `other`. If any of the
        colors is TRANSPARENT, the color of `self` will be used instead.
        """
        return CharCell(
            char = other.char,
            color = (other.color if other.color is not TRANSPARENT
                else self.color),
            bgcol = (other.bgcol if other.bgcol is not TRANSPARENT
                else self.bgcol),
            bold = other.bold,
            ulined = other.ulined,
            italic = other.italic,
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
