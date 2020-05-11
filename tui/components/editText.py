import urwid

class EditText(urwid.GridFlow):
    def __init__(self, label, model, attribute, labelStyle, textStyle, width, hSep, vSep, alignment):
        self.model = model
        self.attribute = attribute
        self.label = label
        self.labelStyle = labelStyle
        self.textStyle = textStyle
        urwid.GridFlow.__init__(self, self.build(), width, hSep, vSep, alignment)
    
    def build(self):
        self.editLabel = urwid.AttrWrap(urwid.Text(f'{self.label}\n', 'left'), self.labelStyle)
        self.editInput = urwid.Edit('', 'left')

        editWithAttr = urwid.AttrWrap(self.editInput, self.textStyle)

        self.refresh()
        return [self.editLabel, editWithAttr]
    
    def refresh(self):
        self.editInput.set_edit_text(str(getattr(self.model, self.attribute)))
