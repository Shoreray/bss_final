class Table():

    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return self.__name

    def select(self, columns, where=None):
        return str(Select(self.__name, columns, where))

class Select():

    def __init__(self, table, columns, where):
        self.__table = self.sanity(table)
        self.__columns = self.sanity(columns)
        self.__where = self.sanity(where)

    def __str__(self):
        if self.__where == None:
            return "SELECT '" + self.__columns + "' FROM '" + self.__table + "'"
        else:
            return "SELECT '" + self.__columns + "' FROM '" \
                + self.__table + "' WHERE '" + self.__columns + " = " + self.__where + "'"

    def sanity(self, raw_str):
        if raw_str == None:
            return None
        sanity_str = raw_str
        if len(raw_str) <= 50:
            # drop '"'
            sanity_str = sanity_str.replace('"', "")
            # drop "'"
            sanity_str = sanity_str.replace("'", "")
        return sanity_str       
