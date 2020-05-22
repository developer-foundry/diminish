# tui.views package

## Submodules

## tui.views.dashboardBody module


### class tui.views.dashboardBody.DashboardBody(model)
Bases: `urwid.widget.WidgetWrap`

DashboardBody is a container view holding the DashboardControls
and LiveDashboardData or PrerecordedDashboardData
(left and right sides of the screen respectfully)

LiveDashboardData or PrerecordedDashboardData will be rendered
based on the mode the user selects


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.dashboardControls module


### class tui.views.dashboardControls.DashboardControls(model)
Bases: `urwid.widget.WidgetWrap`

DashboardControls contains the widgets necessary to configure the ANC algorithm
Certain widgets will show or hide based on selections of the radio buttons.


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered. More complicated
than most widgets due to the hoops that have to be jumped through to show/hide with urwid.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### buildLists()
Composes widgets into sets and each set will be shown or hidden. In order to
hide the widgets, they need to be removed from the render pipeline altogether.
The emptyList array will be swapped in and out based on selections.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### buildWidgets()
Builds all widgets needed by the view (those hidden and shown)


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### hideWidgets()
Analyze the model and swap out the appropriate lists to hide/show widgets.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### on_radio_change(button, state, groupName)
Observer function that is injected into VerticalRadioButtonGroup to detect
value changes in the radio button.


* **Parameters**

    
    * **button** (*str*) – The value of the radio button selected. i.e. ‘crls’ or ‘prerecorded’


    * **state** (*boolean*) – True if the radio is selected, False otherwise


    * **groupName** (*str*) – The name of the group the radio button selected belongs to



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing. This refresh
function has some detailed logic for showing and hiding controls based on
values in the model.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.dashboardView module


### class tui.views.dashboardView.DashboardView(model)
Bases: `urwid.widget.WidgetWrap`

DashboardView is the primary view of the application. It contains
a Header, Body, and Footer. The model must be passed to all
child views and each child view must have a refresh function.


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.errorPercentage module


### class tui.views.errorPercentage.ErrorPercentage(model)
Bases: `urwid.widget.WidgetWrap`

ErrorPercentage contains a Box widget that renders
the current error rate for the ANC algorithm


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.liveDashboardData module


### class tui.views.liveDashboardData.LiveDashboardData(model)
Bases: `urwid.widget.WidgetWrap`

LiveDashboardData contains the monitoring widgets for the
ANC algorithm and the logging widget to determine status or
errors while the algorithm is running. This view is display
when the mode is ‘live’.


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.loggingView module


### class tui.views.loggingView.LoggingView(model, height)
Bases: `urwid.widget.WidgetWrap`

LoggingView contains a Box widget that renders all logging messages
for the TUI and CLI processes to the screen.


#### \__init__(model, height)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### convert(entries)
Converts an array of text strings to urwid Text widgets


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.prerecordedDashboard module


### class tui.views.prerecordedDashboard.PrerecordedDashboardData(model)
Bases: `urwid.widget.WidgetWrap`

PrerecordedDashboardData contains the logging widget to determine status or
errors while the algorithm is running. This view is display
when the mode is ‘prerecorded’.


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.signalGraph module


### class tui.views.signalGraph.SignalGraph(model, signal, name, height, barWidth)
Bases: `urwid.widget.WidgetWrap`

SignalGraph is a container view that uses a HeaderComponent
and a LineBox to display a live graph of incoming data
from the ANC algorithm. Generally, the graph is updated every
one second, but can be tweaked through configuring the
{guiRefreshTimer}


#### \__init__(model, signal, name, height, barWidth)

* **Parameters**

    
    * **model** (*ConfigurationModel*) – The model that this component is linked to.


    * **signal** (*np.array*) – The attribute in the model used to store data that will be graphed


    * **name** (*str*) – The name of the graph to display at the top of the graph


    * **height** (*int*) – The number of rows to use to display the graph.


    * **barWidth** (*int*) – The widget of each bar to be rendered



#### build()
Composes child views and components into a single object to be rendered.
Uses a custom widget PositiveNegativeBarGraph that is a fork of the
urwid BarGraph widget


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.statusView module


### class tui.views.statusView.StatusView(model)
Bases: `urwid.widget.WidgetWrap`

StatusView is a view to display to the user whether
or not the algorithm is paused or not.


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.views.systemMonitors module


### class tui.views.systemMonitors.SystemMonitors(model)
Bases: `urwid.widget.WidgetWrap`

SystemMonitors is a view to track various system level
information like CPU/Memory usage


#### \__init__(model)

* **Parameters**

    **model** (*ConfigurationModel*) – The model that this component is linked to.



#### build()
Composes child views and components into a single object to be rendered.
This view builds a list of System Monitors to track various system level
information like CPU/Memory usage.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the view and any child views based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents

This module contains all TUI views. Views are a collection
of widgets. diminish uses an MVC pattern for its
architecture.
