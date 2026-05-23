class ENVNotFoundError(Exception):
    """Raised when the .env file is not found"""
    def __init__(self):
        super().__init__(".env file not found")

class MysqlConfigLocationVariableNotFoundError(Exception):
    """Raised when the MYSQL_CONFIG_FILE variableis not found"""
    def __init__(self):
        super().__init__("MYSQL_CONFIG_FILE variable not found")