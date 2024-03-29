from  src.entity import Entity
import random


class Person(Entity):
    name            = ""
    age             = 0
    money           = 0
    job             = "None"
    contract        = None
    traits          = []
    education       = 0
    specialization  = "None"
    partner         = None
    family          = []
    happiness       = 30
    status          = 0
    
    inmortal        = False

    hungry          = 0
    dead            = False
    sick            = False

    basic_needs     = {
        "food": 1
    }

    dead_by_hunger  = False
    businesses      = []


    def __init__(self, name="", age=0, money=0, job=None):
        #super.__init__(money)
        super().__init__(money=money)
        self.name = name
        self.age = age
        self.job = "Farmer"
        self.items_price["food"] = 1.5
        self.traits = []
        self.businesses = []
        self.family = []
    
    def __str__(self):
        if self.dead:
            return f"{self.name} is dead"
        return f"{self.name} is {self.age} years old and has {self.money} money, {self.hungry} hungry and items: {self.items}, prices: {self.items_price}"
    
    def add_item(self, item, quantity):
        self.items[item] = quantity
    
    def subtract_item(self, item, quantity):
        if not item in self.items:
            self.items[item] = 0
        if self.items[item] >= quantity:
            self.items[item] -= quantity
        else:
            # print("No hay suficiente producto")
            return False
        return True
    
    def add_trait(self, trait):
        self.traits.append(trait)
    
    def remove_trait(self, trait):
        self.traits.remove(trait)

    
    # Si tiene comida - hambre si no + hambre
    def eat(self, food):
        if self.age <= 18:
            return True
        if not food in self.items:
            self.items[food] = 0
        if self.dead == True:
            return True
        if self.hungry >= 10:
            self.dead = True
            self.active = False
            self.dead_by_hunger = True
            return False

        if self.items[food] > 0:
            self.items[food] -= 1
            self.hungry -= 1
            if self.hungry < 0:
                self.hungry = 0
        else:
            self.hungry += 1
        return True

    # El trabajar da 1 de trabajo a cada individuo si éste tiene trabajo
    def work(self, job_market):
        if self.contract:
            if self.contract not in self.contract.entity1.work_contracts:
                self.contract = None
            self.add_item("work", 10)
        if not self.contract:
            if not self.specialization in self.contracts_price:
                self.contracts_price[self.specialization] = 1
            ran = round(random.random(),2)
            # if ran < self.status * 0.16:
            if self.age > 16:
                j = self.create_job(self.contracts_price[self.specialization], 4, self.specialization, False)
                job_market.add_job(j)
        

        self.add_earnings(self.money)
        self.add_balance()
        

    # create trades for all needed goods
    def create_trades(self, market):
        
        if self.dead:
            return
        for item in self.basic_needs:

            # exp_price = self.get_expected_price(item)
            exp_price = round(self.get_expected_price(item) * 1.2,2)
            if exp_price == 0:
                return
            t = self.trade(item, exp_price, False, self.basic_needs[item])
            market.add_trade(t)

                

    

    # Consume chocolate to increase happiness by 3
    def eat_chocolate(self):
        if "chocolate" in self.items and self.items["chocolate"] > 0:
            self.items["chocolate"] -= 1
            self.happiness += 3
    
    def tax(self, tax_rate):
        if self.contract:
            earnings = self.contract.money1
            if self.money > (earnings * tax_rate):
                self.subtract_money(earnings * tax_rate)
                return earnings * tax_rate
            else:
                self.subtract_money(self.money)
                self.money = 0
                return self.money
        return 0
    
    def get_sick(self):
        # Probability of getting sick
        prob = 0.1
        if self.hungry > 1:
            prob += 0.1
        # Random chance of getting sick
        ran = random.random()
        if ran < prob:
            self.sick = True
            return True
        return False
    
    def heal(self):
        if self.sick:
            if "health" in self.items and self.items["health"] > 0:
                self.items["health"] -= 1
                self.sick = False


    def consume_goods(self):
        if not "good" in self.items:
            self.items["good"] = 0
        
        num = self.items["good"]
        self.items["good"] = 0
        self.happiness += num
        return


    def has_home(self):
        if "home" in self.items and self.items["home"] > 0:
            return True
        return False