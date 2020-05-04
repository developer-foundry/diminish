import getopt
import wave
import sys
import argparse
import os

from soundwave import app

from dotenv import load_dotenv
load_dotenv()

def getInt(val):
    if(val is None):
        val = 0
    else:
        val = int(val)
    return val

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='POC for ACN testing')
        MODE = os.getenv("MODE")
        ALGORITHM = os.getenv("ALGORITHM")
        INPUT_FILE = os.getenv("INPUT_FILE")
        TARGET_FILE = os.getenv("TARGET_FILE")
        DEVICE = os.getenv("DEVICE")
        SIZE = getInt(os.getenv("SIZE"))
        BT_MODE = os.getenv("BT_MODE")
        WAIT_SIZE = getInt(os.getenv("WAIT_SIZE"))
        STEP_SIZE = getInt(os.getenv("STEP_SIZE"))

        if MODE == 'prerecorded':
            app.process_prerecorded(DEVICE, INPUT_FILE,
                                    TARGET_FILE, SIZE, ALGORITHM)
        elif MODE == 'live':
            app.process_live(parser, DEVICE,
                            TARGET_FILE, ALGORITHM)
        elif MODE == 'anc':
            app.process_anc(DEVICE,
                            TARGET_FILE, ALGORITHM, BT_MODE, WAIT_SIZE, STEP_SIZE)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
