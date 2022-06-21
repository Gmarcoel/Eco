from managers.business_manager import BusinessManager
from managers.person_manager import PersonManager
from managers.state_manager import StateManager
from managers.city_manager import CityManager
from managers.market_manager import MarketManager
from managers.job_market_manager import JobMarketManager
from managers.business_market_manager import BusinessMarketManager

from src.new import New

class World():
    new_people = []
    new_businesses = []
    new_states = []
    new_cities = [] 
    new_markets = []
    new_job_markets = []
    new_business_markets = []

    name = "World"


    people_managers = []
    business_managers = []
    states_managers = []
    cities_managers = []
    markets_managers = []
    job_markets_managers = []
    business_market_managers = []

    def __init__(self):
        self.new_people = []
        self.new_businesses = []
        self.new_states = []
        self.new_cities = []
        self.new_markets = []
        self.new_job_markets = []
        self.new_business_markets = []



        self.people_managers = []
        self.business_managers = []
        self.states_managers = []
        self.cities_managers = []
        self.markets_managers = []
        self.job_markets_managers = []
        self.business_market_managers = []

    
    def update(self):
        for p in self.new_people:
            self.people_managers.append(PersonManager(p.object, p.job_market, p.market, p.city, self))
        self.new_people = []
        for b in self.new_businesses:
            self.business_managers.append(BusinessManager(b.object, b.job_market, b.market, b.city, self))
        self.new_businesses = []
        for s in self.new_states:
            self.states_managers.append(StateManager(s.object, self, s.market, s.job_market))
        self.new_states = []
        for c in self.new_cities:
            self.cities_managers.append(CityManager(c.object, self))
        self.new_cities = []
        for m in self.new_markets:
            self.markets_managers.append(MarketManager(m.object, self))
        self.new_markets = []
        for j in self.new_job_markets:
            self.job_markets_managers.append(JobMarketManager(j.object, self))
        self.new_job_markets = []
        for u in self.new_business_markets:
            self.business_market_managers.append(BusinessMarketManager(u.object, self))
        self.new_business_markets = []

    
    def do(self):
        for p in self.people_managers:
            p.do()
            if p.person.dead:
                self.people_managers.remove(p)
        for b in self.business_managers:
            b.do()
        for s in self.states_managers:
            s.do()
        for c in self.cities_managers:
            c.do()
        for m in self.markets_managers:
            m.do()
        for j in self.job_markets_managers:
            j.do()
        for u in self.business_market_managers:
            u.do()
        


