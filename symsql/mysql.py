import symex.fuzzy as fuzzy

class Table():

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def select(self, columns, where=None):
        return str(Select(self.name, columns, where))

class Select():

    def __init__(self, table, columns, where):
        self.table = self.sanity(table)
        self.columns = self.sanity(columns)
        self.where = self.sanity(where)

    def __str__(self):
        if self.where == None:
            return "SELECT '" + self.columns + "' FROM '" + self.table + "'"
        else:
            return "SELECT '" + self.columns + "' FROM '" \
                + self.table + "' WHERE '" + self.where + "'"

    def sanity(self, raw_str):
        if raw_str == None:
            return None
        sanity_str = raw_str
        if len(raw_str) < 50:
            # drop '"'
            sanity_str = sanity_str.replace('"', '')
            # drop "'"
            sanity_str = sanity_str.replace("'", "")
        return sanity_str       
