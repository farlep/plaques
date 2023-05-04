"""Basic classes for plaques."""

from enum import Enum
from wcwidth import wcswidth


class Color(Enum):
    """Basic colors for CharCell."""

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
        """Set provided attributes or the default ones."""
        kwargs = self.DEFAULTS | kwargs
        for _key, _value in kwargs.items():
            self.__setattr__(_key, _value)

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
        """Copy all the attributes of another CharCell, except colors.

        Colors will remain the same if they have the value of TRANSPARENT.
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
