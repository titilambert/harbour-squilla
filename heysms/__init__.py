#!/usr/bin/python3
__version__ = "0.7"
    
from heysms.application import Application
import sys

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
    app = Application(interval=3)
    app.start()
