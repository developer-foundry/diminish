# common package

## Submodules

## common.common module

This script shares common functions and variables needed by the CLI and TUI scripts.


### common.common.getEnvVar(varName, isInteger=False)
Returns a single environment variable


* **Parameters**

    
    * **varName** (*str*) – The name of the environment variable to retrieve


    * **isInteger** (*boolean*) – Is the environment variable an integer and needs to be cast to an int



* **Returns**

    **val** – Returns the value of the env var requested



* **Return type**

    str



* **Raises**

    **None** – 



### common.common.getEnvironmentVariables()
Returns all environment variables needed by the cli and tui


* **Parameters**

    **None** – 



* **Returns**

    **envVars** – A dictionary of all the environment variables needed



* **Return type**

    dictionary



* **Raises**

    **None** – 



### common.common.getInt(val)
Converts a string to an integer with a null check


* **Parameters**

    **val** (*str*) – The value to convert to an integer



* **Returns**

    **val** – Returns converted str value to an int



* **Return type**

    int



* **Raises**

    **None** – 



### common.common.get_project_root()
Used to determine the root folder when the tui application spawns the cli process.


* **Parameters**

    **None** – 



* **Returns**

    **path** – The path of the root module of diminish



* **Return type**

    Path



* **Raises**

    **None** – 



### common.common.guiRefreshTimer( = 1.0)
This timer is used by the tui application to determine how long in between a screen refresh


### common.common.mu( = 1e-05)
Utilized by the CRLS algorithm to determine the step of gradient descent algorithm

## common.continuousBuffer module


### class common.continuousBuffer.ContinuousBuffer(name, stepSize, numChannels=2)
Bases: `object`

ContinuousBuffer is a buffer that acts as a rolling buffer
Items that are popped are simply moved to the end of the buffer
Typically a ContinuousBuffer is initialized with its entire data set
up front rather than continuously pushing data onto the buffer.

ContinuousBuffer is utilized by diminish to handle the Target File buffer.


#### lock()
A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.


* **Type**

    threading.Lock



#### buffer()
A numpy array that holds the underlying data stream (stereo sound)


* **Type**

    np.array



#### maxSize()
The maximum size of the buffer.


* **Type**

    int



#### currentLocation()
Tracks the current location that the buffer is at. Used by the pop method to determine the starting location of the next chunk.


* **Type**

    int



#### stepSize()
The amount of data to pop off the buffer.


* **Type**

    int



#### numChannels()
The number of channels of the sound file in question. Likely will always be 2.


* **Type**

    int



#### name()
The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.


* **Type**

    str



#### subscriber()
Each buffer can have one subscriber that will be notified upon a pop.


* **Type**

    Callable



#### \__init__(name, stepSize, numChannels=2)

* **Parameters**

    
    * **name** (*str*) – The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.


    * **stepSize** (*int*) – The amount of data to pop off the buffer.


    * **numChannels** (*int*) – The number of channels of the sound file in question. Likely will always be 2.



#### pop()
Returns a chunk of data from ‘currentLocation’ to ‘currentLocation + stepSize’.
Moves that chunk to the end of the buffer


* **Parameters**

    **None** – 



* **Returns**

    **data** – A numpy array representing a chunk of the buffer.



* **Return type**

    np.array



* **Raises**

    **None** – 



#### push(data)
Adds data to the end of the buffer


* **Parameters**

    **data** (*np.array*) – The numpy array data to add to the end of the buffer



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### size()
Returns the size of the buffer


* **Parameters**

    **None** – 



* **Returns**

    **size** – Size of the buffer



* **Return type**

    int



* **Raises**

    **None** – 



#### subscribe(observer: Callable)
Subscribes an observer to be notified upon a pop of the buffer.


* **Parameters**

    **observer** (*Callable*) – The observer to attach to the subscriber for notification of a pop.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


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


#### lock()
A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.


* **Type**

    threading.Lock



#### buffer()
A numpy array that holds the underlying data stream (stereo sound)


* **Type**

    np.array



#### waitSize()
The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
Provides a mechanism to capture data while the algorithm is syncronizing.


* **Type**

    int



#### stepSize()
The amount of data to pop off the buffer.


* **Type**

    int



#### numChannels()
The number of channels of the sound file in question. Likely will always be 2.


* **Type**

    int



#### name()
The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.


* **Type**

    str



#### subscriber()
Each buffer can have one subscriber that will be notified upon a pop.


* **Type**

    Callable



#### \__init__(name, waitSize, stepSize, numChannels=2)

* **Parameters**

    
    * **name** (*str*) – The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.


    * **waitSize** (*int*) – The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
    Provides a mechanism to capture data while the algorithm is syncronizing.


    * **stepSize** (*int*) – The amount of data to pop off the buffer.


    * **numChannels** (*int*) – The number of channels of the sound file in question. Likely will always be 2.



#### clear()
Zeros out the entire buffer.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### is_ready()
Determines whether or not the buffer is ready for processing


* **Parameters**

    **None** – 



* **Returns**

    **isReady** – A boolean representing whether or not the buffer is ready for processing in the Diminish algorithm



* **Return type**

    boolean



* **Raises**

    **None** – 



#### pop()
Returns a chunk of data from the front of the buffer to ‘stepSize’.
Deletes the chunk from the buffer.


* **Parameters**

    **None** – 



* **Returns**

    **data** – A numpy array representing a chunk of the buffer.



* **Return type**

    np.array



* **Raises**

    **None** – 



#### push(data)
Adds data to the end of the buffer


* **Parameters**

    **data** (*np.array*) – The numpy array data to add to the end of the buffer



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### size()
Returns the size of the buffer


* **Parameters**

    **None** – 



* **Returns**

    **size** – Size of the buffer



* **Return type**

    int



* **Raises**

    **None** – 



#### subscribe(observer: Callable)
Subscribes an observer to be notified upon a pop of the buffer.


* **Parameters**

    **observer** (*Callable*) – The observer to attach to the subscriber for notification of a pop.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents

Common

This module is for code that is common between the CLI, TUI, and Diminish modules.
Common functions and configuration can be placed in this module.
