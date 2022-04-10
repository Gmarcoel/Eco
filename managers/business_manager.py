from src.job_market import job_market
from managers.manager import Manager
from src.market import Market
from src import business
from src.project import Project
import json
import random

from src.farm import Farm
from src.mine import Mine
from src.sawmill import Sawmill
from src.constructor import Constructor

from src.new import New




class BusinessManager(Manager):
    business = None
    job_market = None
    market = None
    city = None


    def __init__(self, business, job_market, market, city, world):
        super().__init__(business)
        self.business = business
        self.job_market = job_market
        self.market = market
        self.city = city
        self.world = world
        
        # Set manager
        self.business.manager = self
    
    def do(self):

        self.manage_laws()
        self.check_balance()
        # self.maintenance()
        self.manage_personal()
        self.manage_expansion()
        self.work()
        self.ask_for_money()
        self.check_balance()

        # Economy
        self.business.restart_economics()
    

    def check_balance(self):
        pass

    def manage_personal(self):
        new_cs = []
        for contract in self.business.work_contracts:
            new_c = contract.fullfill()
            if new_c is not None:
                new_cs.append(contract)
            else:
                # Renew contract
                self.business.hire(self.job_market)
        self.business.work_contracts = new_cs

    def manage_expansion(self):
        debt_money = 0
        for contract in self.business.work_contracts:
            debt_money += contract.money1
        if self.business.owner is not None and self.business.money < debt_money :
            self.business.owner.subsidize(self.business, self.business.owner.money * 0.3)
            self.business.negative = 0

    def work(self):
        if not self.business.produce(self.job_market):
            self.city.infrastructure += 1
        self.business.sell(self.market)
        self.business.create_trades(self.market)
    
    def maintenance(self):
        flag = False
        for need in self.business.maintenance:
            if need in self.business.items:
                if self.business.maintenance[need] <= self.business.items[need]:
                    self.business.items[need] -= self.business.maintenance[need]
                else:
                    flag = True
        if flag:
            self.business.condition -= 1
        else:
            self.business.condition += 1
            if self.business.condition > 10:
                self.business.condition = 10

            

        # Buy all maintenance needs in the market
        for need in self.business.maintenance:
            money = self.business.money
            ammount = self.business.maintenance[need]
            if not need in self.business.items_price:
                self.business.items_price[need] = 1
            price = self.business.items_price[need]
            # If enough money to buy
            if money > ammount * price:
                # self.business.subtract_money(price * ammount)
                t = self.business.trade(need, price, False, ammount)
                self.market.add_trade(t)
    
    def ask_for_money(self):   
        debt_money = 0
        for contract in self.business.work_contracts:
            debt_money += contract.money1
        if self.business.owner is not None and self.business.money < debt_money :
            self.business.owner.subsidize(self.business, self.business.owner.money * 0.3)
            self.business.negative = 0

    def manage_laws(self):
        self.business.minimum_wage = self.city.minimum_wage
        if self.business.product in self.city.minimum_price:
            self.business.minimum_price = self.city.minimum_price[self.business.product]
        else:
            self.business.minimum_price = 0
        
        if self.business.product in self.city.maximum_price:
            self.business.maximum_price = self.city.maximum_price[self.business.product]
        else:
            self.business.maximum_price = 0









def create_business(business_type, owner, money):
    if business_type == "farm":
        # Generate random name
        name = "Farm " + str(random.randint(1, 10000))
        b = Farm(name, owner, money)
    
    if business_type == "mine":
        # Generate random name
        name = "Mine " + str(random.randint(1, 10000))
        b = Mine(name, owner, money)
    
    if business_type == "sawmill":
        # Generate random name
        name = "Sawmill " + str(random.randint(1, 10000))
        b = Sawmill(name, owner, money)
    
    if business_type == "constructor":
        # Generate random name
        name = "Constructor " + str(random.randint(1, 10000))
        b = Constructor(name, owner, money)
    
    with open("data/projects.json", "r") as f:
        data = json.load(f)
        maintenance = data["projects"][business_type]["maintenance"]
        b.maintenance = maintenance
    
    return b

        
                

    
