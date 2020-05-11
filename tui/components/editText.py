import urwid

class EditText(urwid.Pile):
    def __init__(self, label, model, attribute, labelStyle, textStyle):
        self.model = model
        self.attribute = attribute
        self.label = label
        self.labelStyle = labelStyle
        self.textStyle = textStyle
        urwid.Pile.__init__(self, self.build())
    
    def build(self):
        self.editLabel = urwid.AttrWrap(urwid.Text(f'{self.label}', 'left'), self.labelStyle)
        self.editInput = urwid.Edit('', '')

        editWithAttr = urwid.AttrWrap(self.editInput, self.textStyle)

        self.refresh()
        return [self.editLabel, editWithAttr]
    
    def refresh(self):
        self.editInput.set_edit_text(str(getattr(self.model, self.attribute)))
