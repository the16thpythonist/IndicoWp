import datetime
import tabulate


class SimpleEventTextView:

    def __init__(self, event):
        self.event = event

    def __str__(self):
        return self.get_string()

    def get_string(self):
        string = ''.join([
            self._description_string(),
            self._location_string(),
            self._time_string(),
            self._creator_string()
        ])
        return string

    def _creator_string(self):
        string = (
            'Creator:\n'
            '   first name: {}\n'
            '   last name:  {}\n'
            '   id:         {}\n'
            '   affiliation:{}\n'
        ).format(
            self.event.creator.first_name,
            self.event.creator.last_name,
            self.event.creator.id,
            self.event.creator.affiliation
        )
        return string

    def _time_string(self):
        string = (
            'start time: {}\n'
        ).format(
            self.event.datetime.strftime('at %H:%M on %d th %m')
        )
        return string

    def _description_string(self):
        string = (
            'type:          {}\n'
            'title:         {}\n'
            'description:   {}\n'
        ).format(
            self.event.type,
            self.event.title,
            self.event.description
        )

        return string

    def _location_string(self):
        string = (
            'Location:\n'
            '   location:   {}\n'
            '   address:    {}\n'
        ).format(
            self.event.location,
            self.event.address
        )
        return string


class SimpleEventsTableView:
    """
    :ivar events: The list of events, that is supposed to be displayed by the view object
    :ivar event: The current event. Internally there is a loop through the list of events and methods of this class
        operate on this variable.
    :ivar max_length: The max length of characters allowed for one column of the table

    :cvar ORDER: A list of strings to be used as headers for the table.
        Reordering this list, will reorder the structure of the table
    :cvar DATETIME_FORMAT: The format string for the datetime string
    """
    ORDER = ['TITLE', 'TYPE', 'STARTING', 'CREATOR', 'LOCATION']
    DATETIME_FORMAT = '%d %B %Y, %H:%M:%S'

    def __init__(self, event_list, max_length=50):
        self.events = event_list
        self.event = None

        self.max_length = max_length

    def __str__(self):
        return self.get_string()

    def get_string(self):
        """
        The actual view string

        :return: string
        """
        table_list = self.table_list()
        string = tabulate.tabulate(table_list, headers=self.ORDER, tablefmt='fancy_grid')
        return string

    def table_list(self):
        """
        The list of rows for the table, which contains the row lists, each containing the items in the order specified
        by the class variable ORDER

        :return: [[string]]: A "matrix" structure of strings to display in the table
        """
        table_list = []
        for self.event in self.events:
            rows = self._event_rows()
            table_list.append(rows)
        return table_list

    def _event_rows(self):
        """
        The row list of the current event. The items are sorted by the ORDER variable given.

        :return: [string] The list of string items to be displayed in the table cells
        """
        # Getting the unordered dict, that assigns each cell item to one of the Header strings
        row_dict = self._event_row_dict()
        # Sorting the items into a list, that follows the same oder as the header
        row_list = []
        for key in self.ORDER:
            row_list.append(row_dict[key])
        return row_list

    def _event_row_dict(self):
        """
        The row dict for the current event. The items are sorted as values to the keys, which are the strings of the
        header items.

        :return: {string: string}
        """
        row_dict = {
            'TITLE': self._title_limited(),
            'TYPE': self.event.type,
            'STARTING': self._datetime_string(),
            'CREATOR': self._creator_full_name(),
            'LOCATION': self.event.location
        }
        return row_dict

    def _datetime_string(self):
        """
        The date & time of the current event, formatted by the format given as the class variable 'DATETIME_FORMAT'

        :return: string
        """
        return self.event.datetime.strftime(self.DATETIME_FORMAT)

    def _title_limited(self):
        """
        The title of the event, but stripped to the maximum number of character for the width of one column, if needed

        :return: string
        """
        if len(self.event.title) >= self.max_length:
            return '{}...'.format(self.event.title[:self.max_length])
        return self.event.title

    def _creator_full_name(self):
        """
        The full name of the creator of the event, separated by comma

        :return: string
        """
        return '{}, {}'.format(
            self.event.creator.last_name,
            self.event.creator.first_name
        )