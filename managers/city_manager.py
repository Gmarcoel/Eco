from managers.manager import Manager


class CityManager(Manager):
    city = None
    world = None

    def __init__(self, city, world):
        super().__init__(city)
        self.city = city
        self.world = world
    
    def do(self):
        self.restart_sold_terrain()
        self.census()

    def restart_sold_terrain(self):
        self.city.sold_terrain = 0
    
    def change_sold_terrain(self, amount):
        self.city.sold_terrain += amount
    
    population = 0
    deaths = 0
    borns = 0
    deaths_by_hunger = 0

    last_borns = [0]
    last_deaths = [0]

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
            