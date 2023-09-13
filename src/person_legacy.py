from  src.entity import Entity
import random


class Person(Entity):
    name = ""
    age = 0
    money = 0
    job = "None"
    contract = None
    traits = []
    education = 0
    specialization = "None"
    partner = None
    family = []
    happiness = 30
    status = 0
    

    food_price = 2 # Chapuza para que no se mueran

    inmortal = False

    hungry = 0
    dead = False
    sick = False

    basic_needs = {
        "food": 1
    }

    dead_by_hunger = False

    businesses = []


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
        """
        if self.items_price[food] < 0.1:
            self.items_price[food] = 0.2
        if self.hungry > 0:
            self.items_price[food] = round(self.items_price[food] + self.items_price[food] * 0.2,2)
        elif self.hungry > 2:
            self.items_price[food] = round(self.items_price[food] + self.items_price[food] * 0.5,2)
        elif self.hungry > 5:
            self.items_price[food] = round(self.items_price[food] + self.items_price[food] * 0.7,2)
        elif self.hungry > 8:
            self.items_price[food] = round(self.money * 0.8,2)
        elif self.hungry > 10:
            self.items_price[food] = self.money
        """
        """
        elif self.hungry >= 7:
            self.items_price[food] = self.money / 3
        elif self.hungry >= 9:
            self.items_price[food] = self.money
        """

        return True

    # El trabajar da 1 de trabajo a cada individuo si éste tiene trabajo
    def work(self, job_market):
        if self.contract:
            if self.contract not in self.contract.entity1.work_contracts:
                self.contract = None
            self.add_item("work", 10)
            # self.job.fullfill()
        if not self.contract:
            # print("No tiene trabajo")
            if not self.specialization in self.contracts_price:
                self.contracts_price[self.specialization] = 1
            """
            if self.items_price["food"] * 3 < self.contracts_price[self.specialization]:
                self.contracts_price[self.specialization] = round(self.food_price * 3,2)
            if self.hungry > 5:
                self.contracts_price[self.specialization] = round(self.food_price * 1.5,2)
            if self.hungry > 8:
                self.contracts_price[self.specialization] = self.food_price
            """

            # Select a random number between 0 and 1
            ran = round(random.random(),2)
            # if ran < self.status * 0.16:
            if self.age > 16:
                j = self.create_job(self.contracts_price[self.specialization], 1, self.specialization, False)
                job_market.add_job(j)
        
        # self.earnings[2] = self.earnings[1]
        # self.earnings[1] = self.earnings[0]
        # self.earnings[0] = self.money
        # self.balance[2] = self.balance[1]
        # self.balance[1] = self.balance[-1]
        #  = round(self.earnings[0] - self.earnings[1],2)
        self.add_earnings(self.money)
        self.add_balance()
        

            
    


    # create trades for all needed goods

    def create_trades(self, market):
        for item in self.items_price:
            if self.items_price[item] < 0.1:
                self.items_price[item] = 0.2

        
        if self.dead:
            return
        for item in self.basic_needs:
            # No comprar mas caro que el salario propio
            """
            if self.contract and self.specialization in self.contracts_price and self.contracts_price[self.specialization] < self.get_expected_price(item):
                return
            """


            exp_price = self.get_expected_price(item)
            if exp_price == 0:
                return
            t = self.trade(item, exp_price, False, self.basic_needs[item])
            market.add_trade(t)

            # If extra money buy more
            if self.money > self.items_price[item] * 5:
                t = self.trade(item, self.items_price[item], False, 1)
                market.add_trade(t)
        
        # if hungry buy more food
        if self.hungry > 0:
            if self.money > self.items_price[item]:
                t = self.trade(item, self.items_price[item], False, 1)
                market.add_trade(t)
                




    def get_expected_price(self, item):
        if not item in self.items_price:
            self.items_price[item] = 1
        price = self.items_price[item]
        if price > self.money:
            if self.businesses:
                for b in self.businesses:
                    b.extra_dividend()
        if price > self.money:
            price = self.money
        return price
    

    # Consume chocolate to increase happiness by 3
    def eat_chocolate(self):
        # If chocolate is in inventory
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

