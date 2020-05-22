import urwid


class EditText(urwid.Pile):
    """
    The EditText component is a text box coupled with a label.
    """

    def __init__(self, label, model, attribute, labelStyle, textStyle):
        """
        Parameters
        ----------
        label : str
            The label value that will be displayed on screen.
        model : ConfigurationModel
            The model that this component is linked to.
        attribute : str
            The attribute in the model that this component is linked to. i.e. self.mode['name']
        labelStyle : str
            The style used by urwid to apply to the label text
        textStyle : str
            The style used by urwid to apply to the textbox
        """
        self.model = model
        self.attribute = attribute
        self.label = label
        self.labelStyle = labelStyle
        self.textStyle = textStyle
        urwid.Pile.__init__(self, self.build())

    def build(self):
        """
        Creates the subwidgets of the components and stiches them together for the final render.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.editLabel = urwid.AttrWrap(urwid.Text(
            f'{self.label}', 'left'), self.labelStyle)
        self.editInput = urwid.Edit('', '')

        editWithAttr = urwid.AttrWrap(self.editInput, self.textStyle)

        self.refresh()
        return [self.editLabel, editWithAttr]

    def refresh(self):
        """
        Updates the component underlying widget display values based on the model changing

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.editInput.set_edit_text(str(getattr(self.model, self.attribute)))
