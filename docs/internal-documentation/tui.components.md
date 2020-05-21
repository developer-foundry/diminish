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
