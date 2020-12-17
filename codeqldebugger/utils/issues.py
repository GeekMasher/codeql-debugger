class Issues:
    __ERRORS__ = []
    __WARNINGS__ = []

    @staticmethod
    def getErrors():
        return Issues.__ERRORS__

    @staticmethod
    def addError(id, message, data=""):
        Issues.__ERRORS__.append({"id": id, "msg": message, "data": data})

    @staticmethod
    def getWarnings():
        return Issues.__WARNINGS__

    @staticmethod
    def addWarning(id, message, data=""):
        Issues.__WARNINGS__.append({"id": id, "msg": message, "data": data})
