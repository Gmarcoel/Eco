from  src.entity import Entity
from src.project import Project

import json


    


class State(Entity):
    name = ""
    governor = None
    cities = []
    population = []
    owned_bussiness = []
    projects = []
    in_construction = []
    needed_resources = {}

    def __init__(self, name, governor, money):
        super().__init__(money=money)
        self.name = name
        self.governor = governor
        self.cities = []
        self.population = []
        self.owned_bussiness = []
        self.projects = []
        self.in_construction = []
        self.needed_resources = {}

    def __str__(self):
        return f"{self.name} has {self.money} money"

    def add_city(self, city):
        self.cities.append(city)

    def remove_city(self, city):
        self.cities.remove(city)

    def add_infrastructure(self, city):
        with open("data/projects.json", "r") as f:
                        data = json.load(f)
                        # Get the resources needed for the project
                        resources = data["projects"]["infrastructure"]["resources"]
                        # Get the time needed for the project
                        time = int(data["projects"]["infrastructure"]["time"])
                        # Create the project
                        p = Project("infrastructure", city, self, 0, resources, time)
                        # Add the project to the list of projects
                        self.projects.append(p)
        # inf = Project("infrastructure", city, self, 100, {'stone': 50}, 5)
        # self.projects.append(inf)

    def process_needed_resourcess(self, market):
        # add all resources from projects to needed resources
        for res in self.needed_resources:
            res = 0
        for project in self.projects:
            for key in project.resources:
                if not key in self.needed_resources:
                    self.needed_resources[key] = 0
                self.needed_resources[key] += project.resources[key]

        # create trades for all needed resources
        for key in self.needed_resources:
            t = self.trade(key, self.get_expected_price(
                key), False, self.needed_resources[key])
            market.add_trade(t)

    def work(self):
        for p in self.projects:
            if p.accomplish(self):
                self.projects.remove(p)
                self.in_construction.append(p)
        done = []
        for p in self.in_construction:
            if p.time <= 0:
                done.append(p)
                if p.name == "infrastructure":
                    p.entity.add_infrastructure(1)
            else:
                p.time -= 1
        # remove completed projects from the project
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