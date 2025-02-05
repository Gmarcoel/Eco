from managers.manager import Manager
from managers.business_manager import create_business, get_building
from src import person
from src.project import Project
import json
import random
from src.person import Person
from src.business_sale import Sale

from src.new import New

class PersonManager(Manager):
    person      = None
    job_market  = None
    market      = None
    inversion   = False
    city        = None


    project_resources   = {}
    project             = None


    def __init__(self, person, job_market, market, city, world):
        super().__init__(person)
        self.person             = person
        self.job_market         = job_market
        self.market             = market
        self.city               = city
        self.world              = world
        self.inversion          = False

        self.project_resources  = {}
        self.project            = None

        self.salary                 = 0.0

        self.food_money             = 0.0        # Presupuesto para comida
        self.luxury_money           = 0.0        # Presupuesto para lujos
        self.savings_money          = 0.0        # Presupuesto para ahorros

        self.investment_pool        = 0.0        # Dinero para empezar negocio

        for item in self.market.database.previous_average_price:
            self.person.items_price[item] = self.market.database.previous_average_price[item] * 100

        # self.person.contracts_price[self.person.specialization] = self.job_market.average_contracts_price
        self.person.contracts_price[self.person.specialization] = self.job_market.average_contractor_price
        
        if "food" in self.market.database.previous_average_price:
            if self.person.contracts_price[self.person.specialization] <= self.market.database.previous_average_price["food"]* 3:
                self.person.contracts_price[self.person.specialization] = self.market.database.previous_average_price["food"] * 3
        
        self.preload()

        # Set manager
        self.person.manager = self
    
    def do(self):

        if self.person.dead:
            return
        
        self.balance()

        self.eat()
        self.work()       
        self.person.create_trades(self.market)

        # Decissions:
        self.check_status()
        self.grow()

        # Invest
        if not self.person.has_home():
            house_savings = round(self.savings_money / 2, 2)
            self.savings_money = house_savings
        self.entrepreneur()
        self.invest()
        self.manage()

        # Family
        self.marry()
        self.children()
        self.family()

        # Happiness
        self.person.get_sick()
        if self.person.sick:
            self.health()
        else:
            half_luxury_money = round( self.luxury_money / 2, 2)
            self.luxury_money = half_luxury_money
            self.happiness()
            self.luxury_money = half_luxury_money
            self.manage_goods()
            if not self.person.has_home():
                self.savings_money = house_savings
                self.housing()

        # Economy
        self.person.restart_economics()
        
        if not self.person.inmortal:
            self.die()


    def preload(self):
        self.person.items_price["chocolate"] = 1
        self.person.items["house"] = 0
        self.person.items["furniture"] = 0
        self.person.items_price["house"] = 10
        self.person.items_price["furniture"] = 1
        self.person.items["health"] = 0
        self.person.items_price["health"] = 10
        self.person.items_price["good"] = 2

    def balance(self):
        # Comprobar si tiene trabajo
        salary = 0
        works = False
        if self.person.contract:
            works = True
        if works:
            if self.person.contract.time <= 0:
                self.person.contract = None
                works = False
            else:
                salary = self.person.contract.money1
        self.salary = salary

        # Prices
        # contract_price        = self.person.contracts_price[self.person.specialization]
        # market_contract_price = self.job_market.average_contract_price

        # Values
        food_value            = self.market.database.get_sell_price("food")
        hunger                = self.person.hungry
        salary                = salary
        money                 = self.person.money

        # Si tiene trabajo 50 para comida 30 para lujos 20 para ahorro aprox
        # Excepto si esta hambriento
        if works:
            # Si el food value es mayor que la 

            self.food_money     = round(salary * 0.1, 2)
            self.luxury_money   = round(salary * 0.7, 2)
            self.savings_money  = round(salary * 0.1, 2) + round(money - salary, 2)
        else:
            self.food_money     = money
            self.luxury_money   = 0.0
            self.savings_money  = 0.0
        if hunger > 3:
            self.food_money     = money
            self.luxury_money   = 0.0
            self.savings_money  = 0.0

    def eat(self):
        # Basic needs
        if self.person.age > 1:
            if self.market.database.get_sell_price("food") < self.food_money:
                self.person.items_price["food"] = round(self.market.database.get_sell_price("food") * 0.7 + self.person.items_price["food"] * 0.3, 2)
        # If eating returns false is dead
        if not self.person.eat("food"):
            self.die(c=1)
            return

    def work(self):
        self.person.work(self.job_market)

    # Function to set economic status
    def check_status(self):
        status = 0
        exp_salary = self.market.database.get_expected_salary()
        if self.person.contract:
            status += 1
            salary = self.person.contract.money1
            if salary > exp_salary * 2:
                status += 1
        if self.person.items["house"] > 0:
            status += 1
        if self.person.items["furniture"] > 2:
            status += 1
        if self.person.hungry > 3:
            status -= 5
        if self.person.money > exp_salary * 2:
            status += 1
        if self.person.money > exp_salary * 4:
            status += 1
        if self.person.money > exp_salary * 6:
            status += 1
        
        if status < 0:
            status = 0
        if status > 5:
            status = 5
        if self.person.age < 18:
            status = 6
        self.person.status = status




    # Function to grow
    def grow(self):
        self.person.age += 1
    
    # Function to entrepeneur
    def entrepreneur(self):

        entrepeneurship = 0.1
        
        # If already inversion return
        if self.inversion:
            return
        
        # If is entrepeneur increase chance
        if "entrepeneur" in self.person.traits:
            entrepeneurship += 0.4
        
        # Random chance to become an entrepeneur
        if random.random() < entrepeneurship:
            return
        
        # Find most efficient project
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
            else:
                cero.append(product)
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

        if random.random() < 0.5:
            selected = random.choice(self.market.database.all_existing_goods)
        if not selected:
            return
        # Random chance to create a new business or buy one
        if random.random() < 0.5:
            # Buy business
            sale = Sale(self.person, 10, False, None, get_building(selected))
            self.city.business_market.add_sale(sale)
        else:
            # Create business
            # Buy terrain in city
            if not self.city.buy_terrain(self.person):
                return
            
            # Create project
            project = get_building(selected)
            # Open the projects json file
            with open("data/projects.json", "r") as f:
                data = json.load(f)
                # Get the resources needed for the project
                resources = data["projects"][project]["resources"]
                # Get the time needed for the project
                time = data["projects"][project]["time"]
                # Create the project
                p = Project(project, self.city, self.person, 0, resources, time)
                # Add the project to the list of projects
                self.project = p
            self.inversion = True

    # Invest in current project
    def invest(self):
        # If not food inversion invest so not everyone dies
        if not "food" in self.market.database.previous_amount or self.market.database.previous_amount["food"] == 0:
            # Buy business
            sale = Sale(self.person, 10, False, None, get_building("farm"))
            self.city.business_market.add_sale(sale)

        # If not inversion return
        if not self.inversion:
            return
        
        # Separate savings money in investment pool and project money
        if self.savings_money > 0:
            self.investment_pool += round(self.savings_money * 0.5)
            project_money         = round(self.savings_money * 0.5)
        else:
            return


        # If project is accomplished
        if self.project.accomplish(self.person, project_money):
            # Create new business
            b = create_business(self.project.name,self.person, self.investment_pool)
            self.investment_pool = 0
            # Remove project from list
            self.project = None
            # Set inversion to false
            self.inversion = False
            # Add business to list of businesses
            self.person.businesses.append(b)
            # Add business to city
            self.city.add_business(b)
            self.city.entities.append(b)
            # Add business to world
            self.world.new_businesses.append(New(b, self.city, self.market, self.job_market))
            
            return

        # Invest in project
        self.project_resources = {}
        for key in self.project.resources:
            if not key in self.project_resources:
                self.project_resources[key] = 0
            self.project_resources[key] += self.project.resources[key]
        # Create trades for all needed resources
        for key in self.project_resources:
            # Get the amount of resources the person is able to buy
            if not key in self.person.items_price:
                self.person.items_price[key] = 1
            price = self.person.items_price[key]
            amount = self.project_resources[key]
            money = self.person.money
            # If not enough money return
            if money < self.person.items_price[key] * 30:
                return
            if money > amount * price:
                # self.person.money = round(self.person.money - amount * price,2)
                t = self.person.trade(key, price, False, amount)
                self.market.add_trade(t)
            elif money == 0:
                return
            else:
                while amount != 0:
                    if money > price * amount:
                        # self.person.money = round(self.person.money - amount * price,2)
                        t = self.person.trade(key, price, False, amount)
                        self.market.add_trade(t)
                        break
                    else: amount -= 1
        
    # Manage current businesses
    def manage(self):
        pass

    def marry(self):
        partner = self.person.partner
        if partner is not None and not partner.dead:
            return
        self.person.partner = None
        if self.person.age < 18:
            return
        for p in self.city.people:
            if not p.partner and p.age > 18 and not p.dead and p is not self.person:
                self.person.partner = p
                p.partner = self.person
    
    def children(self):
        partner = self.person.partner
        if partner is None or partner.dead:
            self.person.partner = None
            return
        
        if self.person.age < 18:
            return
        
        if partner.age < 18:
            return
        
        if self.person.age < 50 or partner.age < 50:
            # random chance to have children 1 to 5
            # if random.random() < 0.95:
            if random.random() < 0.95 or len(self.person.family) > 3: # 0.90: # 0.95:# 0.91:
                return
            # Create a random name for the child
            name = "Person " + str(random.randint(100, 10000))
            kid = Person(name,0,0,None)
            self.city.people.append(kid)
            self.city.entities.append(kid)
            self.person.family.append(kid)
            partner.family.append(kid)
            self.world.new_people.append(New(kid, self.city, self.market, self.job_market))

    def family(self):
        if self.person.family == []:
            return
        
        dead = []
        for p in self.person.family:
            if p.dead:
                dead.append(p)
                continue
            if p.age > 18:
                continue
            if self.person.money > self.person.items_price["food"]:
                continue
                self.person.subtract_money(self.person.items_price["food"])
                p.add_money(self.person.items_price["food"])
        # delete all dead people from family
        for p in dead:
            self.person.family.remove(p)   
        
    def die(self, c = 0):
        # The chance increase the older the person is
        chance = 0.01 + c
        if self.person.sick:
            chance += 0.0
        if self.person.age > 50:
            chance += 0.01
        if self.person.age > 70:
            chance += 0.1
        if self.person.age > 80:
            chance += 0.2
        if self.person.age > 90:
            chance += 0.3
        if self.person.age > 100:
            chance += 0.4
        if random.random() < chance:
            self.person.dead = True
            self.person.active = False
            # delete all dead people from family
            dead = []
            for p in self.person.family:
                if p.dead:
                    dead.append(p)
            for p in dead:
                self.person.family.remove(p)
            
                
            if self.person.family != []:
                amount = len(self.person.family)
                partition_money = round(self.person.money / amount,2)
                for p in self.person.family:
                    p.add_money(partition_money)
                # Give bussiness to family
                i = 0
                for b in self.person.businesses:
                    b.owner = self.person.family[i]
                    self.person.family[i].businesses.append(b)
                    
                    i += 1
                    if i >= amount:
                        i = 0
                self.person.businesses = []
                if self.person.partner:
                    self.person.partner.partner = None
                    self.person.partner = None
                self.person.money = 0
            # If not family but partner
            elif self.person.partner is not None and not self.person.partner.dead:
                
                self.person.partner.add_money(self.person.money)
                # Give all bussinesses to partner
                if self.person.businesses != []:
                    for b in self.person.businesses:
                        b.owner = self.person.partner
                        self.person.partner.businesses.append(b)
                        
                    self.person.businesses = []
                self.person.money = 0
                self.person.partner.partner = None
                self.person.partner = None
            # else give everything to the state
            else:
                self.city.add_money(self.person.money)
                for b in self.person.businesses:
                    b.owner = self.city.state
                    self.city.state.businesses.append(b)
                    
                self.person.businesses = []
                self.person.money = 0
            # Remove person from city ESTO LO HACE LA PROPIA CITY PARA LLEVAR EL CENSO
            # self.city.people.remove(self.person)

            self.person.partner = None
            
            self.person.partner = None


    # A partir de aqui rework
    ########################################################

    def happiness(self):
        # Work happiness
        person = self.person
        person.happiness -= 1
        if person.happiness < 0:
            person.happiness = 0
        
        if person.items_price["chocolate"] >  self.luxury_money:
            person.items_price["chocolate"] = self.luxury_money


        if person.happiness < 100: # 10
            if self.market.database.get_sell_price("chocolate") < self.luxury_money:
                self.person.items_price["chocolate"] = round(self.market.database.get_sell_price("chocolate") * 0.7 + self.luxury_money * 0.3,2)
            if self.person.status >= 3:
                person.items_price["chocolate"] = round(self.market.database.get_sell_price("chocolate") * 5,2) # Esto es horrible
            if person.items_price["chocolate"] != 0:
                t = self.person.trade("chocolate", person.items_price["chocolate"], False, 1)
                self.market.add_trade(t)

        person.eat_chocolate()
    
    def housing(self):

        if self.person.items["house"] < 1:
            if self.market.database.get_sell_price("house") <= self.savings_money:
                self.person.items_price["house"] = round(self.market.database.get_sell_price("house") * 0.7 + self.savings_money * 0.3,2)
            else:
                self.person.items_price["house"] = self.savings_money
            t = self.person.trade("house", self.person.items_price["house"], False, 1)
            if t:
                self.market.add_trade(t)
        else:
            if random.random() < 0.01:
                self.person.items["house"] -= 1
                if self.person.items["house"] < 0:
                    self.person.items["house"] = 0
        
        if self.person.items["house"] > 0:
            if self.person.items["furniture"] < 4: 
                if self.market.database.get_sell_price("furniture") <= self.savings_money:
                    self.person.items_price["furniture"] = round(self.market.database.get_sell_price("furniture") * 0.7 + self.savings_money * 0.3,2)
                else:
                    self.person.items_price["furniture"] = self.savings_money
                t = self.person.trade("furniture", self.person.items_price["furniture"], False, 1)     
                if t:
                    self.market.add_trade(t)
        else:
            return
            # TODO if no house, sell furniture
            if self.person.items["furniture"] > 0: 
                t = self.person.trade("furniture", self.person.items_price["furniture"], True, self.person.items["furniture"])     
                if t:
                    self.market.add_trade(t)

    def health(self):
        if not self.person.sick:
            return
        if self.person.items["health"] < 1:
            if self.market.database.get_sell_price("health") <= self.luxury_money:
                self.person.items_price["health"] = round(self.market.database.get_sell_price("health") * 0.7 + self.luxury_money * 0.3,2)
            else:
                self.person.items_price["health"] = self.luxury_money
            t = self.person.trade("health", self.person.items_price["health"], False, 1)
            if t:
                self.market.add_trade(t)
        # Heal
        self.person.heal()
    
    def manage_goods(self):
        if self.person.hungry > 3:
            return
        if self.person.status < 1:
            return
        # Get a number between 1 and 10
        number = self.person.status
        # Buy as much goods as number
        if self.market.database.get_sell_price("good") <= self.luxury_money * 2:  # TODO quitar el * 2 YA
            self.person.items_price["good"] = round(self.market.database.get_sell_price("good") * 0.7 + self.luxury_money * 0.3,2)
        else:
            self.person.items_price["good"] = self.luxury_money
        t = self.person.trade("good", self.person.items_price["good"], False, number)
        if t:
            #print("Sueldo de ", self.salary, "compra con", self.luxury_money, "a", self.person.items_price["good"])
            self.market.add_trade(t)
        #else:
        #    print("Sueldo de ", self.salary, "no compra con", self.luxury_money, "a", self.person.items_price["good"])


        self.person.consume_goods()
