from typing import Literal
from platformdirs import user_data_path

version: tuple[Literal[0], Literal[0], Literal[1]] = (0, 0, 1)
version_string: str = ".".join([str(each) for each in version])

APP_NAME = "Accountant"
APP_NAME_WITH_VERSION: str = APP_NAME + "@" + version_string

HOME = user_data_path() / APP_NAME_WITH_VERSION
DB_FOLDER = HOME / "Database"
DB_FILE_PATH = DB_FOLDER / f"{APP_NAME}_DB.csv"
LOG_FOLDER = HOME / str("Log" + "@" + version_string)
