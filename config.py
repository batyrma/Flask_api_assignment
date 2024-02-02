from configparser import ConfigParser


def config(filename="C:\\Users\Knopka\PycharmProjects\pythonProject2\\venv\Home_task\DB_start\data.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        # items() ==> key:value
        for param in params:
            db[param[0]] = param[1]
            #db['host']='localhost'
    else:
        raise Exception(f"Section {section} is not found in the {filename}")
    return db

