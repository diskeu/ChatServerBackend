from src.utils.type_helpers import to_int
from src.settings import settings


def configuration_parse():
    """
    ### Returns a mysql connection object ###
    
    Connects to mysql via the file location and mysql - user name provided
    in the .env file. If no user is provided DEFAULT will be used.

    :return: returns a mysql connection object
    :rtype: aio_MySQLConnection
    """

    # Loading Configurations
    def new_section(line: str, confg_dict: dict, cur_section_name: str) -> bool:
        """If the line contains a new section, return True; otherwise, return None and add the values to the section."""
        if line == " " or line == "\n": return False
        elif "[" in line: return True
        else:
            try:
                k, v = line.split("=")
                k, v = to_int(k.strip()), to_int(v.strip())
                confg_dict[cur_section_name][k] = v
            except ValueError:
                raise ValueError("Can't unbound line, no key-value couple")
        return False
        
    
    def create_section(line: str, confg_dict: dict) -> str:
        """Creates a section, in the confg_dict"""
        section_name = line.strip()                 # removing (trailing & leading) whitespaces and line breaks
        section_name = section_name.strip("[]")     # removing parentheses
        confg_dict[section_name] = {}
        return section_name
    
    def config_file_parser(confg_f_lines: list) -> dict[str, dict]:
        """Creates a dictionary from the lines of a config file"""
        confg_dict: dict = {}
        cur_section: bool = False
        for line in confg_f_lines:
            if cur_section:
                if new_section(line=line, confg_dict=confg_dict, cur_section_name=section_name):
                    section_name = create_section(line=line, confg_dict=confg_dict)

            elif "[" in line:
                section_name = create_section(line=line, confg_dict=confg_dict)
                cur_section = True
        return confg_dict

    # Getting lines from the config file
    try:
        with open(settings.MYSQL_CONFIG_FILE, "r") as confg_f:
            confg_f_lines: list = confg_f.readlines()
    except FileNotFoundError:
        mysql_connection_logger.exception("Can't open file")
    
    # Calling function to parse lines into dictionary format
    confg_dict = config_file_parser(confg_f_lines)

    # Combining both dictionarys
    confg: dict = confg_dict.get("DEFAULT")
    if settings.MYSQL_USER_NAME:
        user: dict = confg_dict.get(settings.MYSQL_USER_NAME)
        confg = confg | user

    return confg