from src.city import City
from src.state import State
from managers.manager import Manager
from managers.business_manager import create_business, get_building
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
    job_market = None
    current_laws = {}
    last_law = ""
    manual = False
    basics_manual = False

    def __init__(self, state, world, market, job_market):
        super().__init__(state)
        self.state = state
        self.state.world = world
        self.market = market
        self.job_market = job_market

        self.state.manager = self
        self.current_laws = {}
    
    def do(self):
        self.last_law = ""

        # if not self.basics_manual:
        self.tax()
        self.work()
        self.pay_subsidies()
        
        if not self.manual:
            self.invest()
        
        # if not self.basics_manual:
        self.buy_resources()

        if not self.manual:
            self.propose_law()

        


    
    def tax(self):
        self.state.tax()
        
    
    def work(self):
        for c in self.state.cities:
            self.state.work(c)

        done = []
        for p in self.state.in_construction:
            if p.time <= 0:
                done.append(p)
                if p.name == "infrastructure":
                    p.entity.add_infrastructure(10) # AQUI NO LLEGA CREOOOOOOOOOOOOOOOOOOOOOOOO
                else:
                    b = create_business(p.name, self.state, p.entity.money)
                    self.state.businesses.append(b)
                    # Add business to the city
                    # p.entity.businesses.append(b)
                    p.entity.add_business(b)
                    # Add .05 percent of state money to the business
                    amm = round(self.state.money * .05, 2)
                    self.state.subtract_money(amm)
                    b.add_money(amm)
                    self.state.world.new_businesses.append(New(b, p.entity, self.market, self.job_market)) # object, city, market, job_market

            else:
                p.time -= 1
        # remove completed projects from the project
        for p in done:
            self.state.in_construction.remove(p)
    
    def invest(self):
        # randomize city order
        cities = self.state.cities
        random.shuffle(cities)
        for c in cities:
            if self.state.money > 50 and len(self.state.projects) < 3:
                if c.infrastructure < 5:
                    self.state.add_infrastructure(c)
                else:
                    # self.state.add_project(c)
                    selected = None
                    max = - 9999
                    cero = []
                    for product in self.market.database.all_existing_goods:
                        # Se comprueba la oferta y demanda
                        if product in self.market.database.last_offer:
                            offer = self.market.database.last_offer[product]
                            demand = self.market.database.last_demand[product]
                            new_max = demand - offer
                            # Se escoge el que más margen tenga (mas demanda/menos oferta)
                            if new_max > max:
                                max = new_max
                                selected = product
                                
                            # Si no hay oferta se guarda para después (prioridad)
                            if offer == 0 and demand != 0:
                                cero.append(product)
                        # else:
                        #     print("POR QUEEE")
                        #     return
                    # Se coge prioridad en los sin oferta
                    if cero != []:
                        for product in cero:
                            if product in self.market.database.last_offer:
                                offer = self.market.database.last_offer[product]
                                demand = self.market.database.last_demand[product]
                                new_max = demand - offer
                                if new_max > max:
                                    max = new_max
                                    selected = product

                    if not selected:
                        return
                    
                    # Create project
                    project = get_building(selected)
                    self.state.add_industry(c, project)
        
    def buy_resources(self):
        self.state.process_needed_resourcess(self.market)
    
    def pay_workers(self):
        if self.state.governor:
            dividend = round(self.state.money * 0.05,2)
            self.state.governor.add_money(dividend)
            self.state.subtract_money(dividend)




    def build_infrastructure(self, city):
        if city == "City":
            return
        for c in self.state.cities:
            if str(c) == city:
                self.state.add_infrastructure(c)
                self.last_law = "build infrastructure"
                return


    def build_industry(self, bus, city):
        chosen = None
        for c in self.state.cities:
            if str(c) == city:
                chosen = c
                break
        if chosen:
            self.state.add_industry(chosen,bus)


    def propose_law(self):
        n = 8
        if self.state.minimum_price != {}:
            n += 1
        if self.state.maximum_price != {}:
            n += 1
        # random number 
        r = random.randint(1,n)
        if r == 1:
            # Set a random value between -0.1 and 0.1
            v = round(random.uniform(0,0.5),2)

            self.set_people_tax(v)
            return
        elif r == 2:
            # Set a random value between -0.1 and 0.1
            v = round(random.uniform(0,0.5),2)
            self.set_business_tax(v)
            return

        elif r == 3:
            i = 20
            bus = None
            while i > 0:
                # choose a random city
                c = random.choice(self.state.cities)
                # Choose a random business
                if not c.businesses:
                    return
                b = random.choice(c.businesses)
                # If business is not owned by state
                if not isinstance(b.owner, State):
                    bus = b
                    break
                i -= 1
            if bus:
                self.nationalize(bus)



        elif r == 4:
            i = 20
            bus = None
            while i > 0:
                # choose a random city
                c = random.choice(self.state.cities)
                # Choose a random business
                if not c.businesses:
                    return
                b = random.choice(c.businesses)
                # If business is not owned by state
                if  isinstance(b.owner, State):
                    bus = b
                    break
                i -= 1
            if bus:
                
                self.privatize(bus)

                
        elif r == 5:
            # Set a random value between market value of food * 2 and market value of food * 10
            if not r in self.market.database.average_price:
                self.last_law = ""
                return
            avg_food = self.market.database.average_price["food"]
            v = round(random.uniform( avg_food* 2, avg_food * 10),2)

            self.set_minimum_wage(v)

        elif r == 6:
            # Create a list with all resources
            resources = ["food", "wood", "iron", "build"]
            # Choose a random resource
            r = random.choice(resources)
            if not r in self.market.database.average_price:
                self.last_law = ""
                return
            # Set a random value between market value of food * 5 and market value of food * 10
            avg_food = self.market.database.average_price[r]
            v = round(random.uniform( avg_food* 1, avg_food * 3),2)
            self.set_maximum_price(v, r)


        elif r == 7:
            # Create a list with all resources
            resources = ["food", "wood", "iron", "build", "chocolate", "house", "furniture"]
            # Choose a random resource
            r = random.choice(resources)
            # Set a random value between market value of food /2 and market value of food * 2
            if not "food" in self.market.database.average_price:
                self.last_law = ""
                return
            avg_food = self.market.database.average_price["food"]
            v = round(random.uniform( avg_food/2, avg_food * 2),2)

            self.set_minimum_price(v, r)

        elif r == 8:
            # Select a random inside self.state.maximum_price
            if not self.state.maximum_price:
                self.last_law = ""
                return
            r = random.choice(list(self.state.maximum_price))
            self.remove_maximum_price(r)



        elif r == 9:
            # Select a random inside self.state.minimum_price
            if not self.state.minimum_price:
                self.last_law = ""
                return
            r = random.choice(list(self.state.minimum_price))
            self.remove_minimum_price(r)

        
        elif r == 10:
            self.print_money(10000)

        self.last_law = ""
        return



    def print_money(self, n):
        # Print money
        self.state.money = round(self.state.money + n,2)
        self.last_law = "print_money"
        return

    def remove_minimum_price(self, r):
        self.state.remove_minimum_price(r)
        # Remove from current_laws
        if not self.state.minimum_price:
            self.current_laws.pop("minimum_price")
        else:
            self.current_laws["minimum_price"] = self.state.minimum_price
        self.last_law = "remove minimum price of " + r
        return

    def remove_maximum_price(self, r):
        self.state.remove_maximum_price(r)
        # Remove from current_laws
        if not self.state.maximum_price:
            self.current_laws.pop("maximum_price")
        else:
            self.current_laws["maximum_price"] = self.state.maximum_price
        self.last_law = "remove maximum price of " + r
        return

    def set_minimum_price(self, v, r):
        self.state.set_minimum_price(v,r)
        self.current_laws["minimum_price"] = self.state.minimum_price
        self.last_law = "minimum price of " + r + ": " + str(self.state.minimum_price[r])
        return

    def set_maximum_price(self, v, r):
        self.state.set_maximum_price(v, r)
        self.current_laws["maximum_price"] = self.state.maximum_price
        self.last_law = "maximum price of " + r + ": " + str(self.state.maximum_price[r])
        return

    def set_minimum_wage(self, v):
        self.state.set_minimun_wage(v)
        self.current_laws["minimum_wage"] = self.state.minimum_wage
        self.last_law = "minimum_wage " + str(self.state.minimum_wage)


    def privatize(self, bus):
        # Select random person in city
        if not bus.manager:
            self.last_law = ""
            return
        if not bus.manager.city.people:
            return
        p = random.choice(bus.manager.city.people)
        self.give_business(p, bus)

    def give_business(self, person, bus):
        # set owner of business to person
        bus.owner = person
        # Add business to person
        person.businesses.append(bus)
        # Remove business from state
        if bus in self.state.businesses: # ESTO TIENE ALGO QUE NO DEBERIA SER NECESARIO QUE MIEDO 
            self.state.businesses.remove(bus)
        
        self.last_law = "privatize " + bus.name

    def nationalize(self, bus):
        self.state.nationalize_business(bus)
        self.last_law = "nationalize " + bus.name
        return


    def set_business_tax(self, v):
        # Add v to tax
        # self.state.set_businesses_tax(round(self.state.business_tax_rate + v,2))
        self.state.set_businesses_tax(v)
        self.current_laws["business_tax_rate"] = self.state.business_tax_rate
        self.last_law = "business_tax_rate " + str(self.state.business_tax_rate)

    def set_people_tax(self, v):
        # Add v to tax
        # self.state.set_people_tax(round(self.state.people_tax_rate + v,2))
        self.state.set_people_tax(v)
        self.current_laws["people_tax_rate"] = self.state.people_tax_rate
        self.last_law = "people_tax_rate " + str(self.state.people_tax_rate)

    def nationalize_sector(self, sector):
        for c in self.state.cities:
            for b in c.businesses:
                if b.sector == sector:
                    self.nationalize(b)
    
    def privatize_sector(self, sector):
        for c in self.state.cities:
            for b in c.businesses:
                if b.sector == sector and isinstance(b.owner, State):
                    self.privatize(b)

    def nationalize_all(self):
        for c in self.state.cities:
            for b in c.businesses:
                if not isinstance(b.owner, State):
                    self.nationalize(b)
    
    def privatize_all(self):
        for c in self.state.cities:
            for b in c.businesses:
                if isinstance(b.owner, State):
                    self.privatize(b)   

    def set_manual(self):
        self.manual = not self.manual
        return

    def set_basics_manual(self):
        self.basics_manual = not self.basics_manual
        return

    def subsidize_business(self, bus, money):
        self.state.subsidize(bus, money)

    def unsubsidize_business(self, bus):
        self.state.unsubsidize(bus)


    def pay_subsidies(self):
        self.state.pay_subsidies()
    
    def open_business(self, bus):
        if bus.status == "open":
            return
        bus.status = "open"
        if bus.owner:
            if bus in bus.owner.businesses:
                bus.owner.businesses.remove(bus)
        bus.owner = self.state
        self.state.businesses.append(bus)

