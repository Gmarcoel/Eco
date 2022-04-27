from src.job_market import job_market
from managers.manager import Manager
from src.market import Market
from src import state
from src.project import Project
import json
import random

from src.farm import Farm
from src.mine import Mine
from src.sawmill import Sawmill
from src.constructor import Constructor
from src.chocolate_factory import ChocolateFactory
from src.housing import Housing
from src.furniture_factory import FurnitureFactory
from src.science_hub import ScienceHub
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
        self.entity = self.business
    
    def do(self):

        self.manage_laws()
        self.check_balance()
        self.maintenance()
        self.manage_personal()
        self.manage_expansion()
        self.work()
        self.ask_for_money()
        # self.check_balance()
        self.contract_workers()

        # Economy
        self.business.restart_economics()

        # Investigation
        self.investigate()

        self.check_balance()
    
    total_costs = 0
    expected_earnings = 0
    expected_one_earning = 0
    expected_product_price = 0
    def check_balance(self):
        amount = 0
        number_products = 0
        expected_earnings = 0
        for con in self.business.work_contracts:
            amount += con.money1
            number_products += 1 * self.business.productivity * self.business.production
        for item in self.business.needed_goods:
            if item in self.business.items_price:
                amount += self.business.items_price[item] * self.business.needed_goods[item]

        if self.business.product in self.business.items_price:
            expected_earnings = round(self.business.items_price[item]*number_products,2)
        self.total_costs = amount
        self.expected_earnings = expected_earnings
        if self.business.work_contracts:
            # Se calcula el dinero que se gana por persona
            self.expected_one_earning = expected_earnings / len(self.business.work_contracts)
            print("EXPECTED ONE EARNING: ", self.expected_one_earning)
            # Se calcula el dinero minimo para ser rentable
            self.expected_product_price = round(self.total_costs/ number_products,2)
            # Si el dinero minimo para mantenerse es menor que el precio se iguala
            if not self.business.product in self.business.items_price:
                return
            if self.business.items_price[self.business.product] < self.expected_product_price:
                self.business.items_price[self.business.product] = self.expected_product_price
        else:
            self.expected_one_earning = 0



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

    def contract_workers(self):
        if self.business.specialization not in self.business.contracts_price:
            self.business.contracts_price[self.business.specialization] = 5
        # Si el balamce es positivo se intenta contratar
        if self.business.check_balance():
            if self.expected_one_earning > self.business.contracts_price[self.business.specialization]:
                self.business.expected_contracts += 1
        
        if self.business.expected_contracts < 1:
            self.business.expected_contracts = 1
        # Si los contratos son más caros que la ganancia del negocio se reduce el precio de los contratos
        if self.business.contracts_price[self.business.specialization] < 1: # Esto es una mierda que hay que cambiar
            self.business.contracts_price[self.business.specialization] = 1
        if self.business.last_balance() < self.business.contracts_price[self.business.specialization]:
            self.business.contracts_price[self.business.specialization] = round(self.business.contracts_price[self.business.specialization] * 0.8, 2)
        if not self.business.work_contracts:
            self.business.contracts_price[self.business.specialization] = round(self.business.contracts_price[self.business.specialization] * 1.5,2)
        elif self.business.expected_contracts > len(self.business.work_contracts):
            # print("NEGOCIO", self.business.name, " PRECIO", self.business.contracts_price[self.business.specialization])
            self.business.hire(self.job_market)
        

    def investigate(self):
        if not isinstance(self.business.owner, state.State):
            if not "science" in self.business.items:
                self.business.items["science"] = 0
            if not "science" in self.business.items_price:
                self.business.items_price["science"] = 1
    
            if self.business.money >= self.total_costs:
                t = self.business.trade("science", self.business.items_price["science"], False, 1)
                self.market.add_trade(t)
            while self.business.items["science"] > 0:
                self.business.productivity = round(self.business.productivity + 0.2, 1)
                self.business.items["science"] -= 1

        
        ran = random.randint(1, 5)
        if ran == 1:
            self.business.productivity = round(self.business.productivity - 0.2, 1)
            if self.business.productivity < 1:
                self.business.productivity = 1
            
        
        






def create_business(business_type, owner, money):
    print("Creating business" + business_type)
    if business_type == "farm":
        # Generate random name
        name = "Farm " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Farm(name, owner, money)
    
    if business_type == "mine":
        # Generate random name
        name = "Mine " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Mine(name, owner, money)
    
    if business_type == "sawmill":
        # Generate random name
        name = "Sawmill " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Sawmill(name, owner, money)
    
    if business_type == "constructor":
        # Generate random name
        name = "Constructor " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Constructor(name, owner, money)
    if business_type == "chocolate":
        # Generate random name
        name = "Chocolate " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = ChocolateFactory(name, owner, money)
    if business_type == "housing":
        # Generate random name
        name = "Housing " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Housing(name, owner, money)   
    if business_type == "furniture":
        # Generate random name
        name = "Furniture " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = FurnitureFactory(name, owner, money) 
    if business_type == "science":
        # Generate random name
        name = "Science Hub " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = ScienceHub(name, owner, money) 

    
    with open("data/projects.json", "r") as f:
        data = json.load(f)
        maintenance = data["projects"][business_type]["maintenance"]
        b.maintenance = maintenance
    
    return b

        
                

    
