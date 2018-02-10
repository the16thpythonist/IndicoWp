import logging
import datetime
import pathlib
import os

# The path to the IndicoWp main folder, that contains all the modules
PATH = os.path.dirname(os.path.realpath(__file__))


class LoggingController:
    """
    Handles the log file management.
    Log files are being created for each day, with the date being part of the name of the log file.
    This class creates a new log file if there is none and init's the logging Logger for the file.
    Writes additional information into the log files at the beginning and end of a session.

    :cvar DATE_FORMAT: The datetime format string for dates only, used for the file names
    :cvar DATETIME_FORMAT: The datetime format string for date & time, used inside the log files
    :ivar logging_folder: The string name of the sub folder in which the logs are stored
    :ivar log_name: The name of the log file for the current day
    :ivar path: The pathlib.Path object to the folder in which the logs are located
    """
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self):

        # The name of the folder which will contain the log files
        # TODO: Make this a part of the config.ini file
        self.logging_folder = 'logging'
        self.log_name = 'test.log'

        # The path object pointing to the folder with the logs
        self.path = pathlib.Path(PATH) / self.logging_folder / ''

    def init(self):
        """
        To be called before there is any attempt at writing log files.
        This creates a log file if there is none and also fixes the logging.logger on that file.

        :return: void
        """
        self._prepare_log_file()

    def close(self):
        """
        Writes a closing sentence into the log file.

        :return: void
        """
        self._post_process_log_file()

    def _prepare_log_file(self):
        """
        If there is no log file yet creates new one and appends a line, that states at which point a new session was
        started. Also inits the logging.BasicLogger on the newly created file.

        :return: void
        """
        datetime_string = self._current_datetime_string()

        line_string = '\n\nSTARTING NEW LOGGING SESSION @ "{}"\n\n'.format(datetime_string)

        file_mode = 'a'
        with self.path.open(mode=file_mode) as file:
            file.write(line_string)

        file_path = str(self.path)
        logging.basicConfig(
            level=logging.INFO,
            filename=file_path,
            filemode='a',
            format='%(asctime)s %(name)-40s %(levelname)-8s %(message)s'
        )

    def _post_process_log_file(self):
        """
        Writes a new line into the log file, that signals at which point the session ended

        :return: void
        """
        datetime_string = self._current_datetime_string()

        line_string = '\n\nCLOSING SESSION @ "{}"\n\n'.format(datetime_string)

        with self.path.open(mode='a') as file:
            file.write(line_string)

    def _current_datetime_string(self):
        """
        Creates a datetime object for the current time of the method execution and formats the string based on the
        format, that is given as static field of the logging controller.

        :return: The string of the current date & time
        """
        datetime_object = datetime.datetime.now()
        datetime_string = datetime_object.strftime(self.DATETIME_FORMAT)

        return datetime_string

