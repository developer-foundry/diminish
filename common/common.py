"""
This script shares common functions and variables needed by the CLI and TUI scripts.
"""

import os
from pathlib import Path
import logging

from dotenv import load_dotenv
env_path = Path('./environment') / '.env'
load_dotenv(dotenv_path=env_path)

mu = 0.00001
"""
Utilized by the CRLS algorithm to determine the step of gradient descent algorithm
"""

guiRefreshTimer = 1.0
"""
This timer is used by the tui application to determine how long in between a screen refresh
"""


def get_project_root() -> Path:
    """
    Used to determine the root folder when the tui application spawns the cli process.

    Parameters
    ----------
    None

    Returns
    -------
    path : Path
        The path of the root module of diminish

    Raises
    ------
    None
    """
    return Path(__file__).parent.parent


def getEnvironmentVariables():
    """
    Returns all environment variables needed by the cli and tui

    Parameters
    ----------
    None

    Returns
    -------
    envVars : dictionary
        A dictionary of all the environment variables needed

    Raises
    ------
    None
    """
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
    """
    Returns a single environment variable

    Parameters
    ----------
    varName : str
        The name of the environment variable to retrieve
    isInteger : boolean
        Is the environment variable an integer and needs to be cast to an int

    Returns
    -------
    val : str
        Returns the value of the env var requested

    Raises
    ------
    None
    """

    if isInteger:
        return getInt(os.getenv(varName))
    else:
        return os.getenv(varName)


def getInt(val):
    """
    Converts a string to an integer with a null check

    Parameters
    ----------
    val : str
        The value to convert to an integer

    Returns
    -------
    val : int
        Returns converted str value to an int

    Raises
    ------
    None
    """
    if(val is None):
        val = 0
    else:
        val = int(val)
    return val
