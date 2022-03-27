from entity import Entity


class Proyect():
    entity = None
    name = ""
    money = 0
    resources = {}
    time = 1

    def __init__(self, name="", entity=None, money=0, resources={}, time=1):
        self.name = name
        self.entity = entity
        self.money = money
        self.resources = resources
        self.time = time

    def __str__(self):
        return f"Proyecto {self.name} Falta: Dinero {self.money}, recursos {self.resources}"

    def accomplish(self, entity):
        if entity.money >= self.money:
            entity.money = round(entity.money - self.money,2)
            self.money = 0
        completed = []
        for key in self.resources:
            if key not in entity.items:
                entity.items[key] = 0
            if entity.items[key] >= self.resources[key]:
                entity.items[key] -= self.resources[key]
                self.resources[key] = 0
                completed.append(key)

            else:
                self.resources[key] -= entity.items[key]
                entity.items[key] = 0
        # remove completed resources from the project
        for key in completed:
            del self.resources[key]
        if not self.resources and self.money == 0:
            return True
        return False
    


class State(Entity):
    name = ""
    governor = None
    cities = []
    population = []
    owned_bussiness = []
    proyects = []
    in_construction = []
    needed_resources = {}

    def __init__(self, name, governor, money):
        super().__init__(money=money)
        self.name = name
        self.governor = governor
        self.cities = []
        self.population = []
        self.owned_bussiness = []
        self.proyects = []
        self.in_construction = []
        self.needed_resources = {}

    def __str__(self):
        return f"{self.name} has {self.money} money"

    def add_city(self, city):
        self.cities.append(city)

    def remove_city(self, city):
        self.cities.remove(city)

    def add_infrastructure(self, city):
        inf = Proyect("infrastructure", city, 100, {'stone': 50}, 5)
        self.proyects.append(inf)

    def process_needed_resourcess(self, market):
        self.needed_resources = {}
        # add all resources from proyects to needed resources
        for res in self.needed_resources:
            res = 0
        for proyect in self.proyects:
            for key in proyect.resources:
                if not key in self.needed_resources:
                    self.needed_resources[key] = 0
                self.needed_resources[key] += proyect.resources[key]

        # create trades for all needed resources
        for key in self.needed_resources:
            t = self.trade(key, self.get_expected_price(
                key, market), False, self.needed_resources[key])
            market.add_trade(t)

    def work(self):
        for p in self.proyects:
            if p.accomplish(self):
                self.proyects.remove(p)
                self.in_construction.append(p)
        done = []
        for p in self.in_construction:
            if p.time <= 0:
                done.append(p)
                if p.name == "infrastructure":
                    p.entity.add_infrastructure(1)
            else:
                p.time -= 1
        # remove completed proyects from the project
        for p in done:
            self.in_construction.remove(p)
    
    def tax(self):
        tax = 0
        for c in self.cities:
            tax += c.tax()
        self.money = round(self.money + tax,2)
    

    def subsidize_entity(self, entity, amount):
        if self.money >= amount:
            self.subtract_money(amount)
            entity.add_money(amount)