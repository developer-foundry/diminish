import urwid
from tui.controllers.dashboardController import DashboardController
from common.common import getEnvironmentVariables


if __name__ == '__main__':
    try:
        parameters = getEnvironmentVariables()
        dashboard = DashboardController(parameters)
        dashboard.run()

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
