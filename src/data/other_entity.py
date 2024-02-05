from __init__ import Item, not_none

class Offer(Item):
    @not_none('id', 'title', 'state', 'description', 'location_type')
    def __init__(self,
                 id: int,
                 title: str,
                 state: str,
                 description: str,
                 location_type: str,
                 location):
        self.__id: int = id
        self.__title: str = title
        self.__state: str = state
        self.__description: str = description
        self.__location_type: str = location_type
        self.__location = location

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def state(self):
        return self.__state

    @property
    def description(self):
        return self.__description

    @property
    def location_type(self):
        return self.__location_type

    @property
    def location(self):
        return self.__location


class Skill:
    @not_none('id', 'name', 'type')
    def __init__(self,
                 id: int,
                 name: str,
                 type: str):
        self.__id: int = id
        self.__name: str = name
        self.__type: str = type

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type