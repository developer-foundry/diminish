import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.verticalRadioButtonGroup import VerticalRadioButtonGroup
from tui.components.editText import EditText
from tui.views.errorPercentage import ErrorPercentage
from tui.components.runningTime import RunningTime
from tui.views.statusView import StatusView

class DashboardControls(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        self.livePile = None
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        self.buildWidgets()
        self.buildLists()

        self.startPile = urwid.WidgetPlaceholder(urwid.Pile(self.startAlwaysVisibleList))
        self.prerecordedPile = urwid.WidgetPlaceholder(urwid.Pile(self.prerecordedList))
        self.livePile = urwid.WidgetPlaceholder(urwid.Pile(self.liveList))
        self.endPile = urwid.WidgetPlaceholder(urwid.Pile(self.endAlwaysVisibleList))

        l = [
            self.startPile,
            self.prerecordedPile,
            self.livePile,
            self.endPile
        ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        self.hideWidgets()
        return w
    
    def buildWidgets(self):
        self.mode_buttons = VerticalRadioButtonGroup(self.model, 'mode', self.model.options.availableModes, [], self.on_radio_change)
        self.algorithm_buttons = VerticalRadioButtonGroup(self.model, 'algorithm', self.model.options.availableAlgorithms, [], self.on_radio_change)
        self.header = HeaderComponent(f'Algorithm Controls', 'header')
        self.inputFile = EditText("Input File", self.model, 'inputFile', 'controlLabel', 'controlText')
        self.targetFile = EditText("Target File", self.model, 'targetFile', 'controlLabel', 'controlText')
        self.device = EditText("Device", self.model, 'device', 'controlLabel', 'controlText')
        self.size = EditText("Size", self.model, 'size', 'controlLabel', 'controlText')
        self.role = EditText("Role", self.model, 'role', 'controlLabel', 'controlText')
        self.waitSize = EditText("Wait Size", self.model, 'waitSize', 'controlLabel', 'controlText')
        self.stepSize = EditText("Step Size", self.model, 'stepSize', 'controlLabel', 'controlText')
        self.errorPercentage = ErrorPercentage(self.model)
        self.runningTime = RunningTime()
        self.status = StatusView(self.model)

    def buildLists(self):
        self.startAlwaysVisibleList = [
            self.header,
            urwid.AttrWrap(urwid.Text("Mode"), 'controlLabel'),
            self.mode_buttons,
            urwid.Divider(),
            urwid.AttrWrap(urwid.Text("Algorithm"), 'controlLabel'),
            self.algorithm_buttons,
            urwid.Divider(),
            self.device,
            urwid.Divider(),
        ]

        self.prerecordedList = [
            self.inputFile,
            urwid.Divider(),
            self.targetFile,
            urwid.Divider(),
            self.size,
            urwid.Divider(),
        ]

        self.liveList = [
            self.role,
            urwid.Divider(),
            self.waitSize,
            urwid.Divider(),
            self.stepSize,
            urwid.Divider(),
        ]

        self.endAlwaysVisibleList = [
            self.errorPercentage,
            urwid.Divider(),
            self.runningTime,
            urwid.Divider(),
            self.status
        ]

        self.emptyList = []

    def hideWidgets(self):
        if self.model.mode == 'live':
            self.prerecordedPile._set_original_widget(urwid.Pile(self.emptyList))
            self.livePile._set_original_widget(urwid.Pile(self.liveList))
        elif self.model.mode == 'prerecorded':
            self.livePile._set_original_widget(urwid.Pile(self.emptyList))
            self.prerecordedPile._set_original_widget(urwid.Pile(self.prerecordedList))

    def on_radio_change(self, button, state, groupName):
        if self.livePile is not None:
            self.hideWidgets()

    def refresh(self):
        self.hideWidgets()
        self.mode_buttons.refresh()
        self.algorithm_buttons.refresh()
        self.inputFile.refresh()
        self.targetFile.refresh()
        self.device.refresh()
        self.size.refresh()
        self.role.refresh()
        self.waitSize.refresh()
        self.stepSize.refresh()
        self.errorPercentage.refresh()
        self.runningTime.refresh()
        self.status.refresh()
        self.hideWidgets()
