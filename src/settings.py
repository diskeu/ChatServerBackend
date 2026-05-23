from pathlib import Path
from dotenv import load_dotenv
from src.exceptions import ENVNotFoundError
import os

# class to handle environment variables
class Settings():
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        os.environ["BASE_DIR"] = str(self.BASE_DIR)
        if not load_dotenv(dotenv_path=self.BASE_DIR / ".env", override=False):
            raise ENVNotFoundError()

    @property
    def MYSQL_CONFIG_FILE(self):
        if not hasattr(self, "_MYSQL_CONFIG_FILE"):
            self._MYSQL_CONFIG_FILE = os.getenv("MYSQL_CONFIG_FILE")
            if self._MYSQL_CONFIG_FILE is None:
                raise MysqlConfigLocationVariableNotFoundError
        return self._MYSQL_CONFIG_FILE

    @property
    def MYSQL_LOGFILE(self):
        if not hasattr(self, "_MYSQL_LOGFILE"):
            self._MYSQL_LOGFILE = os.getenv(
                "MYSQL_LOGFILE",
                default=(
                    Path(os.getenv("BASE_DIR", default=Path("../Logs").resolve())) / "mysql.log"
                )
            )
        return self._MYSQL_LOGFILE
    
    @property
    def MYSQL_USER_NAME(self):
        if not hasattr(self, "_MYSQL_USER_NAME"):
            self._MYSQL_USER_NAME = os.getenv("MYSQL_USER_NAME")
        return self._MYSQL_USER_NAME
    
    @property
    def BASE_LOGFILE(self):
        if not hasattr(self, "_BASE_LOGFILE"):
            self._BASE_LOGFILE = os.getenv(
                "BASE_LOGFILE",
                default=(
                    Path(os.getenv("BASE_DIR", default="../Logs")) / "base_log.log"
                )
            )
        return self._BASE_LOGFILE

settings = Settings()