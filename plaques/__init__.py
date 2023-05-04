"""Plaques is a minimalistic TUI library."""

from .version import __version__
VERSION = __version__

from .char import Color, CharCell
globals().update(Color.__members__)
