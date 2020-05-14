import os
from pathlib import Path
import logging

from dotenv import load_dotenv
env_path = Path('./environment') / '.env'
load_dotenv(dotenv_path=env_path)

mu = 0.00001
guiRefreshTimer = 1.0

def get_project_root() -> Path:
    return Path(__file__).parent.parent

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
        'tuiConnection': getEnvVar("TUI_CONNECTION") == "True"
    }

def parseCliParameters(argv):
    return {
        'mode': argv[1],
        'algorithm': argv[2],
        'inputFile': argv[3],
        'targetFile': argv[4],
        'device': argv[5],
        'size': int(argv[6]),
        'role': argv[7],
        'waitSize': int(argv[8]),
        'stepSize': int(argv[9]),
        'tuiConnection': argv[10] == "True",
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