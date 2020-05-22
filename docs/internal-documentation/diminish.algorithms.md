# diminish.algorithms package

## Submodules

## diminish.algorithms.crls module


### diminish.algorithms.crls.crls(inputSignal, targetSignal, mu, n)
RLS signal processing algorithm. The python code will call a C implementation of RLS


* **Parameters**

    
    * **inputSignal** (*np.array*) – Input matrix (2-dimensional array). Rows are samples. Columns are input arrays.


    * **targetSignal** (*np.array*) – Target matrix (2-dimensional array). Rows are samples. Columns are input arrays.


    * **mu** (*float*) – It is introduced to give exponentially less weight to older error samples. It is usually chosen between 0.98 and 1.


    * **n** (*int*) – The number of samples in the dataset.



* **Returns**

    
    * **y** (*np.array*) – An array of data representing the output signal


    * **e** (*np.array*) – Ar array of data representing the error singal




* **Raises**

    **None** – 


## diminish.algorithms.signal_processing module


### diminish.algorithms.signal_processing.process_signal(inputSignal, targetSignal, algorithm)
Processes input signal to try and achieve an output that is closest to target signal by running an ANC algorithm


* **Parameters**

    
    * **algorithm** (*str*) – The name of the algorithm used to perform ANC. Currently, only ‘crls’ is available.


    * **inputSignal** (*np.array*) – Input matrix (2-dimensional array). Rows are samples. Columns are input arrays.


    * **targetSignal** (*np.array*) – Target matrix (2-dimensional array). Rows are samples. Columns are input arrays.



* **Returns**

    
    * **outputSignal** (*np.array*) – An array of data representing the output signal


    * **errorSignal** (*np.array*) – Ar array of data representing the error singal




* **Raises**

    **None** – 



### diminish.algorithms.signal_processing.run_algorithm(algorithm, inputSignal, targetSignal, numChannels)
Selects a specific algorithm to use to process signa. Currently, there is only one algorithm implemented,
additional algorithms can be added here.


* **Parameters**

    
    * **algorithm** (*str*) – The name of the algorithm used to perform ANC. Currently, only ‘crls’ is available.


    * **inputSignal** (*np.array*) – Input matrix (2-dimensional array). Rows are samples. Columns are input arrays.


    * **targetSignal** (*np.array*) – Target matrix (2-dimensional array). Rows are samples. Columns are input arrays.


    * **numChannels** (*int*) – The number of channels in the input signal. Likely to always be 2.



* **Returns**

    
    * **y** (*np.array*) – An array of data representing the output signal


    * **e** (*np.array*) – Ar array of data representing the error singal




* **Raises**

    **None** – 


## Module contents

This module contains specific anc algorithm implementations
