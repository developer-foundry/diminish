# diminish.monitoring package

## Submodules

## diminish.monitoring.monitor module


### class diminish.monitoring.monitor.Monitor(buffers)
Bases: `object`

Monitor is utilized by Dimish to track the entire data set sound data for the
error microphone, reference microphone, target file, output speaker, and output error.

It will also send information to subscribers like the TUI application.


#### buffers()
A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.


* **Type**

    threading.Lock



#### dataClient()
Using the multiprocessing Listener object to push data to the TUI application


* **Type**

    Listener



#### process()
Used to retrieve system level monitoring information like CPU/Memory.


* **Type**

    psutil.Process



#### \__init__(buffers)

* **Parameters**

    **buffers** (*array*) – An array of buffers to monitor



#### close_connection()
Closes the connection to the TUI process


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### create_connection()
Creates a data connection to the TUI process in order to send data.
Uses the python multiprocessing library to communicate between processes.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### observe(bufferName, data)
Function utilized to track the anc data over time. Monitors the real time data from the algorithm and tracks it for
plotting or analysis


* **Parameters**

    
    * **bufferName** (*str*) – The name of the buffer that is passing data to the monitor (error, target, etc)


    * **data** (*np.array*) – An array of sound data to add to the buffer



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### plot_buffers(algorithm)
Plots all buffers that have been monitored using mathplotlib


* **Parameters**

    **algorithm** (*str*) – The name of the algorithm utilized in the run of the system.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### sendData()
Used to send data to the TUI application. This function runs on a timer that sends data
every <guiRefreshTimer>


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents

This module contains an implementation of a monitoring service for diminish.
