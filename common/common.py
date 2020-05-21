"""Common

This script shares common functions and variables needed by the CLI and TUI scripts.

This file can also be imported as a module and contains the following
functions and variables:
    * mu - utilized by the CRLS algorithm to determine the step of gradient 
        descent algorithm
    * guiRefreshTimer - this timer is used by the tui application to determine how 
        long in between a screen refresh
    * get_project_root - used to determine the root folder when the tui applications 
        spawns the cli process.
    * getEnvironmentVariables - returns all environment variables needed by
        the cli and tui
    * getEnvVar - returns a single environment variable
    * getInt - converts a str to int for env vars
"""

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
