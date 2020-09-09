class data:
    def __init__(self, Name, BadgeID, message):
        self.__Name = Name
        self.__BadgeID = BadgeID
        self.__message = message

    def getBadgeID(self):
        return self.__BadgeID

    def getName(self):
        return self.__Name

    def getMessage(self):
        return self.__message

