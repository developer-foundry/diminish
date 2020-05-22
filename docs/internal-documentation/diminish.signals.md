# diminish.signals package

## Submodules

## diminish.signals.inputSignal module


### class diminish.signals.inputSignal.InputSignal(device, buffer, stepSize, threadName)
Bases: `threading.Thread`

Represents an input signal such as the error microphone
or reference microphone. Runs in its own thread to push
and pop data onto the buffer


#### buffer()
A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)


* **Type**

    FiFoBuffer



#### device()
A string representation of the sound device being used. ‘default’ is usually all that is needed


* **Type**

    String



#### stepSize()
The number of signal frames or matrix rows used in the transfer of data to the server


* **Type**

    int



#### stopped()
A flag indicating if the algorithm is running


* **Type**

    Boolean



#### \__init__(device, buffer, stepSize, threadName)

* **Parameters**

    
    * **device** (*String*) – A string representation of the sound device being used. ‘default’ is usually all that is needed


    * **buffer** (*FiFoBuffer*) – A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)


    * **stepSize** (*int*) – The number of signal frames or matrix rows used in the transfer of data to the server


    * **threadName** (*str*) – The name of the thread. Utilized for debugging.



#### listener(indata, frames, time, status)
Callback function for sounddevice InputStream
Is called periodically to place data from the
microphone and pushes data onto its respective
buffer. This is driven by PulseAudio under the
covers of sounddevice


* **Parameters**

    
    * **indata** (*numpy.ndarray*) – The numpy matrix that contains the microphone data with
    one column per channel


    * **frames** (*int*) – The number of rows for indata


    * **time** (*CData*) – Provides a CFFI structure with timestamps indicating the ADC capture time of the first sample in the input buffer


    * **status** (*CallbackFlags*) – Instance indicating whether input and/or output buffers have been inserted or will be dropped to overcome underflow or overflow conditions.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### run()
The primary thread function that initializes the
InputStream and continuously calls the Stream
listener to place data onto the buffer


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### stop()
Called when the algorithm is stopped and sets the stopped flag to False


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## diminish.signals.outputSignal module


### class diminish.signals.outputSignal.OutputSignal(device, buffer, stepSize, waitCondition, threadName)
Bases: `threading.Thread`

Represents an output signal such as the speaker
Runs in its own thread to push data onto the buffer


#### device()
A string representation of the sound device being used. ‘default’ is usually all that is needed


* **Type**

    String



#### buffer()
A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)


* **Type**

    FiFoBuffer



#### stepSize()
The number of signal frames or matrix rows used in the transfer of data to the server


* **Type**

    int



#### waitCondition()
The threading condition or lock that is used to signal when output can start


* **Type**

    Condition



#### stopped()
A flag indicating if the algorithm is running


* **Type**

    Boolean



#### \__init__(device, buffer, stepSize, waitCondition, threadName)

* **Parameters**

    
    * **device** (*String*) – A string representation of the sound device being used. ‘default’ is usually all that is needed


    * **buffer** (*FiFoBuffer*) – A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)


    * **stepSize** (*int*) – The number of signal frames or matrix rows used in the transfer of data to the server


    * **waitCondition** (*Condition*) – The threading condition or lock that is used to signal when output can start


    * **threadName** (*str*) – The name of the thread. Utilized for debugging.



#### listener(outdata, frames, time, status)
Callback function for sounddevice OutputStream
Is called periodically to place data from the
buffer into the speaker output This is driven
by PulseAudio under the covers of sounddevice


* **Parameters**

    
    * **outdata** (*numpy.ndarray*) – The numpy matrix that contains the microphone data with
    one column per channel


    * **frames** (*int*) – The number of rows for indata


    * **time** (*CData*) – Provides a CFFI structure with timestamps indicating the ADC capture time of the first sample in the input buffer


    * **status** (*CallbackFlags*) – Instance indicating whether input and/or output buffers have been inserted or will be dropped to overcome underflow or overflow conditions.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### run()
The primary thread function that initializes the
OutputStream and continuously calls the Stream
listener to place data from the buffer into the
Stream


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### stop()
Called when the algorithm is stopped and sets the stopped flag to False


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## diminish.signals.targetSignal module


### class diminish.signals.targetSignal.TargetSignal(targetFile, buffer, stepSize, size, threadName)
Bases: `threading.Thread`

Represents an output signal such as the speaker
Runs in its own thread to push data onto the buffer


#### buffer()
A thread-safe ContinuousBuffer that reads the underlying data stream (stereo sound)


* **Type**

    ContinuousBuffer



#### stepSize()
The number of signal frames or matrix rows used in the transfer of data to the server


* **Type**

    int



#### size()
The number of frames to read from the target signal file


* **Type**

    int



#### targetFile()
The name of the target signal data file


* **Type**

    String



#### targetSignal()
The sound data read in from targetFile


* **Type**

    numpy.ndarray



#### stopped()
A flag indicating if the algorithm is running


* **Type**

    Boolean



#### \__init__(targetFile, buffer, stepSize, size, threadName)

* **Parameters**

    
    * **targetFile** (*String*) – The name of the target signal data file


    * **buffer** (*ContinousBuffer*) – A thread-safe ContinuousBUffer that reads the underlying data stream (stereo sound)


    * **stepSize** (*int*) – The number of signal frames or matrix rows used in the transfer of data to the server


    * **size** (*int*) – The number of frames to read from the target signal file


    * **threadName** (*str*) – The name of the thread. Utilized for debugging.



#### run()
The primary thread function that initializes the
TargetStream. This is called once to load the buffer
and then the algorithm can use the ContinuousBuffer
to load “new” information into the algorithm


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### stop()
Called when the algorithm is stopped and sets the stopped flag to False


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents
