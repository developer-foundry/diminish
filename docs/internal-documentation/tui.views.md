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
