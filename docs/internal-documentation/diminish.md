# diminish package

## Subpackages


* diminish.algorithms package


    * Submodules


    * diminish.algorithms.crls module


    * diminish.algorithms.signal_processing module


    * Module contents


* diminish.monitoring package


    * Submodules


    * diminish.monitoring.monitor module


    * Module contents


* diminish.orchestrators package


    * Submodules


    * diminish.orchestrators.clientOrchestrator module


    * diminish.orchestrators.serverOrchestrator module


    * Module contents


* diminish.plotting package


    * Submodules


    * diminish.plotting.plot module


    * Module contents


* diminish.signals package


    * Submodules


    * diminish.signals.inputSignal module


    * diminish.signals.outputSignal module


    * diminish.signals.targetSignal module


    * Module contents


## Submodules

## diminish.diminish module


### class diminish.diminish.Diminish()
Bases: `object`

Main entry point for CLI and TUI to start ANC algorithm
Provides two primary mechanisms for ANC - prerecorded
and live (ANC)


#### None()

#### process_anc(device, targetFile, algorithm, btmode, waitSize, stepSize, size, tuiConnection)
Process live signal streams from the server and client


* **Parameters**

    
    * **device** (*String*) – A string representation of the sound device being used. ‘default’ is usually all that is needed


    * **targetFile** (*String*) – The name of the target signal data file. This is the desired signal the user should hear


    * **algorithm** (*str*) – The name of the algorithm used to perform ANC. Currently, only ‘crls’ is available.


    * **btmode** (*String*) – The role of the current process. Can be ‘server’ or ‘client’ and is set via ENV


    * **waitSize** (*int*) – The number of signal frames that should be received before the algorithm is ready


    * **stepSize** (*int*) – The number of signal frames or matrix rows used in the transfer of data to the server


    * **size** (*int*) – The number of frames to read from the target signal file


    * **tuiConnection** (*Boolean*) – A flag indicating if the server is running under the TUI interface or the CLIN interface



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### process_prerecorded(device, inputFile, targetFile, truncateSize, algorithm)
Process prerecorded WAV files


* **Parameters**

    
    * **device** (*String*) – A string representation of the sound device being used. ‘default’ is usually all that is needed


    * **inputFile** (*String*) – The name of the input signal data file. This represents the reference microphone


    * **targetFile** (*String*) – The name of the target signal data file. This is the desired signal the user should hear


    * **truncateSize** (*int*) – The number of frames to read from the WAV files


    * **algorithm** (*str*) – The name of the algorithm used to perform ANC. Currently, only ‘crls’ is available.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents
