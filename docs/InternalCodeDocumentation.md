# cli package

## Module contents

Diminish CLI

This module allows a user to start the ANC process for a server or client
using environment variables to configure the process. The process will
run as a command line interface that the user can exit with Ctrl + C.
The user can pause the algorithm using ‘P’
# client module
# common package

## Submodules

## common.common module

Common

This script shares common functions and variables needed by the CLI and TUI scripts.

This file can also be imported as a module and contains the following
functions and variables:

> 
> * mu - utilized by the CRLS algorithm to determine the step of gradient 

>     descent algorithm


> * guiRefreshTimer - this timer is used by the tui application to determine how 

>     long in between a screen refresh


> * get_project_root - used to determine the root folder when the tui applications 

>     spawns the cli process.


> * getEnvironmentVariables - returns all environment variables needed by

>     the cli and tui


> * getEnvVar - returns a single environment variable


> * getInt - converts a str to int for env vars


### common.common.getEnvVar(varName, isInteger=False)

### common.common.getEnvironmentVariables()

### common.common.getInt(val)

### common.common.get_project_root()
## common.continuousBuffer module


### class common.continuousBuffer.ContinuousBuffer(name, stepSize, numChannels=2)
Bases: `object`

ContinuousBuffer is a buffer that acts as a rolling buffer
Items that are popped are simply moved to the end of the buffer
Typically a ContinuousBuffer is initialized with its entire data set
up front rather than continuously pushing data onto the buffer.

ContinuousBuffer is utilized by diminish to handle the Target File buffer.

lock

    A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.

buffer

    A numpy array that holds the underlying data stream (stereo sound)

maxSize

    The maximum size of the buffer.

currentLocation

    Tracks the current location that the buffer is at. Used by the pop method to determine the starting location of the next chunk.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.

name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

subscriber

    Each buffer can have one subscriber that will be notified upon a pop.

subscribe(observer: Callable)

    Subscribes an observer to be notified upon a pop of the buffer.

push(data: np.array)

    Adds data to the end of the buffer

pop()

    Returns a chunk of data from ‘currentLocation’ to ‘currentLocation + stepSize’.
    Moves that chunk to the end of the buffer

size()

    Returns the size of the buffer


#### \__init__(name, stepSize, numChannels=2)
name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.


#### pop()
Returns a chunk of data from ‘currentLocation’ to ‘currentLocation + stepSize’.
Moves that chunk to the end of the buffer

None

data

    A numpy array representing a chunk of the buffer.

None


#### push(data)
Adds data to the end of the buffer

data

    The numpy array data to add to the end of the buffer

None

None


#### size()
Returns the size of the buffer

None

size

    Size of the buffer

None


#### subscribe(observer: Callable)
Subscribes an observer to be notified upon a pop of the buffer.

observer

    The observer to attach to the subscriber for notification of a pop.

None

None

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

lock

    A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.

buffer

    A numpy array that holds the underlying data stream (stereo sound)

waitSize

    The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
    Provides a mechanism to capture data while the algorithm is syncronizing.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.

name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

subscriber

    Each buffer can have one subscriber that will be notified upon a pop.

subscribe(observer: Callable)

    Subscribes an observer to be notified upon a pop of the buffer.

push(data: np.array)

    Adds data to the end of the buffer

pop()

    Returns a chunk of data from the front of the buffer to ‘stepSize’.
    Deletes the chunk from the buffer.

is_ready()

    Determines whether or not the buffer is ready for processing

size()

    Returns the size of the buffer

clear()

    Zeros out the entire buffer.


#### \__init__(name, waitSize, stepSize, numChannels=2)
name

    The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.

waitSize

    The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
    Provides a mechanism to capture data while the algorithm is syncronizing.

stepSize

    The amount of data to pop off the buffer.

numChannels

    The number of channels of the sound file in question. Likely will always be 2.


#### clear()
Zeros out the entire buffer.

None

None

None


#### is_ready()
Determines whether or not the buffer is ready for processing

None

isReady

    A boolean representing whether or not the buffer is ready for processing in the Diminish algorithm

None


#### pop()
Returns a chunk of data from the front of the buffer to ‘stepSize’.
Deletes the chunk from the buffer.

None

data

    A numpy array representing a chunk of the buffer.

None


#### push(data)
Adds data to the end of the buffer

data

    The numpy array data to add to the end of the buffer

None

None


#### size()
Returns the size of the buffer

None

size

    Size of the buffer

None


#### subscribe(observer: Callable)
Subscribes an observer to be notified upon a pop of the buffer.

observer

    The observer to attach to the subscriber for notification of a pop.

None

None

## Module contents

Common

This module is for code that is common between the CLI, TUI, and Diminish modules.
Common functions and configuration can be placed in this module.
# diminish.algorithms package

## Submodules

## diminish.algorithms.crls module


### class diminish.algorithms.crls.Signal()
Bases: `_ctypes.Structure`


#### channel_one()
Structure/Union member


#### channel_one_start()
Structure/Union member


#### channel_two()
Structure/Union member


#### channel_two_start()
Structure/Union member


#### length()
Structure/Union member


### diminish.algorithms.crls.crls(inputSignal, targetSignal, mu, n)
## diminish.algorithms.signal_processing module


### diminish.algorithms.signal_processing.process_signal(inputSignal, targetSignal, algorithm)

### diminish.algorithms.signal_processing.run_algorithm(algorithm, inputSignal, targetSignal, numChannels)
## Module contents
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


#### process_anc(device, targetFile, algorithm, btmode, waitSize, stepSize, size, tuiConnection)

#### process_prerecorded(device, inputFile, targetFile, truncateSize, algorithm)
## Module contents
# diminish.monitoring package

## Submodules

## diminish.monitoring.monitor module


### class diminish.monitoring.monitor.Monitor(buffers)
Bases: `object`


#### \__init__(buffers)
Initialize self.  See help(type(self)) for accurate signature.


#### close_connection()

#### create_connection()

#### observe(bufferName, data)

#### plot_buffers(algorithm)

#### sendData()
## Module contents
# diminish.orchestrators package

## Submodules

## diminish.orchestrators.clientOrchestrator module


### class diminish.orchestrators.clientOrchestrator.ClientOrchestrator(device, waitSize, stepSize)
Bases: `object`


#### \__init__(device, waitSize, stepSize)
Initialize self.  See help(type(self)) for accurate signature.


#### run()
## diminish.orchestrators.serverOrchestrator module


### class diminish.orchestrators.serverOrchestrator.ServerOrchestrator(device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection)
Bases: `object`


#### \__init__(device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection)
Initialize self.  See help(type(self)) for accurate signature.


#### clear_buffers()

#### is_ready()

#### on_release(key)

#### pauseHandler(signum, frame)

#### run()

#### run_algorithm()

#### stop()
## Module contents
# diminish.plotting package

## Submodules

## diminish.plotting.plot module


### diminish.plotting.plot.get_dir(algorithm, mode)

### diminish.plotting.plot.plot_simultaneous(algorithm, mode, inputSignal, targetSignal, outputSignal)

### diminish.plotting.plot.plot_vertical(algorithm, mode, inputSignal, targetSignal, outputSignal, errorSignal)

### diminish.plotting.plot.plot_vertical_buffers(algorithm, mode, buffers)
## Module contents
# diminish.signals package

## Submodules

## diminish.signals.inputSignal module


### class diminish.signals.inputSignal.InputSignal(device, buffer, stepSize, threadName)
Bases: `threading.Thread`


#### \__init__(device, buffer, stepSize, threadName)
This constructor should always be called with keyword arguments. Arguments are:

*group* should be None; reserved for future extension when a ThreadGroup
class is implemented.

*target* is the callable object to be invoked by the run()
method. Defaults to None, meaning nothing is called.

*name* is the thread name. By default, a unique name is constructed of
the form “Thread-N” where N is a small decimal number.

*args* is the argument tuple for the target invocation. Defaults to ().

*kwargs* is a dictionary of keyword arguments for the target
invocation. Defaults to {}.

If a subclass overrides the constructor, it must make sure to invoke
the base class constructor (Thread.__init__()) before doing anything
else to the thread.


#### listener(indata, frames, time, status)

#### run()
Method representing the thread’s activity.

You may override this method in a subclass. The standard run() method
invokes the callable object passed to the object’s constructor as the
target argument, if any, with sequential and keyword arguments taken
from the args and kwargs arguments, respectively.


#### stop()
## diminish.signals.outputSignal module


### class diminish.signals.outputSignal.OutputSignal(device, buffer, stepSize, waitCondition, threadName)
Bases: `threading.Thread`


#### \__init__(device, buffer, stepSize, waitCondition, threadName)
This constructor should always be called with keyword arguments. Arguments are:

*group* should be None; reserved for future extension when a ThreadGroup
class is implemented.

*target* is the callable object to be invoked by the run()
method. Defaults to None, meaning nothing is called.

*name* is the thread name. By default, a unique name is constructed of
the form “Thread-N” where N is a small decimal number.

*args* is the argument tuple for the target invocation. Defaults to ().

*kwargs* is a dictionary of keyword arguments for the target
invocation. Defaults to {}.

If a subclass overrides the constructor, it must make sure to invoke
the base class constructor (Thread.__init__()) before doing anything
else to the thread.


#### listener(outdata, frames, time, status)

#### run()
Method representing the thread’s activity.

You may override this method in a subclass. The standard run() method
invokes the callable object passed to the object’s constructor as the
target argument, if any, with sequential and keyword arguments taken
from the args and kwargs arguments, respectively.


#### stop()
## diminish.signals.targetSignal module


### class diminish.signals.targetSignal.TargetSignal(targetFile, buffer, stepSize, size, threadName)
Bases: `threading.Thread`


#### \__init__(targetFile, buffer, stepSize, size, threadName)
This constructor should always be called with keyword arguments. Arguments are:

*group* should be None; reserved for future extension when a ThreadGroup
class is implemented.

*target* is the callable object to be invoked by the run()
method. Defaults to None, meaning nothing is called.

*name* is the thread name. By default, a unique name is constructed of
the form “Thread-N” where N is a small decimal number.

*args* is the argument tuple for the target invocation. Defaults to ().

*kwargs* is a dictionary of keyword arguments for the target
invocation. Defaults to {}.

If a subclass overrides the constructor, it must make sure to invoke
the base class constructor (Thread.__init__()) before doing anything
else to the thread.


#### run()
Method representing the thread’s activity.

You may override this method in a subclass. The standard run() method
invokes the callable object passed to the object’s constructor as the
target argument, if any, with sequential and keyword arguments taken
from the args and kwargs arguments, respectively.


#### stop()
## Module contents
# filtering module
<!-- diminish documentation master file, created by
sphinx-quickstart on Thu May 21 07:59:43 2020.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# Welcome to diminish’s documentation!


* cli package


    * Module contents


* client module


* common package


    * Submodules


    * common.common module


    * common.continuousBuffer module


    * common.fifoBuffer module


    * Module contents


* diminish package


    * Subpackages


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


    * Submodules


    * diminish.diminish module


    * Module contents


* filtering module


* server module


* tasks module


* tui package


    * Subpackages


        * tui.components package


            * Submodules


            * tui.components.editText module


            * tui.components.footerComponent module


            * tui.components.headerComponent module


            * tui.components.positiveNegativeBarGraph module


            * tui.components.runningTime module


            * tui.components.systemMonitor module


            * tui.components.verticalRadioButtonGroup module


            * Module contents


        * tui.controllers package


            * Submodules


            * tui.controllers.dashboardController module


            * Module contents


        * tui.logging package


            * Submodules


            * tui.logging.tuiHandler module


            * Module contents


        * tui.models package


            * Submodules


            * tui.models.configurationModel module


            * tui.models.configurationOptionsModel module


            * Module contents


        * tui.palette package


            * Submodules


            * tui.palette.palette module


            * Module contents


        * tui.views package


            * Submodules


            * tui.views.dashboardBody module


            * tui.views.dashboardControls module


            * tui.views.dashboardView module


            * tui.views.errorPercentage module


            * tui.views.liveDashboardData module


            * tui.views.loggingView module


            * tui.views.prerecordedDashboard module


            * tui.views.signalGraph module


            * tui.views.statusView module


            * tui.views.systemMonitors module


            * Module contents


    * Module contents


# Indices and tables


* Index


* Module Index


* Search Page
# server module
# tasks module
# tui.components package

## Submodules

## tui.components.editText module


### class tui.components.editText.EditText(label, model, attribute, labelStyle, textStyle)
Bases: `urwid.container.Pile`


#### \__init__(label, model, attribute, labelStyle, textStyle)

* **Parameters**

    
    * **widget_list** (*iterable*) – child widgets


    * **focus_item** (*Widget** or **int*) – child widget that gets the focus initially.
    Chooses the first selectable widget if unset.


*widget_list* may also contain tuples such as:

(*given_height*, *widget*)

    always treat *widget* as a box widget and give it *given_height* rows,
    where given_height is an int

(`'pack'`, *widget*)

    allow *widget* to calculate its own height by calling its `rows()`
    method, ie. treat it as a flow widget.

(`'weight'`, *weight*, *widget*)

    if the pile is treated as a box widget then treat widget as a box
    widget with a height based on its relative weight value, otherwise
    treat the same as (`'pack'`, *widget*).

