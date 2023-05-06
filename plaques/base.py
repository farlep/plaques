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


class CharCell:
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


Class Pivot(Enum):
    """Defines several useful points on a Plaque (clockwise).

    1---2---3
    |       |
    |       |
    8   0   4
    |       |
    |       |
    7---6---5
    """

    CENTER_CENTER = 0
    TOP_LEFT = 1
    TOP_CENTER = 2
    TOP_RIGHT = 3
    CENTER_RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM_CENTER = 6
    BOTTOM_LEFT = 7
    CENTER_LEFT = 8

globals().update(Pivot.__members__)


class Plaque:
    """Plaque is the central concept of the module.

    It is a rectangular area defined by absolute (`abs`) and relative (`rel`)
    sizes.
    A plaque knows where it is by keeping position (`pos`) values, that
    can be relative and absolute too.
    It also has `pivot` attribute (Pivot enum), defining its origin point
    by which it is attached to its position.
    Sizes and positions start with `h` or `v`, for Horizontal or Vertical

    Absolute `pos`s and `size`s are integers representing exact number of
    terminal cells:
    `v_abs_pos = 2` means this Plaque must be positioned 2 rows below the top
    side of the "parent", the Plaque that contains it (the exact position
    depends on the `pivot` attribute).

    Relative `pos`s and `size`s are floats representing the values comparing
    to the size of the "parent":
    `h_rel_size = 0.5` means this Plaque will have the width (Horizontal size)
    of 50% of the Plaque that contains it.

    In the real position and size calculations absolute and relative
    attributes get combined:
    `v_rel_pos = 0.3`
    `v_abs_pos = -2`
    In this case, the origin point of the Plaque will be put at 30% of the
    parent's height minus 2 rows. Fore example, if the parent Plaque is
    30 rows high:
    30 * 0.3 + (-2) = 7
    Origin point will be placed on the 7th row.

    Plaque is the base class for any other end user-facing element in the
    module.
    """

    DEFAULTS = {
        "v_abs_pos": 0,
        "h_abs_pos": 0,
        "v_rel_pos": 0.0,
        "h_rel_pos": 0.0,
        "v_abs_size": 1,
        "h_abs_size": 1,
        "v_rel_size": 0.0,
        "h_rel_size": 0.0,
        "pivot": CENTER_CENTER,
        "h_move_to_fit": True,
        "v_move_to_fit": True,
        "h_resize_to_fit": True,
        "v_resize_to_fit": True,
        "fill": None,
    }

    BORDER_SIZE = {
        "top": 0,
        "right": 0,
        "bottom": 0,
        "left": 0,
    }

    def __init__(self, **kwargs) -> None:
        """Set provided attributes or the default ones."""
        kwargs = self.DEFAULTS | kwargs
        for _key, _value in kwargs.items():
            self.__setattr__(_key, _value)
        self.content = []

    def __setattr__(self, name: str, value: bool | str | Color) -> None:
        """Validate attributes.

        """

    def render(self, h_avail: int, v_avail: int) -> \
        list[list[CharCell]], int, int:
        """TODO description.

        Returns ...
        """
        h_real_pos, h_real_size, trim_left, trim_right = self.__calc(
            h_avail,
            self.pivot,
            self.h_move_to_fit,
            self.h_resize_to_fit,
            self.h_rel_size,
            self.h_abs_size,
            self.h_rel_pos,
            self.h_abs_pos,
            )
        v_real_pos, v_real_size, trim_top, trim_bottom = self.__calc(
            v_avail,
            self.pivot,
            self.v_move_to_fit,
            self.v_resize_to_fit,
            self.v_rel_size,
            self.v_abs_size,
            self.v_rel_pos,
            self.v_abs_pos,
            )
        char_table = self.__get_char_table(h_real_size, v_real_size)
        for _element in self.content:
            elem_char_table, elem_h_pos, elem_v_pos = _element.render(
                h_real_size - BORDER_SIZE["left"] - BORDER_SIZE["right"],
                v_real_size - BORDER_SIZE["top"] - BORDER_SIZE["bottom"],
                )
            self.__overlay_tables(char_table, elem_char_table,
                elem_h_pos, elem_v_pos)
        # TODO: trim the table
        return char_table, h_real_pos, v_real_pos

    @staticmethod
    def __calc(
        avail: int,
        pivot: Pivot,
        move_to_fit: bool,
        resize_to_fit: bool,
        rel_size: float,
        abs_size: int,
        rel_pos: float,
        abs_pos: int,
        ) -> int, int, int, int:
        """Calculate ...

        Returns ...
        """

    @staticmethod
    def __overlay_tables(
        table1: list[list[Charcell]],
        table2: list[list[Charcell]],
        h_pos: int,
        v_pos: int,
        ) -> None
        """Overlay one CharCell table on another at specified coordinates.

        For every CharCell, its `overlay()` method is used.
        """
