from html import entities
from  src.business import Business
from  src.person import Person

class City:
    name = ""
    entities = []
    businesses = []
    people = []
    people_tax_rate = 0.2
    businesses_tax_rate = 0.2
    money = 0
    infrastructure = 10
    infrastructure_price = 100
    markets = []
    state = None

    # Law related attributes
    minimum_wage = 0
    maximum_price = {}
    minimum_price = {}

    def __init__(self, name = "", businesses = [], people = [], tax_rate = 0.1, money = 1000, state = None):
        self.entities = []
        self.businesses = []
        self.people = []
        self.markets = []
        self.name = name
        self.businesses = businesses
        self.people = people
        self.tax_rate = tax_rate
        self.money = money
        self.state = state
        self.entities = self.businesses + self.people

        self.maximum_price = {}
        self.minimum_price = {}

    
    def __str__(self):
        return f"{self.name} has {len(self.businesses)} businesses and {len(self.people)} people and {self.infrastructure} infrastructure"

    def add_infrastructure(self, amount):
        self.infrastructure += amount
    
    def add_market(self, market):
        self.businesses.append(market)

    def add_business(self, business):
        self.businesses.append(business)
    
    def add_person(self, person):
        self.people.append(person)
    
    def get_person_by_name(self, name):
        for person in self.people:
            if person.name == name:
                return person
        return None
    
    def get_business_by_name(self, name):
        for business in self.businesses:
            if business.name == name:
                return business
        return None
    
    def get_people_by_job(self, job):
        people = []
        for person in self.people:
            if person.job == job:
                people.append(person)
        return people

    def tax(self):
        taxes = 0
        for person in self.people:
            taxes = round(taxes + person.tax(self.people_tax_rate), 2)
        for business in self.businesses:
            taxes = round(taxes + business.tax(self.businesses_tax_rate), 2)
        return taxes
    
    sold_terrain = 0
    def buy_terrain(self, entity):
        if self.infrastructure > 0 and entity.money > self.infrastructure_price and self.sold_terrain < 3:
            entity.subtract_money(self.infrastructure_price)
            self.add_money(self.infrastructure_price)
            self.infrastructure -= 1
            self.sold_terrain += 1
            return True
        return False
    
    def add_money(self, money):
        self.money = round(money + self.money, 2)
    
    def subtract_money(self, money):
        self.money = round(self.money - money, 2)

    


    # Law related methods
    def set_people_tax(self, tax):
        self.people_tax_rate = tax
    
    def set_businesses_tax(self, tax):
        self.businesses_tax_rate = tax
    
    def set_minimum_wage(self, wage):
        self.minimum_wage = wage
    
    def set_maximum_price(self, price, resource):
        self.maximum_price[resource] = price
    
    def set_minimum_price(self, price, resource):
        self.minimum_price[resource] = price
    
    def remove_maximum_price(self, resource):
        del self.maximum_price[resource]
    
    def remove_minimum_price(self, resource):
        del self.minimum_price[resource]
    



