# tui.controllers package

## Submodules

## tui.controllers.dashboardController module


### class tui.controllers.dashboardController.DashboardController(parameters, logger, loggingHandler)
Bases: `object`

DashboardController is the primary controller in the diminish TUI. As
more screens are added later, new controllers should be created.

This controller kicks off the MainLoop for urwid, handles model updates,
renders views, and maintains a connection to the underlying diminish CLI
process for performing the ANC algorithm.


#### \__init__(parameters, logger, loggingHandler)

* **Parameters**

    
    * **parameters** (*array*) – An array of environment variables used to initialize the model.


    * **logger** (*Logger*) – A python Logger that will render logs to the screen.


    * **loggingHandler** (*TuiHandler*) – The TuiHandler overrides the standard python logging to stdout/stderr and writes any log
    messages to the Logging view.



#### createConnectionToCli()
Using the python multiprocessing library, this function will create a Pipe to the
process that spawned the CLI. All monitoring data will be passed from the Monitor class
in diminish to the TUI via this connection.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### getEnvironmentVars()
Constructs a dictionary of the environment variables to inject into the CLI process that spawns.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### handle_input(key)
All keyboard input for the main screen is processed in this function


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### read_pipe(read_data)
Monitors a stdout or stderr pipe and redirects it to the logger.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh(_loop, data)
Refresh runs every {guiRefreshTimer} seconds and will rerender the screen with updated model values.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### run()
Spawns the diminish CLI and runs the ANC algorithm based on the selections the user made on screen.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### togglePause()
Toggles whether or not the algorithm is running and passes that message to the CLI process


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### updateGraphs()
Parses the data based from the diminish Monitor class related to the sound graphs.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents

This module contains all TUI controllers. Controllers orchestrate the interaction
between the model and the views.
