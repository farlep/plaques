"""More advanced UI elements."""

from enum import Enum
from .base import CharCell, Plaque
from .base import Color, Pivot
globals().update(Color.__members__)
globals().update(Pivot.__members__)


class Text(Plaque):
    """Caption element."""

    DEFAULTS = Plaque.DEFAULTS | {
        "text": "",
        "align": Pivot,
    }


class Frame(Enum):
    """Possible border styles for Window."""

    NO_FRAME = {
           TOP_LEFT: " ",    TOP_CENTER: " ",    TOP_RIGHT: " ",
        CENTER_LEFT: " ",                     CENTER_RIGHT: " ",
        BOTTOM_LEFT: " ", BOTTOM_CENTER: " ", BOTTOM_RIGHT: " ",
        }
    THIN = {
           TOP_LEFT: "┌",    TOP_CENTER: "─",    TOP_RIGHT: "┐",
        CENTER_LEFT: "│",                     CENTER_RIGHT: "│",
        BOTTOM_LEFT: "└", BOTTOM_CENTER: "─", BOTTOM_RIGHT: "┘",
        }
    THICK = {
           TOP_LEFT: "┏",    TOP_CENTER: "━",    TOP_RIGHT: "┓",
        CENTER_LEFT: "┃",                     CENTER_RIGHT: "┃",
        BOTTOM_LEFT: "┗", BOTTOM_CENTER: "━", BOTTOM_RIGHT: "┛",
        }
    DOUBLE = {
           TOP_LEFT: "╔",    TOP_CENTER: "═",    TOP_RIGHT: "╗",
        CENTER_LEFT: "║",                     CENTER_RIGHT: "║",
        BOTTOM_LEFT: "╚", BOTTOM_CENTER: "═", BOTTOM_RIGHT: "╝",
        }
    SMOOTH = {
           TOP_LEFT: "╭",    TOP_CENTER: "─",    TOP_RIGHT: "╮",
        CENTER_LEFT: "│",                     CENTER_RIGHT: "│",
        BOTTOM_LEFT: "╰", BOTTOM_CENTER: "─", BOTTOM_RIGHT: "╯",
        }
    OUTER_HALF = {
           TOP_LEFT: "▛",    TOP_CENTER: "▀",    TOP_RIGHT: "▜",
        CENTER_LEFT: "▌",                     CENTER_RIGHT: "▐",
        BOTTOM_LEFT: "▙", BOTTOM_CENTER: "▄", BOTTOM_RIGHT: "▟",
        }
    INNER_HALF = {
           TOP_LEFT: "▗",    TOP_CENTER: "▄",    TOP_RIGHT: "▖",
        CENTER_LEFT: "▐",                     CENTER_RIGHT: "▌",
        BOTTOM_LEFT: "▝", BOTTOM_CENTER: "▀", BOTTOM_RIGHT: "▘",
        }
    ASCII = {
           TOP_LEFT: "+",    TOP_CENTER: "-",    TOP_RIGHT: "+",
        CENTER_LEFT: "|",                     CENTER_RIGHT: "|",
        BOTTOM_LEFT: "+", BOTTOM_CENTER: "-", BOTTOM_RIGHT: "+",
        }
    SLC_OUTER = { # Unicode 13+ required!
           TOP_LEFT: "🭽",    TOP_CENTER: "▔",    TOP_RIGHT: "🭾",
        CENTER_LEFT: "▏",                     CENTER_RIGHT: "▕",
        BOTTOM_LEFT: "🭼", BOTTOM_CENTER: "▁", BOTTOM_RIGHT: "🭿",
        }


class Window(Plaque):
    """Groups other UI elements in a frame."""

    DEFAULTS = Plaque.DEFAULTS | {
        "title": Text(
            pivot = TOP_LEFT,
            h_abs_pos = 1,
            v_abs_size = 1,
            h_rel_size = 1.0,
            h_abs_pos = -2,
            ),
        "status": Text(
            pivot = BOTTOM_LEFT,
            h_abs_pos = 1,
            v_rel_pos = 1.0,
            v_abs_pos = -1,
            v_abs_size = 1,
            h_rel_size = 1.0,
            h_abs_pos = -2,
            ),
        "frame": Frame.THIN,
    }

    BORDER = {
        "top": 1,
        "right": 1,
        "bottom": 1,
        "left": 1,
    }

