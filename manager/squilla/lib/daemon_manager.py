import os
import sys
import subprocess

from squilla.lib.logger import logger


SQUILLA_DAEMON = "/home/nemo/dev/squilla/daemon/run_squilla_daemon"


def start_stop_daemon(state):
    # Start daemon
    if state == True:
        logger.debug("Daemon starting")
        if daemon_is_running():
            logger.debug("Squilla daemon already started")
            return True

        os.system("/usr/bin/invoker --type=generic -s /usr/bin/harbour-squilla-daemon")
        logger.debug("Daemon started")
        return True

    # Stop daemon
    if state == False:
        logger.debug("Daemon stopping")
        command_line = ["/usr/bin/pkill -6 -f harbour-squilla-daemon"]
        proc = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
        try:
            outs, errs = proc.communicate(timeout=3)
        except TimeoutExpired:
            proc.kill()
            logger.debug("Error stopping Squilla daemon")
            return False

        if proc.returncode == 0:
            logger.debug("Squilla daemon stopped")
            return True
        else:
            logger.debug("Error stopping Squilla daemon")
            return False
    # Impossible...
    return False
        


def daemon_is_running():
    command_line = ['/usr/bin/pgrep -lf harbour-squilla-daemon']
    proc = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
    try:
        outs, errs = proc.communicate(timeout=3)
    except TimeoutExpired:
        proc.kill()
        logger.debug("Squilla daemon state unknown")
        return False
        
    if proc.returncode == 0:
        result = True
    else:
        result = False
    logger.debug("Squilla daemon running: %s" % result)

    return result
