import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.verticalRadioButtonGroup import VerticalRadioButtonGroup
from tui.components.editText import EditText

class DashboardControls(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        self.mode_buttons = VerticalRadioButtonGroup(self.model, 'mode', self.model.options.availableModes, [], 30, 0, 1, 'left')
        self.algorithm_buttons = VerticalRadioButtonGroup(self.model, 'algorithm', self.model.options.availableAlgorithms, [], 30, 0, 1, 'left')
        header = HeaderComponent(f'Algorithm Controls', 'header')

        self.inputFile = EditText("Input File", self.model, 'inputFile', 'controlLabel', 'controlText', 30, 0, 1, 'left')
        self.targetFile = EditText("Target File", self.model, 'targetFile', 'controlLabel', 'controlText', 30, 0, 1, 'left')
        self.device = EditText("Device", self.model, 'device', 'controlLabel', 'controlText', 30, 0, 1, 'left')
        self.size = EditText("Size", self.model, 'size', 'controlLabel', 'controlText', 30, 0, 1, 'left')
        self.role = EditText("Role", self.model, 'role', 'controlLabel', 'controlText', 30, 0, 1, 'left')
        self.waitSize = EditText("Wait Size", self.model, 'waitSize', 'controlLabel', 'controlText', 30, 0, 1, 'left')
        self.stepSize = EditText("Step Size", self.model, 'stepSize', 'controlLabel', 'controlText', 30, 0, 1, 'left')

        l = [
            header,
            urwid.AttrWrap(urwid.Text("Mode"), 'controlLabel'),
            self.mode_buttons,
            urwid.Divider(),
            urwid.AttrWrap(urwid.Text("Algorithm"), 'controlLabel'),
            self.algorithm_buttons,
            self.inputFile,
            self.targetFile,
            self.device,
            self.size,
            self.role,
            self.waitSize,
            self.stepSize
            ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        return w
    
    def refresh(self):
        self.mode_buttons.refresh()
        self.algorithm_buttons.refresh()
