import urwid
from tui.dashboard.dashboardForm import DashboardForm
from common.common import getEnvironmentVariables


if __name__ == '__main__':
    try:
        parameters = getEnvironmentVariables()
        dashboard = DashboardForm(parameters)
        dashboard.run()

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
