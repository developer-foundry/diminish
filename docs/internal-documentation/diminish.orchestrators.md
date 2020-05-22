# diminish.orchestrators package

## Submodules

## diminish.orchestrators.clientOrchestrator module


### class diminish.orchestrators.clientOrchestrator.ClientOrchestrator(device, waitSize, stepSize)
Bases: `object`

ClientOrchestrator is the primary class the coordinates
threads and their corresponding buffers. The client
is straightforward - it reads data from the reference
microphone and transfers that data via the network client
to the ANC server that does the algorithm processing.

Will run until the server stops or it is interrupted by
the user.


#### device()
A string representation of the sound device being used. ‘default’ is usually all that is needed


* **Type**

    String



#### referenceBuffer()
A FifoBuffer that will hold the reference microphone signal


* **Type**

    FifoBuffer



#### threads()
A list maintaing the necessary threads to support the orchestration and sending of data


* **Type**

    list



#### \__init__(device, waitSize, stepSize)

* **Parameters**

    
    * **device** (*String*) – A string representation of the sound device being used. ‘default’ is usually all that is needed


    * **waitSize** (*int*) – The number of signal frames that should be received before the algorithm is ready


    * **stepSize** (*int*) – The number of signal frames or matrix rows used in the transfer of data to the server



#### run()
Initializes buffers, threads, and orders the timing
of threads to ensure everything is ready to start
ANC processing

Runs until the server is killed or an exception is thrown


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## diminish.orchestrators.serverOrchestrator module


### class diminish.orchestrators.serverOrchestrator.ServerOrchestrator(device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection)
Bases: `object`

ServerOrchestrator is the primary class the coordinates
threads and their corresponding buffers. The server handles
a number of functions including

> 
> * Maintaining the error microphone buffer


> * Maintaining the output or speaker buffer


> * Receiving reference microphone data from the client


> * Reading in the target signal


> * Performing the ANC processing algorithm


> * Reporting data back to the Monitor

Will run until the server stops or it is interrupted by
the user. A user can pause the algorithm processing with
the p keybinding. The server will continue to run and
process data, it will just not perform the ANC algorithm


#### algorithm()
The name of the signal processing filter currently being used


* **Type**

    String



#### errorBuffer()
The buffer holding error microphone data


* **Type**

    FifoBuffer



#### outputBuffer()
The buffer holding speaker data


* **Type**

    FifoBuffer



#### outputErrorBuffer()
The buffer that holds the error difference between output and target signal


* **Type**

    FifoBuffer



#### referenceBuffer()
The buffer that holds reference microphone data from the client


* **Type**

    FifoBuffer



#### targetBuffer()
The buffer that holds the target signal data


* **Type**

    ContinuousBuffer



#### tuiConnection()
A flag indicating if the server is running under the TUI interface or the CLIN interface


* **Type**

    Boolean



#### waitCondition()
A threading lock to ensure the processing only starts when threads are ready


* **Type**

    Condition



#### networkThread()
The networking server that performs the receiving of the reference microphone data


* **Type**

    NetworkServer



#### threads()
A list maintaing the necessary threads to support the orchestration and sending of data


* **Type**

    list



#### monitor()
The data monitor that performs communication with TUI, plotting, and potentially database


* **Type**

    Monitor



#### paused()
A flag indicating if the ANC algorithm should be performed during the processing of output data


* **Type**

    Boolean



#### \__init__(device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection)

* **Parameters**

    
    * **device** (*String*) – A string representation of the sound device being used. ‘default’ is usually all that is needed


    * **algorithm** (*String*) – The name of the signal processing filter currently being used


    * **targetFile** (*String*) – The name of the target signal data file


    * **waitSize** (*int*) – The number of signal frames that should be received before the algorithm is ready


    * **stepSize** (*int*) – The number of signal frames or matrix rows used in the transfer of data to the server


    * **size** (*int*) – The number of frames to read from the target signal file


    * **tuiConnection** (*Boolean*) – A flag indicating if the server is running under the TUI interface or the CLIN interface



#### clear_buffers()
Resets the buffers to zero data


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### is_ready()
Determines if the buffers are ready to start
ANC processing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    Boolean



* **Raises**

    **None** – 



#### on_release(key)
Provides pause functionality for the TUI


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### pauseHandler(signum, frame)
Executed via the p keybinding to toggle the paused flag


* **Parameters**

    
    * **signum** (*int*) – A integer representing the interrupt signal


    * **frame** (*stack frame*) – The stack frame from the point in the program that was interrupted by the signal



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### run()
Initializes buffers, threads, and orders the timing
of threads to ensure everything is ready to start
ANC processing

Runs until the server is killed or an exception is thrown


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### run_algorithm()
Executed every iteration to pull data from the necessary
buffers and generate the output signal to be pushed to the
speaker. If the ANC algorithm is on, then this would be the
filtered signal, otherwise it just combines the target signal
and reference microphone signals. Note error signal is not
included in that case since the error microphone is just listening
for feedback reasons, not because the human ear is hearing that.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### stop()
Executed when the application is halted. Informs the
monitor to close and plot the results


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents
