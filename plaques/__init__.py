"""Plaques is a minimalistic TUI (Text User Interface) library."""

from .version import __version__
VERSION = __version__

from .base import Color, Pivot, CharCell, Plaque
globals().update(Color.__members__)
globals().update(Pivot.__members__)
