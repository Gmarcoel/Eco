from numpy import minimum
from  src.entity import Entity
from src.project import Project

from managers.business_manager import create_business

import json
import random


    


class State(Entity):
    name = ""
    governor = None
    cities = []
    population = []
    projects = []
    in_construction = []
    needed_resources = {}

    # Law related attributes
    minimum_wage = 0
    maximum_price = {}
    minimum_price = {}
    people_tax_rate = 0.2
    business_tax_rate = 0.2


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

        self.maximum_price = {}
        self.minimum_price = {}

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
    
    def add_project(self, city):
        if city.infrastructure <= 0: return
        city.infrastructure -= 1
        with open("data/projects.json", "r") as f:
            data = json.load(f)
            # Choose random project from list
            l = ["infrastructure", "farm", "mine", "sawmill", "constructor"]
            ran = random.choice(l)
            # Get the resources needed for the project
            resources = data["projects"][ran]["resources"]
            # Get the time needed for the project
            time = int(data["projects"][ran]["time"])
            # Create the project
            p = Project(ran, city, self, 0, resources, time)
            # Add the project to the list of projects
            self.projects.append(p)


    def process_needed_resourcess(self, market):
        # add all resources from projects to needed resources
        self.needed_resources = {}

        for project in self.projects:
            for key in project.resources:
                if not key in self.needed_resources:
                    self.needed_resources[key] = 0
                self.needed_resources[key] += project.resources[key]

        # create trades for all needed resources
        for key in self.needed_resources:
            if self.get_expected_price(key) <= self.money:
                # self.subtract_money(self.get_expected_price(key))
                t = self.trade(key, self.get_expected_price(
                    key), False, self.needed_resources[key])
                market.add_trade(t)

    def work(self, city):
        if self.governor:
            if self.governor.dead:
                self.governor = None

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
                    b = create_business(p.name, self, p.entity.money)
                    self.owned_bussiness.append(b)
                    # Add business to the city
                    city.businesses.append(b)
                    p.entity.add_business(b)
                    # Add .05 percent of state money to the business
                    amm = round(self.money * .05, 2)
                    self.subtract_money(amm)
                    b.add_money(amm)

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

    def set_governor(self, new_governor):
        self.governor = new_governor


    def set_people_tax(self, tax):
        self.people_tax_rate = tax
        for c in self.cities:
            c.set_people_tax(tax)
    
    def set_businesses_tax(self, tax):
        self.business_tax_rate = tax
        for b in self.owned_bussiness:
            b.set_businesses_tax(tax)
    
    def nationalize_business(self, business):
        owner = business.owner
        owner.businesses.remove(business)
        self.businesses.append(business)
        business.owner = self
    
    def set_minimun_wage(self, wage):
        self.minimum_wage = wage
        for c in self.cities:
            c.set_minimun_wage(wage)
    
    def set_maximum_price(self, price, resource):
        self.maximum_price[resource] = price
        for c in self.cities:
            c.set_maximum_price(price, resource)
    
    def set_minimum_price(self, price, resource):
        self.minimum_price[resource] = price
        for c in self.cities:
            c.set_minimum_price(price, resource)
    
    def remove_maximum_price(self, resource):
        del self.maximum_price[resource]
        for c in self.cities:
            c.remove_maximum_price(resource)
    
    def remove_minimum_price(self, resource):
        del self.minimum_price[resource]
        for c in self.cities:
            c.remove_minimum_price(resource)

    



