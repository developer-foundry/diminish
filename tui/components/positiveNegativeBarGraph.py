from urwid.compat import ord2, with_metaclass
import urwid
from urwid.util import get_encoding_mode
from urwid import Text
from urwid.canvas import CanvasCombine
BOX = 'box'


class PositiveNegativeGraphError(Exception):
    pass


class PositiveNegativeBarGraph(with_metaclass(urwid.BarGraphMeta, urwid.Widget)):
    _sizing = frozenset([BOX])
    maxcol = None
    ignore_focus = True

    def __init__(self, attlist, hatt=None):
        """
        Create a bar graph with the passed display characteristics.
        see set_segment_attributes for a description of the parameters.
        """

        self.set_segment_attributes(attlist, hatt)
        self.set_data([], 1, 0)
        self.set_bar_width(None)

    def set_segment_attributes(self, attlist, hatt=None):
        """
        :param attlist: list containing display attribute or
                        (display attribute, character) tuple for background,
                        first segment, and optionally following segments.
                        ie. len(attlist) == num segments+1
                        character defaults to ' ' if not specified.
        :param hatt: list containing attributes for horizontal lines. First
                    element is for lines on background, second is for lines
                    on first segment, third is for lines on second segment
                    etc.

        eg: set_segment_attributes( ['no', ('unsure',"?"), 'yes'] )
        will use the attribute 'no' for the background (the area from
        the top of the graph to the top of the bar), question marks
        with the attribute 'unsure' will be used for the topmost
        segment of the bar, and the attribute 'yes' will be used for
        the bottom segment of the bar.
        """
        self.attr = []
        self.char = []
        if len(attlist) < 2:
            raise PositiveNegativeGraphError(
                "attlist must include at least background and seg1: %r" % (attlist,))
        assert len(attlist) >= 2, 'must at least specify bg and fg!'
        for a in attlist:
            if type(a) != tuple:
                self.attr.append(a)
                self.char.append(' ')
            else:
                attr, ch = a
                self.attr.append(attr)
                self.char.append(ch)

        self.hatt = []
        if hatt is None:
            hatt = [self.attr[0]]
        elif type(hatt) != list:
            hatt = [hatt]
        self.hatt = hatt

    def set_data(self, bardata, top, bottom):
        """
        Store bar data, bargraph top and horizontal line positions.

        bardata -- a list of bar values.
        top -- maximum value for segments within bardata

        bar values are [ segment1, segment2, ... ] lists where top is
        the maximal value corresponding to the top of the bar graph and
        segment1, segment2, ... are the values for the top of each
        segment of this bar.  Simple bar graphs will only have one
        segment in each bar value.

        Eg: if top is 100 and there is a bar value of [ 80, 30 ] then
        the top of this bar will be at 80% of full height of the graph
        and it will have a second segment that starts at 30%.
        """
        self.data = bardata, top, bottom
        # pylint: disable=no-member
        self._invalidate()

    def _get_data(self, size):
        """
        Return (bardata, top, bottom)
        This function is called by render to retrieve the data for
        the graph. It may be overloaded to create a dynamic bar graph.

        This implementation will truncate the bardata list returned
        if not all bars will fit within maxcol.
        """
        (maxcol, maxrow) = size
        bardata, top, bottom = self.data
        widths = self.calculate_bar_widths((maxcol, maxrow), bardata)

        if len(bardata) > len(widths):
            return bardata[:len(widths)], top, bottom

        return bardata, top, bottom

    def set_bar_width(self, width):
        """
        Set a preferred bar width for calculate_bar_widths to use.

        width -- width of bar or None for automatic width adjustment
        """
        assert width is None or width > 0
        self.bar_width = width
        # pylint: disable=no-member
        self._invalidate()

    def calculate_bar_widths(self, size, bardata):
        """
        Return a list of bar widths, one for each bar in data.

        If self.bar_width is None this implementation will stretch
        the bars across the available space specified by maxcol.
        """
        (maxcol, _) = size

        if self.bar_width is not None:
            return [self.bar_width] * min(
                len(bardata), maxcol // self.bar_width)

        if len(bardata) >= maxcol:
            return [1] * maxcol

        widths = []
        grow = maxcol
        remain = len(bardata)
        for _ in bardata:
            w = int(float(grow) / remain + 0.5)
            widths.append(w)
            grow -= w
            remain -= 1
        return widths

    def selectable(self):
        """
        Return False.
        """
        return False

    def calculate_display(self, size):
        """
        Calculate display data.
        """
        (maxcol, maxrow) = size
        # pylint: disable=no-member
        bardata, top, bottom = self.get_data((maxcol, maxrow))
        widths = self.calculate_bar_widths((maxcol, maxrow), bardata)

        # initialize matrix
        halfwayScaled = maxrow // 2
        # use overscore if the item is above 0 or underscore if below 0, dash if on 0
        disp = [['\u203E' if i < halfwayScaled else '-' if i ==
                 halfwayScaled else '_' for j in range(maxcol)] for i in range(maxrow)]

        def split(word):
            return [char for char in word]

        # first column should be used for scale and
        if(len(bardata) > 0):
            formatString = '{:0.3f}' if type(
                bardata[0][0]) is float else '{:4d}'
            for i in range(maxrow):
                value = self.calculate_scale(maxrow, top, i)
                stringVal = ''
                if(value >= 0):
                    stringVal = ' ' + formatString.format(value)[1:]
                else:
                    stringVal = '-' + formatString.format(value)[2:]

                characters = split(stringVal)
                for cIndex, c in enumerate(characters):
                    disp[i][cIndex] = c

        # add bar entries to matrix
        bar_positions = self.get_bar_positions(
            bardata, top, bottom, widths, maxrow)
        disp = self.update_matrix_with_bar_positions(bar_positions, disp)
        return disp

    def calculate_scale(self, maxrow, top, row):
        halfwayScaled = maxrow // 2
        unit = top / halfwayScaled

        unitsAway = (halfwayScaled - row)
        return unitsAway * unit

    def update_matrix_with_bar_positions(self, bar_positions, disp):
        for i in range(len(disp)):
            for j in range(len(disp[i])):
                if(self.location_is_a_bar(bar_positions, i, j)):
                    disp[i][j] = 'X'

        return disp

    def location_is_a_bar(self, bar_positions, row, col):
        res = False
        if(bar_positions[row] is not None):
            for _, colStart, _ in bar_positions[row]:
                if colStart == col:
                    res = True

        return res

    def render(self, size, focus=False):
        """
        Render BarGraph.
        """
        (maxcol, maxrow) = size
        self.maxcol = maxcol
        disp = self.calculate_display((maxcol, maxrow))

        combinelist = []
        for row in disp:
            l = []
            for _, currLoc in enumerate(row, start=0):
                if currLoc == 'X':
                    # bar
                    a = self.attr[1]
                    t = self.char[0]
                elif currLoc == ' ':
                    a = None
                    t = currLoc
                else:
                    a = None
                    t = currLoc  # this would likely be printing the scale on the left hand side

                l.append((a, t))
            c = Text(l).render((maxcol,))
            assert c.rows() == 1, "Invalid characters in BarGraph!"
            combinelist += [(c, None, False)]

        canv = CanvasCombine(combinelist)
        return canv

    def scale_bar_values(self, bar, top, bottom, maxrow):
        """
        Return a list of bar values aliased to integer values of maxrow.
        maxrow is the maximum colums used in the terminal
        """

        results = []

        for v in bar:
            if(v >= 0):
                start = maxrow // 2  # you want to start positive bar values at the middle of the widget
                end = start - int(((float(v) * (maxrow // 2)) / top) + 0.5)
                results.append((start, end))
            else:
                # you want to start the negative bar values at the last row in the widget
                start = maxrow // 2 + 1
                end = start + int(((float(v) * (maxrow // 2)) / bottom) + 0.5)
                results.append((start, end))

        return results

    def get_bar_positions(self, bardata, top, bottom, bar_widths, maxrow):
        """
        Calculate a rendering of the bar graph described by data, bar_widths
        and height.

        bardata -- bar information with same structure as BarGraph.data
        top -- maximal value for bardata segments
        bar_widths -- list of integer column widths for each bar
        maxrow -- rows for display of bargraph

        Returns a structure as follows:
        [ ( y_count, [ ( bar_type, width), ... ] ), ... ]

        The outer tuples represent a set of identical rows. y_count is
        the number of rows in this set, the list contains the data to be
        displayed in the row repeated through the set.

        The inner tuple describes a run of width characters of bar_type.
        bar_type is an integer starting from 0 for the background, 1 for
        the 1st segment, 2 for the 2nd segment etc..

        This function should complete in approximately O(n+m) time, where
        n is the number of bars displayed and m is the number of rows.
        """

        assert len(bardata) == len(bar_widths)

        # build intermediate data structure
        rows = [None] * maxrow

        def add_segment(seg_num, col, rowStart, rowEnd, width, rows=rows):
            # iterate between rowStart and rowEnd filling the rows
            # check and see if this is a positive bar. if it is you have
            # to use a negative step to count down because row 0 is at the top
            step = 1
            if(rowEnd < rowStart):
                step = -1

            for rowIndex in range(rowStart, rowEnd + step, step):
                if rows[rowIndex] is None:
                    rows[rowIndex] = []
                rows[rowIndex].append((seg_num, col, col + width))

        col = 6  # has to be 6 to account for the scale column being in column 0
        barnum = 0
        for bar in bardata:
            width = bar_widths[barnum]
            if width < 1:
                continue
            # loop through in reverse order
            segments = self.scale_bar_values(bar, top, bottom, maxrow)
            for k in range(len(bar) - 1, -1, -1):
                # each segment has a start and end in the form of a tuple
                sStart, sEnd = segments[k]

                if sEnd >= maxrow:
                    sEnd = maxrow - 1
                if sEnd < 0:
                    sEnd = 0

                add_segment(k + 1, col, sStart, sEnd, width)
            col += width
            barnum += 1
        return rows
