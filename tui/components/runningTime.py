import urwid
import time


class RunningTime(urwid.WidgetWrap):
    """
    The RunningTime component represents a box displaying seconds counting up from 0.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.startTime = time.time()
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        """
        Creates the subwidgets of the component and stiches them together for the final render.

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
        self.bigtext = urwid.BigText("", urwid.HalfBlock5x4Font())
        bt = urwid.Padding(self.bigtext, 'center', None)
        self.attribute = urwid.AttrWrap(bt, 'bigtextgood')
        bt = urwid.Filler(self.attribute, 'bottom', None, 7)
        bt = urwid.BoxAdapter(urwid.LineBox(bt, "Running Time (s)"), 7)

        return bt

    def refresh(self):
        """
        Updates the component underlying widget display values based on the system clock changing

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
        timePassed = f"{int(time.time() - self.startTime)}"
        self.bigtext.set_text(timePassed)
