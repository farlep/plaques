"""Plaques is a minimalistic TUI library."""

import logging
logging.basicConfig(filename = "plaques.log", level = logging.DEBUG)
try:
    from rich.traceback import install
    install(show_locals = True)
except ImportError:
    logging.info("rich.traceback is not available")

from .version import __version__
VERSION = __version__

from .elements import CharCell, render
