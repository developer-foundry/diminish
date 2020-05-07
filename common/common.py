import os
from pathlib import Path
import logging

from dotenv import load_dotenv
env_path = Path('./environment') / '.env'
load_dotenv(dotenv_path=env_path)

mu = 0.00001

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(levelname)s {%(filename)s:%(lineno)d} (%(threadName)-9s) %(message)s',)

def getEnvironmentVariables():
    return {
        'mode': getEnvVar("MODE"),
        'algorithm': getEnvVar("ALGORITHM"),
        'inputFile': getEnvVar("INPUT_FILE"),
        'targetFile': getEnvVar("TARGET_FILE"),
        'device': getEnvVar("DEVICE"),
        'size': getEnvVar("SIZE", True),
        'role': getEnvVar("ROLE"),
        'waitSize': getEnvVar("WAIT_SIZE", True),
        'stepSize': getEnvVar("STEP_SIZE", True),
    }

def getEnvVar(varName, isInteger=False):
    if isInteger:
        return getInt(os.getenv(varName))
    else:
        return os.getenv(varName)

def getInt(val):
    if(val is None):
        val = 0
    else:
        val = int(val)
    return val