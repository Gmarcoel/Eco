from  src.entity import Entity


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

    hungry = 0
    dead = False
    basic_needs = {
        "food": 1
    }

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
    
    def __str__(self):
        if self.dead:
            return f"{self.name} is dead"
        return f"{self.name} is {self.age} years old and has {self.money} money, {self.hungry} hungry and items: {self.items}, prices: {self.items_price}"
    
    def add_item(self, item, quantity):
        self.items[item] = quantity
    
    def subtract_item(self, item, quantity):
        if self.items[item] >= quantity:
            self.items[item] -= quantity
        else:
            print("No hay suficiente producto")
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
            return
        if self.hungry > 10:
            self.dead = True
            return

        if self.items[food] > 0:
            self.items[food] -= 1
            self.hungry -= 1
            if self.hungry < 0:
                self.hungry = 0
        else:
            self.hungry += 1
        if self.hungry > 0:
            self.items_price[food] = round(self.items_price[food] + self.items_price[food] * 0.1,2)
        elif self.hungry > 2:
            self.items_price[food] = round(self.items_price[food] + self.items_price[food] * 0.5,2)

    # El trabajar da 1 de trabajo a cada individuo si éste tiene trabajo
    def work(self, job_market):
        if self.contract:
            self.add_item("work", 1)
            # self.job.fullfill()
        else:
            print("No tiene trabajo")
            if not self.specialization in self.contracts_price:
                self.contracts_price[self.specialization] = 1
            j = self.create_job(self.contracts_price[self.specialization], 1, self.specialization, False)
            
            job_market.add_job(j)
        
        self.earnings[2] = self.earnings[1]
        self.earnings[1] = self.earnings[0]
        self.earnings[0] = self.money

        self.balance[2] = self.balance[1]
        self.balance[1] = self.balance[0]
        self.balance[0] = round(self.earnings[0] - self.earnings[1],2)
        

            
    


    # create trades for all needed goods

    def create_trades(self, market):
        
        if self.dead:
            return
        for item in self.basic_needs:
            exp_price = self.get_expected_price(item)
            if exp_price == 0:
                return
            t = self.trade(item, exp_price, False, self.basic_needs[item])
            market.add_trade(t)



    def get_expected_price(self, item):
        if not item in self.items_price:
            self.items_price[item] = 1
        price = self.items_price[item]
        if price > self.money:
            price = self.money
            self.money = 0
        return price
    

    