from managers.manager import Manager


class CityManager(Manager):
    city = None
    world = None

    def __init__(self, city, world):
        super().__init__(city)
        self.city = city
        self.world = world