Widgets not in a tuple are the same as (`'weight'`, `1`, *widget*)\`

**NOTE**: If the Pile is treated as a box widget there must be at least
one `'weight'` tuple in `widget_list`.


#### build()

#### refresh()
## tui.components.footerComponent module


### class tui.components.footerComponent.FooterComponent(markup, style)
Bases: `urwid.decoration.AttrMap`


#### \__init__(markup, style)

* **Parameters**

    
    * **w** (*widget*) – widget to wrap (stored as self.original_widget)


    * **attr_map** (*display attribute** or **dict*) – attribute to apply to *w*, or dict of old display
    attribute: new display attribute mappings


    * **focus_map** (*display attribute** or **dict*) – attribute to apply when in focus or dict of
    old display attribute: new display attribute mappings;
    if `None` use *attr*


```python
>>> AttrMap(Divider(u"!"), 'bright')
<AttrMap flow widget <Divider flow widget '!'> attr_map={None: 'bright'}>
>>> AttrMap(Edit(), 'notfocus', 'focus')
<AttrMap selectable flow widget <Edit selectable flow widget '' edit_pos=0> attr_map={None: 'notfocus'} focus_map={None: 'focus'}>
>>> size = (5,)
>>> am = AttrMap(Text(u"hi"), 'greeting', 'fgreet')
>>> next(am.render(size, focus=False).content()) # ... = b in Python 3
[('greeting', None, ...'hi   ')]
>>> next(am.render(size, focus=True).content())
[('fgreet', None, ...'hi   ')]
>>> am2 = AttrMap(Text(('word', u"hi")), {'word':'greeting', None:'bg'})
>>> am2
<AttrMap flow widget <Text flow widget 'hi'> attr_map={'word': 'greeting', None: 'bg'}>
>>> next(am2.render(size).content())
[('greeting', None, ...'hi'), ('bg', None, ...'   ')]
```

## tui.components.headerComponent module


### class tui.components.headerComponent.HeaderComponent(markup, style)
Bases: `urwid.decoration.AttrMap`


#### \__init__(markup, style)

* **Parameters**

    
    * **w** (*widget*) – widget to wrap (stored as self.original_widget)


    * **attr_map** (*display attribute** or **dict*) – attribute to apply to *w*, or dict of old display
    attribute: new display attribute mappings


    * **focus_map** (*display attribute** or **dict*) – attribute to apply when in focus or dict of
    old display attribute: new display attribute mappings;
    if `None` use *attr*


```python
>>> AttrMap(Divider(u"!"), 'bright')
<AttrMap flow widget <Divider flow widget '!'> attr_map={None: 'bright'}>
>>> AttrMap(Edit(), 'notfocus', 'focus')
<AttrMap selectable flow widget <Edit selectable flow widget '' edit_pos=0> attr_map={None: 'notfocus'} focus_map={None: 'focus'}>
>>> size = (5,)
>>> am = AttrMap(Text(u"hi"), 'greeting', 'fgreet')
>>> next(am.render(size, focus=False).content()) # ... = b in Python 3
[('greeting', None, ...'hi   ')]
>>> next(am.render(size, focus=True).content())
[('fgreet', None, ...'hi   ')]
>>> am2 = AttrMap(Text(('word', u"hi")), {'word':'greeting', None:'bg'})
>>> am2
<AttrMap flow widget <Text flow widget 'hi'> attr_map={'word': 'greeting', None: 'bg'}>
>>> next(am2.render(size).content())
[('greeting', None, ...'hi'), ('bg', None, ...'   ')]
```

## tui.components.positiveNegativeBarGraph module


### class tui.components.positiveNegativeBarGraph.PositiveNegativeBarGraph(attlist, hatt=None)
Bases: `urwid.widget.Widget`


#### \__init__(attlist, hatt=None)
Create a bar graph with the passed display characteristics.
see set_segment_attributes for a description of the parameters.


#### calculate_bar_widths(size, bardata)
Return a list of bar widths, one for each bar in data.

If self.bar_width is None this implementation will stretch
the bars across the available space specified by maxcol.


#### calculate_display(size)
Calculate display data.


#### calculate_scale(maxrow, top, row)

#### get_bar_positions(bardata, top, bottom, bar_widths, maxrow)
Calculate a rendering of the bar graph described by data, bar_widths
and height.

bardata – bar information with same structure as BarGraph.data
top – maximal value for bardata segments
bar_widths – list of integer column widths for each bar
maxrow – rows for display of bargraph

Returns a structure as follows:
[ ( y_count, [ ( bar_type, width), … ] ), … ]

The outer tuples represent a set of identical rows. y_count is
the number of rows in this set, the list contains the data to be
displayed in the row repeated through the set.

The inner tuple describes a run of width characters of bar_type.
bar_type is an integer starting from 0 for the background, 1 for
the 1st segment, 2 for the 2nd segment etc..

This function should complete in approximately O(n+m) time, where
n is the number of bars displayed and m is the number of rows.


#### property get_data()

#### location_is_a_bar(bar_positions, row, col)

#### maxcol( = None)

#### render(size, focus=False)
Render BarGraph.


#### scale_bar_values(bar, top, bottom, maxrow)
Return a list of bar values aliased to integer values of maxrow.
maxrow is the maximum colums used in the terminal


#### selectable()
Return False.


#### set_bar_width(width)
Set a preferred bar width for calculate_bar_widths to use.

width – width of bar or None for automatic width adjustment


#### set_data(bardata, top, bottom)
Store bar data, bargraph top and horizontal line positions.

bardata – a list of bar values.
top – maximum value for segments within bardata

bar values are [ segment1, segment2, … ] lists where top is
the maximal value corresponding to the top of the bar graph and
segment1, segment2, … are the values for the top of each
segment of this bar.  Simple bar graphs will only have one
segment in each bar value.

Eg: if top is 100 and there is a bar value of [ 80, 30 ] then
the top of this bar will be at 80% of full height of the graph
and it will have a second segment that starts at 30%.


#### set_segment_attributes(attlist, hatt=None)

* **Parameters**

    
    * **attlist** – list containing display attribute or
    (display attribute, character) tuple for background,
    first segment, and optionally following segments.
    ie. len(attlist) == num segments+1
    character defaults to ‘ ‘ if not specified.


    * **hatt** – list containing attributes for horizontal lines. First
    element is for lines on background, second is for lines
    on first segment, third is for lines on second segment
    etc.


eg: set_segment_attributes( [‘no’, (‘unsure’,”?”), ‘yes’] )
will use the attribute ‘no’ for the background (the area from
the top of the graph to the top of the bar), question marks
with the attribute ‘unsure’ will be used for the topmost
segment of the bar, and the attribute ‘yes’ will be used for
the bottom segment of the bar.


#### update_matrix_with_bar_positions(bar_positions, disp)

### exception tui.components.positiveNegativeBarGraph.PositiveNegativeGraphError()
Bases: `Exception`

## tui.components.runningTime module


### class tui.components.runningTime.RunningTime()
Bases: `urwid.widget.WidgetWrap`


#### \__init__()
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.components.systemMonitor module


### class tui.components.systemMonitor.SystemMonitor(model, monitorType, style, title)
Bases: `urwid.graphics.LineBox`


#### \__init__(model, monitorType, style, title)
Draw a line around original_widget.

Use ‘title’ to set an initial title text with will be centered
on top of the box.

Use title_attr to apply a specific attribute to the title text.

Use title_align to align the title to the ‘left’, ‘right’, or ‘center’.
The default is ‘center’.

You can also override the widgets used for the lines/corners:

    tline: top line
    bline: bottom line
    lline: left line
    rline: right line
    tlcorner: top left corner
    trcorner: top right corner
    blcorner: bottom left corner
    brcorner: bottom right corner

If empty string is specified for one of the lines/corners, then no
character will be output there.  This allows for seamless use of
adjoining LineBoxes.


#### refresh()
## tui.components.verticalRadioButtonGroup module


### class tui.components.verticalRadioButtonGroup.VerticalRadioButtonGroup(model, attribute, labelOptions, group, modelRefreshFunction)
Bases: `urwid.container.Pile`


#### \__init__(model, attribute, labelOptions, group, modelRefreshFunction)

* **Parameters**

    
    * **widget_list** (*iterable*) – child widgets


    * **focus_item** (*Widget** or **int*) – child widget that gets the focus initially.
    Chooses the first selectable widget if unset.


*widget_list* may also contain tuples such as:

(*given_height*, *widget*)

    always treat *widget* as a box widget and give it *given_height* rows,
    where given_height is an int

(`'pack'`, *widget*)

    allow *widget* to calculate its own height by calling its `rows()`
    method, ie. treat it as a flow widget.

(`'weight'`, *weight*, *widget*)

    if the pile is treated as a box widget then treat widget as a box
    widget with a height based on its relative weight value, otherwise
    treat the same as (`'pack'`, *widget*).

Widgets not in a tuple are the same as (`'weight'`, `1`, *widget*)\`

**NOTE**: If the Pile is treated as a box widget there must be at least
one `'weight'` tuple in `widget_list`.


#### build(labelOptions, group)

#### on_radio_change(button, state, groupName)

#### refresh()
## Module contents
# tui.controllers package

## Submodules

## tui.controllers.dashboardController module


### class tui.controllers.dashboardController.DashboardController(parameters, logger, loggingHandler)
Bases: `object`


#### \__init__(parameters, logger, loggingHandler)
Initialize self.  See help(type(self)) for accurate signature.


#### createConnectionToCli()

#### getEnvironmentVars()

#### handle_input(key)

#### read_pipe(read_data)

#### refresh(_loop, data)

#### run()

#### togglePause()

#### updateGraphs()
## Module contents
# tui.logging package

## Submodules

## tui.logging.tuiHandler module


### class tui.logging.tuiHandler.TuiHandler()
Bases: `logging.StreamHandler`


#### \__init__()
Initialize the handler.

If stream is not specified, sys.stderr is used.


#### configureModel(model)

#### emit(record)
Emit a record.

If a formatter is specified, it is used to format the record.
The record is then written to the stream with a trailing newline.  If
exception information is present, it is formatted using
traceback.print_exception and appended to the stream.  If the stream
has an ‘encoding’ attribute, it is used to determine how to do the
output to the stream.

## Module contents
# tui package

## Subpackages


* tui.components package


    * Submodules


    * tui.components.editText module


    * tui.components.footerComponent module


    * tui.components.headerComponent module


    * tui.components.positiveNegativeBarGraph module


    * tui.components.runningTime module


    * tui.components.systemMonitor module


    * tui.components.verticalRadioButtonGroup module


    * Module contents


* tui.controllers package


    * Submodules


    * tui.controllers.dashboardController module


    * Module contents


* tui.logging package


    * Submodules


    * tui.logging.tuiHandler module


    * Module contents


* tui.models package


    * Submodules


    * tui.models.configurationModel module


    * tui.models.configurationOptionsModel module


    * Module contents


* tui.palette package


    * Submodules


    * tui.palette.palette module


    * Module contents


* tui.views package


    * Submodules


    * tui.views.dashboardBody module


    * tui.views.dashboardControls module


    * tui.views.dashboardView module


    * tui.views.errorPercentage module


    * tui.views.liveDashboardData module


    * tui.views.loggingView module


    * tui.views.prerecordedDashboard module


    * tui.views.signalGraph module


    * tui.views.statusView module


    * tui.views.systemMonitors module


    * Module contents


## Module contents
# tui.models package

## Submodules

## tui.models.configurationModel module


### class tui.models.configurationModel.ConfigurationModel(parameters)
Bases: `object`


#### \__init__(parameters)
Initialize self.  See help(type(self)) for accurate signature.

## tui.models.configurationOptionsModel module


### class tui.models.configurationOptionsModel.ConfigurationOptionsModel()
Bases: `object`


#### \__init__()
Initialize self.  See help(type(self)) for accurate signature.

## Module contents
# tui.palette package

## Submodules

## tui.palette.palette module

## Module contents
# tui.views package

## Submodules

## tui.views.dashboardBody module


### class tui.views.dashboardBody.DashboardBody(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.views.dashboardControls module


### class tui.views.dashboardControls.DashboardControls(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### buildLists()

#### buildWidgets()

#### hideWidgets()

#### on_radio_change(button, state, groupName)

#### refresh()
## tui.views.dashboardView module


### class tui.views.dashboardView.DashboardView(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.views.errorPercentage module


### class tui.views.errorPercentage.ErrorPercentage(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.views.liveDashboardData module


### class tui.views.liveDashboardData.LiveDashboardData(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.views.loggingView module


### class tui.views.loggingView.LoggingView(model, height)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model, height)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### convert(entries)

#### refresh()
## tui.views.prerecordedDashboard module


### class tui.views.prerecordedDashboard.PrerecordedDashboardData(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.views.signalGraph module


### class tui.views.signalGraph.SignalGraph(model, signal, name, height, barWidth)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model, signal, name, height, barWidth)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.views.statusView module


### class tui.views.statusView.StatusView(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## tui.views.systemMonitors module


### class tui.views.systemMonitors.SystemMonitors(model)
Bases: `urwid.widget.WidgetWrap`


#### \__init__(model)
w – widget to wrap, stored as self._w

This object will pass the functions defined in Widget interface
definition to self._w.

The purpose of this widget is to provide a base class for
widgets that compose other widgets for their display and
behaviour.  The details of that composition should not affect
users of the subclass.  The subclass may decide to expose some
of the wrapped widgets by behaving like a ContainerWidget or
WidgetDecoration, or it may hide them from outside access.


#### build()

#### refresh()
## Module contents
