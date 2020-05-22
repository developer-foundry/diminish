# diminish.plotting package

## Submodules

## diminish.plotting.plot module

This script shares common functions and variables needed to plot signal data


### diminish.plotting.plot.get_dir(algorithm, mode)
Used to determine the plotting folder


* **Parameters**

    
    * **algorithm** (*String*) – The name of the current ANC algorithm running


    * **mode** (*String*) – The MODE (precorded or anc) the server is currently running



* **Returns**

    **path** – The path of the plots directory of diminish



* **Return type**

    Path



* **Raises**

    **None** – 



### diminish.plotting.plot.plot_vertical(algorithm, mode, inputSignal, targetSignal, outputSignal, errorSignal)
Plots the necessary signals for prerecorded mode


* **Parameters**

    
    * **algorithm** (*String*) – The name of the current ANC algorithm running


    * **mode** (*String*) – The MODE (precorded or anc) the server is currently running


    * **inputSignal** (*np.array*) – The reference microphone signal


    * **targetSignal** (*np.array*) – The desired target signal the user should hear


    * **outputSignal** (*np.array*) – The actual speaker output the user hears


    * **errorSignal** (*np.array*) – The difference between the output signal and the target signal



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



### diminish.plotting.plot.plot_vertical_buffers(algorithm, mode, buffers)
Plots the error, reference, output, target, and output error
signals for ANC mode


* **Parameters**

    
    * **algorithm** (*String*) – The name of the current ANC algorithm running


    * **mode** (*String*) – The MODE (precorded or anc) the server is currently running


    * **buffers** (*list*) – The list of buffers to plot



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents
