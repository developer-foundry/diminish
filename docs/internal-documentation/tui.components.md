# tui.components package

## Submodules

## tui.components.editText module


### class tui.components.editText.EditText(label, model, attribute, labelStyle, textStyle)
Bases: `urwid.container.Pile`

The EditText component is a text box coupled with a label.


#### \__init__(label, model, attribute, labelStyle, textStyle)

* **Parameters**

    
    * **label** (*str*) – The label value that will be displayed on screen.


    * **model** (*ConfigurationModel*) – The model that this component is linked to.


    * **attribute** (*str*) – The attribute in the model that this component is linked to. i.e. self.mode[‘name’]


    * **labelStyle** (*str*) – The style used by urwid to apply to the label text


    * **textStyle** (*str*) – The style used by urwid to apply to the textbox



#### build()
Creates the subwidgets of the components and stiches them together for the final render.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the component underlying widget display values based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.components.footerComponent module


### class tui.components.footerComponent.FooterComponent(markup, style)
Bases: `urwid.decoration.AttrMap`

The FooterComponent wraps a Text widget to used at the bottom of a urwid.Frame


#### \__init__(markup, style)

* **Parameters**

    
    * **markup** (*str*) – The urwid markup used to create the Text widget.


    * **style** (*str*) – The style to apply to the Text widget


## tui.components.headerComponent module


### class tui.components.headerComponent.HeaderComponent(markup, style)
Bases: `urwid.decoration.AttrMap`

The HeaderComponent wraps a Text widget to used at the top of a urwid.Frame


#### \__init__(markup, style)

* **Parameters**

    
    * **markup** (*str*) – The urwid markup used to create the Text widget.


    * **style** (*str*) – The style to apply to the Text widget


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

The RunningTime component represents a box displaying seconds counting up from 0.


#### \__init__()

* **Parameters**

    **None** – 



#### build()
Creates the subwidgets of the component and stiches them together for the final render.


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### refresh()
Updates the component underlying widget display values based on the system clock changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.components.systemMonitor module


### class tui.components.systemMonitor.SystemMonitor(model, monitorType, style, title)
Bases: `urwid.graphics.LineBox`

The SystemMonitor component represents a box displaying a value being monitored in the system like cpu or memory usage


#### \__init__(model, monitorType, style, title)

* **Parameters**

    
    * **model** (*ConfigurationModel*) – The model that this component is linked to.


    * **monitorType** (*str*) – The attribute in the model that this component is linked to. i.e. self.mode[‘cpu’]


    * **style** (*str*) – The style used by urwid to apply to the label text


    * **title** (*str*) – The title of the box that wraps the system monitor value.



#### refresh()
Updates the component underlying widget display values based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## tui.components.verticalRadioButtonGroup module


### class tui.components.verticalRadioButtonGroup.VerticalRadioButtonGroup(model, attribute, labelOptions, group, modelRefreshFunction)
Bases: `urwid.container.Pile`

The VerticalRadioButtonGroup component represents a list of radio buttons stacked vertically.


#### \__init__(model, attribute, labelOptions, group, modelRefreshFunction)

* **Parameters**

    
    * **model** (*ConfigurationModel*) – The model that this component is linked to.


    * **attribute** (*str*) – The attribute in the model that this component is linked to. i.e. self.mode[‘algorithm’]


    * **labelOptions** (*array*) – An array that contains the text values to display for each button


    * **group** (*str*) – An identifier to uniquely identify a group of radio buttons


    * **modelRefreshFunction** (*str*) – A callback function that can be called when the radio button value changes in the component



#### build(labelOptions, group)
Creates the subwidgets of the components and stiches them together for the final render.


* **Parameters**

    
    * **labelOptions** (*array*) – An array that contains the text values to display for each button


    * **group** (*str*) – An identifier to uniquely identify a group of radio buttons



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 



#### on_radio_change(button, state, groupName)
When the radio button value changes update the unerlying model to keep it in sync with the UI


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
Updates the component underlying widget display values based on the model changing


* **Parameters**

    **None** – 



* **Returns**

    


* **Return type**

    None



* **Raises**

    **None** – 


## Module contents

This module contains all TUI components. Components are urwid Widgets
that can be reused. This compared to a diminish View, which is a collection
of widgets.
