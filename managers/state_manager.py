from src.city import City
from src.state import State
from managers.manager import Manager
from managers.business_manager import create_business
from src import person
from src.project import Project
import json
import random
from src.person import Person

from src.new import New

class StateManager(Manager):
    world = None
    state = None
    market = None
    def __init__(self, state, world, market):
        super().__init__(state)
        self.state = state
        self.state.world = world
        self.market = market
    
    def do(self):

        self.tax()
        self.work()
        self.invest()
        self.buy_resources()

        self.propose_law()

        


    
    def tax(self):
        for c in self.state.cities:
            c.tax()
    
    def work(self):
        for c in self.state.cities:
            self.state.work(c)
    
    def invest(self):
        # randomize city order
        cities = self.state.cities
        random.shuffle(cities)
        for c in cities:
            if self.state.money > 50 and len(self.state.projects) < 3:
                if c.infrastructure < 5:
                    self.state.add_infrastructure(c)
                else:
                    self.state.add_project(c)
        
    def buy_resources(self):
        self.state.process_needed_resourcess(self.market)
    
    def pay_workers(self):
        if self.state.governor:
            dividend = round(self.state.money * 0.05,2)
            self.state.money = round(self.state.money - dividend,2)
            self.state.governor.money = round(self.governor.money + dividend,2)
    
    def propose_law(self):
        n = 6
        if self.state.minimum_price != {}:
            n += 1
        if self.state.maximum_price != {}:
            n += 1
        # random number 
        r = random.randint(1,n)
        if r == 1:
            # Set a random value between -0.1 and 0.1
            v = round(random.uniform(-0.1,0.1),2)
            # Add v to tax
            self.state.set_people_tax(round(self.state.people_tax_rate + v,2))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Proposed a people tax rate of {}".format(self.state.people_tax_rate))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        elif r == 2:
            # Set a random value between -0.1 and 0.1
            v = round(random.uniform(-0.1,0.1),2)
            # Add v to tax
            self.state.set_businesses_tax(round(self.state.business_tax_rate + v,2))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Proposed a business tax rate of {}".format(self.state.business_tax_rate))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        elif r == 3:
            i = 20
            bus = None
            while i > 0:
                # choose a random city
                c = random.choice(self.state.cities)
                # Choose a random business
                b = random.choice(c.businesses)
                # If business is not owned by state
                if not isinstance(b.owner, State):
                    bus = b
                    break
                i -= 1
            if bus:
                self.state.nationalize_business(bus)
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("Proposed to nationalize {}".format(bus.name))
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        elif r == 4:
            i = 20
            bus = None
            while i > 0:
                # choose a random city
                c = random.choice(self.state.cities)
                # Choose a random business
                b = random.choice(c.businesses)
                # If business is not owned by state
                if  isinstance(b.owner, State):
                    bus = b
                    break
                i -= 1
            if bus:
                # Select random person in city
                p = random.choice(c.people)
                # set owner of business to person
                bus.owner = p
                # Add business to person
                p.businesses.append(bus)
                # Remove business from state
                if bus in self.state.businesses: # ESTO TIENE ALGO QUE NO DEBERIA SER NECESARIO QUE MIEDO 
                    self.state.businesses.remove(bus)
                # self.state.businesses.remove(bus)
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("Proposed to privatize {}".format(bus.name))
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                
        elif r == 5:
            # Set a random value between market value of food * 2 and market value of food * 10
            if not r in self.market.database.average_price:
                return
            avg_food = self.market.database.average_price["food"]
            v = round(random.uniform( avg_food* 2, avg_food * 10),2)
            self.state.set_minimun_wage(v)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Proposed a minimum wage of {}".format(self.state.minimum_wage))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        elif r == 6:
            # Create a list with all resources
            resources = ["food", "wood", "stone", "build"]
            # Choose a random resource
            r = random.choice(resources)
            if not r in self.market.database.average_price:
                return
            # Set a random value between market value of food * 5 and market value of food * 10
            avg_food = self.market.database.average_price[r]
            v = round(random.uniform( avg_food* 5, avg_food * 10),2)
            self.state.set_maximum_price(v, r)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Proposed a maximum price of {} for {}".format(self.state.maximum_price[r], r))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        elif r == 7:
            # Create a list with all resources
            resources = ["food", "wood", "stone", "build"]
            # Choose a random resource
            r = random.choice(resources)
            # Set a random value between market value of food /2 and market value of food * 2
            if not "food" in self.market.database.average_price:
                return
            avg_food = self.market.database.average_price["food"]
            v = round(random.uniform( avg_food/2, avg_food * 2),2)
            self.state.set_minimum_price(v,r)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Proposed a minimum price of {} for {}".format(self.state.minimum_price[r], r))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        elif r == 8:
            # Select a random inside self.state.maximum_price
            r = random.choice(list(self.state.maximum_price))
            self.state.remove_maximum_price(r)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Removed maximum price for {}".format(r))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        elif r == 9:
            # Select a random inside self.state.minimum_price
            r = random.choice(list(self.state.minimum_price))
            self.state.remove_minimum_price(self, r)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Removed minimum price for {}".format(r))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")





    # set_people_tax(self, tax):
    # set_business_tax(self, tax):
    # nationalize_business(self, business):
    # set_minimun_wage(self, wage):
    # set_maximum_price(self, price, resource):
    # set_minimum_price(self, price, resource):
    # remove_maximum_price(self, resource):
    # remove_minimum_price(self, resource):

