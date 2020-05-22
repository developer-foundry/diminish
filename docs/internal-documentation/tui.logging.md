# tui.logging package

## Submodules

## tui.logging.tuiHandler module


### class tui.logging.tuiHandler.TuiHandler()
Bases: `logging.StreamHandler`

TuiHandler is a custom logging handler that will add log messages
to a ConfigurationModel object rather than directing the messages
to stdout or stderr. This prevents urwid from displaying random
error messages on top of DashboardView.


#### \__init__()

* **Parameters**

    **None** – 



#### configureModel(model)
Called to register the model with the handler so that messages can be appended to logEntries


* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### emit(record)
Called when a message is sent to a logger.


* **Parameters**

    **record** (*LogRecord*) – The record passed from the logger that contains the message and log level.



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents

This module contains all custom logging code for the TUI application
