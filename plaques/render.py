"""Functions that depend on terminal output implementation."""

from os import get_terminal_size
from .base import CharCell, Plaque, NORMAL, TRANSPARENT


def __ansi_transition(cell1: CharCell, cell2: CharCell) -> str:
    """Change style and color between 2 CharCells.

    Return a sequence of ANSI SGR escape codes necessary to transition
    from the colors and styles of CharCell `cell1` to the colors and
    styles of CharCell `cell2`. The codes are to be printed in between
    the characters form char attributes of the CharCells.

    If the CharCell colors and styles are the same, an empty string is
    returned.

    See en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
    for details.
    """
    _escseq = "\033["
    if cell1.color != cell2.color:
        _color = (cell2.color if cell2.color != TRANSPARENT else NORMAL)
        #return to normal color if the next char's color is transparent
        _escseq = _escseq + "3" + str(_color.value) + ";"
    if cell1.bgcol != cell2.bgcol:
        _bgcol = (cell2.bgcol if cell2.bgcol != TRANSPARENT else NORMAL)
        _escseq = _escseq + "4" + str(_bgcol.value) + ";"
    if cell1.bold != cell2.bold:
        _escseq = _escseq + "1;" if cell2.bold else _escseq + "21;"
    if cell1.ulined != cell2.ulined:
        _escseq = _escseq + "4;" if cell2.ulined else _escseq + "24;"
    if cell1.italic != cell2.italic:
        _escseq = _escseq + "3;" if cell2.italic else _escseq + "23;"
    if _escseq == "\033[": #if no colors and styles were changed,
        return ""          #return an empty string
    return _escseq[:-1] + "m" #replace the trailing semicolon with SGR `m`


def __ansi_char_line(chars: list[CharCell]) -> str:
    """Get a printable representation of a list of CharCells."""
    chars = [CharCell()] + chars
    return "".join(
        [__ansi_transition(chars[i], chars[i+1]) + chars[i+1].char
            for i in range(len(chars) - 1)
            ]
        ) + "\033[0m" #SGR normal


def print_plaque(plaque: Plaque) -> None:
    """Print a plaque to console without using alt screen."""
    h_avail, v_avail = get_terminal_size()
    lines, _, _ = plaque.render(h_avail, v_avail)
    if lines == []:
        return
    for _line in lines:
        print(__ansi_char_line(_line))
