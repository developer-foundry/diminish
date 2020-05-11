import urwid
import logging

from tui.logging.tuiHandler import TuiHandler
from tui.controllers.dashboardController import DashboardController
from common.common import getEnvironmentVariables


def configureLogging():
    logger = logging.getLogger('TUI')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s {%(filename)s:%(lineno)d} (%(threadName)-9s) %(message)s')

    ch = TuiHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger, ch

if __name__ == '__main__':
    try:
        parameters = getEnvironmentVariables()
        logger, handler = configureLogging()
        dashboard = DashboardController(parameters, logger, handler)

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
