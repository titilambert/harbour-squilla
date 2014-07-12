#!/usr/bin/python3

__version__ = "0.7"
    
import sys
import os
import grp

embedded_libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  '../embedded_libs/')
sys.path.append(embedded_libs_path)

from squilla.application import Application
from squilla.lib.logger import logger


try:
    import pyotherside
except ImportError:
    import sys
    # Allow testing Python backend alone.
    print("PyOtherSide not found, continuing anyway!", file=sys.stderr)

    class pyotherside:
        def atexit(*args): pass
        def send(*args): pass
    sys.modules["pyotherside"] = pyotherside()


def main():
    """Initialize application."""
    global app
    try:
        os.setgid(grp.getgrnam("privileged").gr_gid)
    except Exception as e:
        logger.debug(str(e))
    app = Application(interval=3)
    app.start()
