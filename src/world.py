from managers.business_manager import BusinessManager
from managers.person_manager import PersonManager
from managers.state_manager import StateManager
from managers.city_manager import CityManager

from src.new import New

class World():
    new_people = []
    new_businesses = []
    new_states = []
    new_cities = [] 
    name = "World"


    people_managers = []
    business_managers = []
    states_managers = []
    cities_managers = []

    def __init__(self):
        self.new_people = []
        self.new_businesses = []
        self.new_states = []
        self.new_cities = []
        self.people_managers = []
        self.business_managers = []
        self.states_managers = []
        self.cities_managers = []
    
    def update(self):
        for p in self.new_people:
            self.people_managers.append(PersonManager(p.object, p.job_market, p.market, p.city, self))
        self.new_people = []
        for b in self.new_businesses:
            self.business_managers.append(BusinessManager(b.object, b.job_market, b.market, b.city, self))
        self.new_businesses = []
        for s in self.new_states:
            self.states_managers.append(StateManager(s.object, self, s.market))
        self.new_states = []
        for c in self.new_cities:
            self.cities_managers.append(CityManager(c.object, self))
        self.new_cities = []
    
    def do(self):
        for p in self.people_managers:
            p.do()
            if p.person.dead:
                self.people_managers.remove(p)
        for b in self.business_managers:
            b.do()
            if b.business.status == "closed":
                self.business_managers.remove(b)
        for s in self.states_managers:
            s.do()
        

