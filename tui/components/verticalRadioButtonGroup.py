import urwid


class VerticalRadioButtonGroup(urwid.Pile):
    """
    The VerticalRadioButtonGroup component represents a list of radio buttons stacked vertically.
    """

    def __init__(self, model, attribute, labelOptions, group, modelRefreshFunction):
        """
        Parameters
        ----------
        model : ConfigurationModel
            The model that this component is linked to.
        attribute : str
            The attribute in the model that this component is linked to. i.e. self.mode['algorithm']
        labelOptions : array
            An array that contains the text values to display for each button
        group : str
            An identifier to uniquely identify a group of radio buttons
        modelRefreshFunction : str
            A callback function that can be called when the radio button value changes in the component
        """
        self.model = model
        self.modelRefreshFunction = modelRefreshFunction
        self.attribute = attribute
        urwid.Pile.__init__(self, self.build(labelOptions, group))

    def build(self, labelOptions, group):
        """
        Creates the subwidgets of the components and stiches them together for the final render.

        Parameters
        ----------
        labelOptions : array
            An array that contains the text values to display for each button
        group : str
            An identifier to uniquely identify a group of radio buttons

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.buttons = []

        for txt in labelOptions:
            r = urwid.RadioButton(group, txt, False)
            urwid.connect_signal(
                r, 'change', self.on_radio_change, self.attribute)
            urwid.connect_signal(
                r, 'change', self.modelRefreshFunction, self.attribute)
            ra = urwid.AttrWrap(r, 'button normal', 'button select')
            self.buttons.append(ra)

        self.refresh()
        return self.buttons

    def on_radio_change(self, button, state, groupName):
        """
        When the radio button value changes update the unerlying model to keep it in sync with the UI

        Parameters
        ----------
        button : str
            The value of the radio button selected. i.e. 'crls' or 'prerecorded'
        state : boolean
            True if the radio is selected, False otherwise
        groupName : str
            The name of the group the radio button selected belongs to

        Returns
        -------
        None

        Raises
        ------
        None
        """
        if state:
            setattr(self.model, self.attribute, button.get_label())

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
        for button in self.buttons:
            if(button.get_label() == getattr(self.model, self.attribute)):
                button.set_state(True)
            else:
                button.set_state(False)
