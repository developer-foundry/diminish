import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.verticalRadioButtonGroup import VerticalRadioButtonGroup
from tui.components.editText import EditText
from tui.views.errorPercentage import ErrorPercentage

class DashboardControls(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        self.mode_buttons = VerticalRadioButtonGroup(self.model, 'mode', self.model.options.availableModes, [])
        self.algorithm_buttons = VerticalRadioButtonGroup(self.model, 'algorithm', self.model.options.availableAlgorithms, [])
        header = HeaderComponent(f'Algorithm Controls', 'header')

        self.inputFile = EditText("Input File", self.model, 'inputFile', 'controlLabel', 'controlText')
        self.targetFile = EditText("Target File", self.model, 'targetFile', 'controlLabel', 'controlText')
        self.device = EditText("Device", self.model, 'device', 'controlLabel', 'controlText')
        self.size = EditText("Size", self.model, 'size', 'controlLabel', 'controlText')
        self.role = EditText("Role", self.model, 'role', 'controlLabel', 'controlText')
        self.waitSize = EditText("Wait Size", self.model, 'waitSize', 'controlLabel', 'controlText')
        self.stepSize = EditText("Step Size", self.model, 'stepSize', 'controlLabel', 'controlText')
        self.errorPercentage = ErrorPercentage(self.model)

        l = [
            header,
            urwid.AttrWrap(urwid.Text("Mode"), 'controlLabel'),
            self.mode_buttons,
            urwid.Divider(),
            urwid.AttrWrap(urwid.Text("Algorithm"), 'controlLabel'),
            self.algorithm_buttons,
            urwid.Divider(),
            self.inputFile,
            urwid.Divider(),
            self.targetFile,
            urwid.Divider(),
            self.device,
            urwid.Divider(),
            self.size,
            urwid.Divider(),
            self.role,
            urwid.Divider(),
            self.waitSize,
            urwid.Divider(),
            self.stepSize,
            urwid.Divider(),
            self.errorPercentage
            ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        return w
    
    def refresh(self):
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
