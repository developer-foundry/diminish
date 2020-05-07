import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.radioButtonGroup import RadioButtonGroup

class DashboardControls(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        mode_buttons = RadioButtonGroup(self.model.options.availableModes, [], self.on_mode_button, self.model.mode)
        header = HeaderComponent(f'Algorithm Controls', 'header')

        l = [
            header,    
            urwid.Text("Mode"),
            ] + mode_buttons + [ #radiobuttongroup is a list, so you have to concat vs referencing directly for the walker
            urwid.Divider(),
            urwid.Text("Animation")
            ]

        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w
    
    def on_mode_button(self, button, state):
        """Notify the controller of a new mode setting."""
        if state:
            # The new mode is the label of the button
            self.model.mode = button.get_label()