# common package

## Submodules

## common.common module

Common

This script shares common functions and variables needed by the CLI and TUI scripts.

This file can also be imported as a module and contains the following
functions and variables:

> 
> * mu - utilized by the CRLS algorithm to determine the step of gradient 

>     descent algorithm


> * guiRefreshTimer - this timer is used by the tui application to determine how 

>     long in between a screen refresh


> * get_project_root - used to determine the root folder when the tui applications 

>     spawns the cli process.


> * getEnvironmentVariables - returns all environment variables needed by

>     the cli and tui


> * getEnvVar - returns a single environment variable


> * getInt - converts a str to int for env vars


### common.common.getEnvVar(varName, isInteger=False)

### common.common.getEnvironmentVariables()

### common.common.getInt(val)

### common.common.get_project_root()
## common.continuousBuffer module


### class common.continuousBuffer.ContinuousBuffer(name, stepSize, numChannels=2)
Bases: `object`

ContinuousBuffer is a buffer that acts as a rolling buffer
Items that are popped are simply moved to the end of the buffer
Typically a ContinuousBuffer is initialized with its entire data set
up front rather than continuously pushing data onto the buffer.

ContinuousBuffer is utilized by diminish to handle the Target File buffer.

lock

    A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.

buffer

    A numpy array that holds the underlying data stream (stereo sound)

maxSize

    The maximum size of the buffer.

currentLocation

    Tracks the current location that the buffer is at. Used by the pop method to determine the starting location of the next chunk.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.

name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

subscriber

    Each buffer can have one subscriber that will be notified upon a pop.

subscribe(observer: Callable)

    Subscribes an observer to be notified upon a pop of the buffer.

push(data: np.array)

    Adds data to the end of the buffer

pop()

    Returns a chunk of data from ‘currentLocation’ to ‘currentLocation + stepSize’.
    Moves that chunk to the end of the buffer

size()

    Returns the size of the buffer


#### \__init__(name, stepSize, numChannels=2)
name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.


#### pop()
Returns a chunk of data from ‘currentLocation’ to ‘currentLocation + stepSize’.
Moves that chunk to the end of the buffer

None

data

    A numpy array representing a chunk of the buffer.

None


#### push(data)
Adds data to the end of the buffer

data

    The numpy array data to add to the end of the buffer

None

None


#### size()
Returns the size of the buffer

None

size

    Size of the buffer

None


#### subscribe(observer: Callable)
Subscribes an observer to be notified upon a pop of the buffer.

observer

    The observer to attach to the subscriber for notification of a pop.

None

None

## common.fifoBuffer module


### class common.fifoBuffer.FifoBuffer(name, waitSize, stepSize, numChannels=2)
Bases: `object`

FifoBuffer is a buffer that acts as a Queue
Items that are popped are deleted from the buffer
Typically a FifoBuffer is continuously pushed and popped from
Locking is required as the pushing and popping occurs from different
threads.

FifoBuffer is utilized by diminish to handle the Input Signal
and Output Signals.

lock

    A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.

buffer

    A numpy array that holds the underlying data stream (stereo sound)

waitSize

    The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
    Provides a mechanism to capture data while the algorithm is syncronizing.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.

name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

subscriber

    Each buffer can have one subscriber that will be notified upon a pop.

subscribe(observer: Callable)

    Subscribes an observer to be notified upon a pop of the buffer.

push(data: np.array)

    Adds data to the end of the buffer

pop()

    Returns a chunk of data from the front of the buffer to ‘stepSize’.
    Deletes the chunk from the buffer.

is_ready()

    Determines whether or not the buffer is ready for processing

size()

    Returns the size of the buffer

clear()

    Zeros out the entire buffer.


#### \__init__(name, waitSize, stepSize, numChannels=2)
name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

waitSize

    The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
    Provides a mechanism to capture data while the algorithm is syncronizing.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.


#### clear()
Zeros out the entire buffer.

None

None

None


#### is_ready()
Determines whether or not the buffer is ready for processing

None

isReady

    A boolean representing whether or not the buffer is ready for processing in the Diminish algorithm

None


#### pop()
Returns a chunk of data from the front of the buffer to ‘stepSize’.
Deletes the chunk from the buffer.

None

data

    A numpy array representing a chunk of the buffer.

None


#### push(data)
Adds data to the end of the buffer

data

    The numpy array data to add to the end of the buffer

None

None


#### size()
Returns the size of the buffer

None

size

    Size of the buffer

None


#### subscribe(observer: Callable)
Subscribes an observer to be notified upon a pop of the buffer.

observer

    The observer to attach to the subscriber for notification of a pop.

None

None

## Module contents

Common

This module is for code that is common between the CLI, TUI, and Diminish modules.
Common functions and configuration can be placed in this module.
