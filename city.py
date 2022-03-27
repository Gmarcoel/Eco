from html import entities
from business import Business
from person import Person

class City:
    name = ""
    entities = []
    businesses = []
    people = []
    tax_rate = 0.1
    money = 0
    infrastructure = 10
    markets = []

    def __init__(self, name = "", businesses = [], people = [], tax_rate = 0.1, money = 1000):
        self.entities = []
        self.businesses = []
        self.people = []
        self.markets = []
        self.name = name
        self.businesses = businesses
        self.people = people
        self.tax_rate = tax_rate
        self.money = money
        self.entities = self.businesses + self.people

    
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
        for entity in self.entities:
            taxes = round(taxes + entity.tax(self.tax_rate), 2)
        return taxes

    # Functio to do a turn of all the people and businesses


