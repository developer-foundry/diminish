import getopt
import wave
import sys
import os

from common.common import getEnvVar
from soundwave import app


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

        if MODE == 'prerecorded':
            app.process_prerecorded(DEVICE, INPUT_FILE,
                                    TARGET_FILE, SIZE, ALGORITHM)
        elif MODE == 'live':
            app.process_anc(DEVICE,
                            TARGET_FILE, ALGORITHM, BT_MODE, WAIT_SIZE, STEP_SIZE)

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
