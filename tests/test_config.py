from IndicoWp.config import PATH, LoggingController, Config

import pathlib
import shutil

import pytest


@pytest.fixture(scope='session')
def log_folder(request):
    # Creating log folder
    log_folder = 'logging_tests'
    log_path = pathlib.Path(PATH) / log_folder

    # Now we need to replace the value that specifies the logging folder in the config file
    config = Config.get_instance()
    config['LOGGING']['folder'] = log_folder

    if not log_path.is_dir():
        log_path.mkdir()

    def delete_log_folder():
        log_path_string = str(log_path)
        shutil.rmtree(log_path_string)

    request.addfinalizer(delete_log_folder)


@pytest.mark.usefixtures('log_folder')
def test_log_file_creation():
    # Creating the logging controller
    logging_controller = LoggingController()

    logging_controller.init()
    log_path = logging_controller.path
    assert log_path.exists() and log_path.is_file()

