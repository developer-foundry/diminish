import urwid
from tui.dashboard.dashboardForm import DashboardForm
from common.common import getEnvVar


if __name__ == '__main__':
    try:
        MODE = getEnvVar("MODE")
        ALGORITHM = getEnvVar("ALGORITHM")
        INPUT_FILE = getEnvVar("INPUT_FILE")
        TARGET_FILE = getEnvVar("TARGET_FILE")
        DEVICE = getEnvVar("DEVICE")
        SIZE = getEnvVar("SIZE", True)
        BT_MODE = getEnvVar("BT_MODE")
        WAIT_SIZE = getEnvVar("WAIT_SIZE", True)
        STEP_SIZE = getEnvVar("STEP_SIZE", True)

        dashboard = DashboardForm()
        urwid.MainLoop(dashboard.layout, palette=[('reversed', 'standout', '')]).run()

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
