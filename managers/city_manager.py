from managers.manager import Manager
from src.new import New
from src.business_market import BusinessMarket


class CityManager(Manager):
    city = None
    world = None
    population = 0
    deaths = 0
    borns = 0
    deaths_by_hunger = 0

    last_borns = [0]
    last_deaths = [0]


    def __init__(self, city, world):
        super().__init__(city)
        self.city = city
        self.world = world

        # Si no existe crear el business market de la ciudad
        if not self.city.business_market:
            market = BusinessMarket(self.city.name + " Business Market", None, 0, 0.1)
            self.world.new_business_markets.append(New(market, self.city, None, None))
            self.city.business_market = market
    
    def do(self):
        self.restart_sold_terrain()
        self.census()
        self.check_business_status()

    def restart_sold_terrain(self):
        self.city.sold_terrain = 0
    
    def change_sold_terrain(self, amount):
        self.city.sold_terrain += amount
    
    def check_business_status(self):
        aux = []
        for business in self.city.businesses:
            if business.status == "closed":
                self.city.closed_businesses.append(business)
            else:
                aux.append(business)
        self.city.businesses = aux
        aux = []
        for business in self.city.closed_businesses:
            if business.status == "open":
                self.city.businesses.append(business)
            else:
                aux.append(business)
        self.city.closed_businesses = aux


    def census(self):
        population = 0
        deaths = 0
        deaths_by_hunger = 0
        borns = 0
        dead = []
        for person in self.city.people:
            if person.dead:
                deaths += 1
                if person.dead_by_hunger:
                    deaths_by_hunger += 1
                dead.append(person)
            else:
                if person.age == 0:
                    borns += 1
                population += 1
        self.population = population
        self.deaths = deaths
        self.deaths_by_hunger = deaths_by_hunger
        self.borns = borns
        for person in dead:
            self.city.people.remove(person)
        
        self.last_borns.append(borns)
        self.last_deaths.append(deaths)
        if len(self.last_borns) > 100:
            self.last_borns.pop(0)
        if len(self.last_deaths) > 100:
            self.last_deaths.pop(0)
            