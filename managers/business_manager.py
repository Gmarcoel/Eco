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
from src.pharmaceutical_industry import Pharmacy
from src.hospital import Hospital
from src.consumer_goods_factory import GoodsFactory
from src.copper_mine import CopperMine
from src.electric_central import ElectricCentral
from src.oil_extractor import OilExtractor
from src.refinery import Refinery
from src.engine_factory import EngineFactory

from src.new import New
from src.business_sale import Sale




class BusinessManager(Manager):
    business = None
    job_market = None
    market = None
    city = None
    pib = 0
    average_profit = 0
    last_profits = []

    # Fixed parameters
    fixed_sell_price = -1
    fixed_ammount_workers = -1
    fixed_contract_price = -1
    fixed_science_buy = -1
    fixed_science_price = -1


    def __init__(self, business, job_market, market, city, world):
        super().__init__(business)
        self.business = business
        self.job_market = job_market
        self.market = market
        self.city = city
        self.world = world
        self.last_profits = []
        
        # Set manager
        self.business.manager = self
        self.entity = self.business
    
    def do(self):


        self.manage_laws()
        self.check_balance()

        self.calculate_average_profit()


        self.maintenance()
        self.manage_personal()
        self.manage_expansion()

        self.fixed_parameters()

        self.work()
        self.ask_for_money()
        # self.check_balance()
        self.contract_workers()

        # Economy
        self.business.restart_economics()

        # Investigation
        self.investigate()
        self.improve_production()

        # Sell
        self.sell_business()

        self.fixed_parameters()
        # self.check_balance()
    
    total_costs = 0
    expected_earnings = 0
    expected_one_earning = 0
    expected_product_price = 0
    number_sold_products = 0
    number_products = 0
    def check_balance(self):
        amount = 0                  # Cantidad de dinero que gasta el negocio
        number_products = 0         # Cantidad que produce el negocio
        expected_earnings = 0       # Cantia de dinero que se espera que gane el negocio
        print(self.business.name)
        for con in self.business.work_contracts:
            print("     ", con.money1)
            amount += con.money1
            print("         ", amount)
            number_products += round(1 * self.business.productivity * self.business.production,0)
        for item in self.business.needed_goods:
            if item in self.business.items_price:
                amount += self.business.items_price[item] * self.business.needed_goods[item]

        # Vamos a usar los sold products en vez de los productos fabricados porque asi los precios no bajan de manera inssotenible
        # Si no vendemos usamos lo otro para que baje el precio

        # Número de productos vendidos la última vez
        no_sales = False
        if not self.business.product in self.business.last_ammount_traded:
            number_sold_products = 1
        else:
            number_sold_products = self.business.last_ammount_traded[self.business.product]
            if number_sold_products == 0:
                no_sales = True
                number_sold_products = 1
        
        # Ganancias esperadas si se vende la misma cantidad
        if self.business.product in self.business.items_price:
            expected_earnings = round(self.business.items_price[item]*number_sold_products,2)
            
        self.total_costs = amount
        self.expected_earnings = expected_earnings
        self.number_sold_products = number_sold_products
        self.number_products = number_products

        # Se calcula el dinero que se gana por persona
        if self.business.work_contracts: 
            self.expected_one_earning = expected_earnings / len(self.business.work_contracts)
        else:
            self.expected_one_earning = 0

        # Se calcula el dinero minimo para ser rentable
        self.expected_product_price = round(self.total_costs/ number_sold_products,2)
        if not self.business.product in self.business.items_price:
            return
        
        # Si el dinero minimo para mantenerse es menor que el precio
        # if self.business.items_price[self.business.product] > self.expected_product_price:

        # Se comprueba oferta y demanda del producto
        if self.business.product in self.market.database.last_offer:
            offer = self.market.database.last_offer[self.business.product]
            demand = self.market.database.last_demand[self.business.product]
        else:
            offer = 0
            demand = 0
        
        # Si la oferta es mayor que la demanda y no se venden todos los productos se baja el precio
        if offer < demand and number_sold_products < number_products:
            # Se baja el precio del producto
            self.business.items_price[self.business.product] = round(self.business.items_price[self.business.product] * 0.6,2)
            if self.business.items_price[self.business.product] < 0.1:
                self.business.items_price[self.business.product] = 0.1
            # Si aun así sigue siendo alto respecto al mercado:
            if not self.business.product in self.market.database.previous_average_price:
                return
            if self.business.items_price[self.business.product] > self.market.database.previous_average_price[self.business.product]:
                # Se iguala a la media del mercado
                self.business.items_price[self.business.product] = self.market.database.previous_average_price[self.business.product]
    
        # Si se venden todos los productos se sube el precio
        elif number_sold_products == number_products:
            if offer < demand:
                # Se sube el precio del producto
                self.business.items_price[self.business.product] = round(self.business.items_price[self.business.product] * 1.2,2)
            else:
                # Se sube el precio del producto
                self.business.items_price[self.business.product] = round(self.business.items_price[self.business.product] * 1.05,2)
            # Si aun así sigue siendo bajo respecto al mercado:
            if not self.business.product in self.market.database.previous_average_price:
                return
            """
            if self.business.items_price[self.business.product] < self.market.database.previous_average_price[self.business.product]:
                # Se iguala a la media del mercado
                self.business.items_price[self.business.product] = self.market.database.previous_average_price[self.business.product]
            # Si el precio es menor que el minimo para ganancia se sube a este
            if self.business.items_price[self.business.product] < self.expected_product_price:
                self.business.items_price[self.business.product] = self.expected_product_price
            """
        
        elif offer > demand:
            self.business.items_price[self.business.product] = round(self.business.items_price[self.business.product] * 0.5,2)


            # Si la oferta es menor que la demana se sube el precio


            # SI la oferta es menor que la demanda pero no se vende todo el producto se mantiene el precio
            # else:
                # El precio del producto se encaja con las ganancias
            #     self.business.items_price[self.business.product] = self.expected_product_price
            self.number_sold_products = number_sold_products
            self.number_products = number_products


    def manage_personal(self):
        new_cs = []
        for contract in self.business.work_contracts:
            new_c = contract.fullfill()
            if new_c is not None:
                new_cs.append(contract)
            """
            else:
                # Renew contract
                self.business.hire(self.job_market)
            """
        self.business.work_contracts = new_cs
        
    def manage_expansion(self):
        pass

    def work(self):
        work_used = self.business.produce(self.job_market)
        if self.business.product in self.market.database.previous_average_price:
            self.pib = self.market.database.previous_average_price[self.business.product] * self.business.productivity * self.business.production * work_used
        else:
            self.pib = 0
        # if not self.business.produce(self.job_market):
        #     self.city.infrastructure += 1
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
                t = self.business.trade(need, price, False, ammount)
                self.market.add_trade(t)
    
    def ask_for_money(self):   
        debt_money = 0
        for contract in self.business.work_contracts:
            debt_money += contract.money1
        if self.business.owner is not None and self.business.money < debt_money :
            mon = self.business.owner.money * 0.3
            self.business.owner.subtract_money(mon)
            self.business.add_money(mon)
            self.business.negative = 0
        

    def manage_laws(self):
        self.business.minimum_wage = self.city.minimum_wage
        if self.business.product in self.city.minimum_price:
            self.business.minimum_price = self.city.minimum_price[self.business.product]
        else:
            self.business.minimum_price = -1
        
        if self.business.product in self.city.maximum_price:
            self.business.maximum_price = self.city.maximum_price[self.business.product]
        else:
            self.business.maximum_price = -1

        if not isinstance(self.business.owner, state.State):
            self.business.public_price = -1
        else:
            if self.business.product in self.city.public_price:
                self.business.public_price = self.city.public_price[self.business.product]
            
    contracted = 0
    contracted_price = 0
    def contract_workers(self):
        self.contracted = 0
        self.contracted_price = 0
        if self.fixed_ammount_workers == -1:
            # Se comprueba oferta y demanda del producto
            if self.business.product in self.market.database.last_offer:
                offer = self.market.database.last_offer[self.business.product]
                demand = self.market.database.last_demand[self.business.product]
            else:
                offer = 0
                demand = 0

            
            if self.business.specialization not in self.business.contracts_price:
                self.business.contracts_price[self.business.specialization] = 5

            # Si lo que se espera ganar por empleado es menor que el precio del contrato
            if self.expected_one_earning < self.business.contracts_price[self.business.specialization]:
                # Se baja el precio del contrato
                self.business.contracts_price[self.business.specialization] = round(self.expected_one_earning*0.9,2)
            
            # Si el balamce es positivo se intenta contratar
            # if self.business.check_balance():
            if offer < demand: # and self.business.check_balance()>0:
                
                # if self.expected_one_earning > self.business.contracts_price[self.business.specialization]:
                self.business.expected_contracts += 1
                # Si 
            else:
                self.business.expected_contracts = len(self.business.work_contracts) - 1
            if self.business.expected_contracts < 1:
                self.business.expected_contracts = 1
            

            # Si los contratos son más caros que la ganancia del negocio se reduce el precio de los contratos
            if self.business.contracts_price[self.business.specialization] < 1: # Esto es una mierda que hay que cambiar
                self.business.contracts_price[self.business.specialization] = 1
            
            """
            if self.business.last_balance() < self.business.contracts_price[self.business.specialization]:
                self.business.contracts_price[self.business.specialization] = round(self.business.contracts_price[self.business.specialization] * 0.8, 2)
            """
            # Si no hay contratos se hace lo posible por contratar
            if not self.business.work_contracts:
                self.business.contracts_price[self.business.specialization] = round(self.business.contracts_price[self.business.specialization] * 1.5,2)
            
            # Si el precio de los contratos es mayor que la mitad del dinero actual se iguala a esta
            if self.business.contracts_price[self.business.specialization] > self.business.money / 2:
                self.business.contracts_price[self.business.specialization] = self.business.money / 2
        
        # Se contrata a todos los que se necesiten
        if self.business.expected_contracts > len(self.business.work_contracts):
            for i in range(self.business.expected_contracts - len(self.business.work_contracts)):
                self.business.hire(self.job_market)
        
        # Printear el nombre del negrocio y los expected_contracts
        # print(self.business.name, self.business.expected_contracts)

    def improve_production(self):
        if not "electricity" in self.business.items:
            self.business.items["electricity"] = 0
            self.business.items_price["electricity"] = 1

        if not "engine" in self.business.items:
            self.business.items["engine"] = 0
            self.business.items_price["engine"] = 10
        
        if not "gas" in self.business.items:
            self.business.items["gas"] = 0
            self.business.items_price["gas"] = 2
        
        # Use electricity
        if self.business.items["electricity"] > 0:
            self.business.items["electricity"] -= 1
            self.business.electricity = 2
        else:
            self.business.electricity = 1
        
        # If engine use gas
        if self.business.items["engine"] > 0 and self.business.items["gas"] > 0:
            self.business.items["gas"] -= 1
            self.business.engine = 3
        else:
            self.business.engine = 1
        
        # 1 in 10 for engine to break
        if self.business.items["engine"] > 0 and random.randint(1,10) == 1:
            self.business.items["engine"] -= 1


        # If engine try to buy gas
        if self.business.items["engine"] > 0:
            t = self.business.trade("gas", self.business.items_price["gas"], False, 1)
            if t:
                self.market.add_trade(t)

        # If not enough money to improve return
        if not self.business.product in self.business.items_price:
            return
        if self.business.check_balance() < self.business.items_price[self.business.product] * 2:
            return
        # Try to buy electricity
        t = self.business.trade("electricity", self.business.items_price["electricity"], False, 1)
        if t:
            self.market.add_trade(t)
        # If not enough money to improve return
        if self.business.check_balance() < self.business.items_price[self.business.product] * 3:
            return
        # Try to buy engine
        t = self.business.trade("engine", self.business.items_price["engine"], False, 1)
        if t:
            self.market.add_trade(t)

        

    def investigate(self):
        if self.fixed_science_buy == -1:
            ammount = 1
        else:
            ammount = self.fixed_science_buy
        if not isinstance(self.business.owner, state.State):
            if not "science" in self.business.items:
                self.business.items["science"] = 0
            if not "science" in self.business.items_price:
                self.business.items_price["science"] = 1
            # If business is profitable
            if self.business.check_balance() > 0:
                if self.business.money >= self.total_costs:
                    t = self.business.trade("science", self.business.items_price["science"], False, ammount)
                    self.market.add_trade(t)
                while self.business.items["science"] > 0:
                    self.business.productivity = round(self.business.productivity + 0.2, 1)
                    self.business.items["science"] -= 1

        
        ran = random.randint(1, 5)
        if ran == 1:
            self.business.productivity = round(self.business.productivity - 0.2, 1)
            if self.business.productivity < 1:
                self.business.productivity = 1

    def calculate_average_profit(self):
        profit = self.business.check_balance() + self.contracted_price
        self.last_profits.append(profit)
        if len(self.last_profits) > 10:
            self.last_profits.pop(0)
        self.average_profit = round(sum(self.last_profits) / len(self.last_profits),2)


    def fixed_parameters(self):
        if self.fixed_sell_price != -1:
            self.business.items_price[self.business.product] = self.fixed_sell_price
        if self.fixed_ammount_workers != -1:
            self.business.expected_contracts = self.fixed_ammount_workers
        if self.fixed_contract_price != -1:
            self.business.contracts_price[self.business.specialization] = self.fixed_contract_price
        # Cantidad de ciencia comprada se determina en la funcion investigate
        if self.fixed_science_price != -1:
            self.business.items_price["science"] = self.fixed_science_price
        

    def set_sell_price(self, price):
        self.fixed_sell_price = price
    
    def unset_sell_price(self):
        self.fixed_sell_price = -1

    def set_ammount_workers(self, ammount):
        self.fixed_ammount_workers = ammount

    def unset_ammount_workers(self):
        self.fixed_ammount_workers = -1

    def set_contract_price(self, price):
        self.fixed_contract_price = price
    
    def unset_contract_price(self):
        self.fixed_contract_price = -1
    
    def set_science_buy(self, price):
        self.fixed_science_buy = price
    
    def unset_science_buy(self):
        self.fixed_science_buy = -1
    
    def set_science_price(self, price):
        self.fixed_science_price = price
    
    def unset_science_price(self):
        self.fixed_science_price = -1
    
    def sell_business(self):
        # Si el negocio está cerrado vender
        if self.business.status == "closed":
            if self.business.owner:
                sale = Sale(self.business.owner, 10, True, self.business, get_building(self.business.product))
            else:
                sale = Sale(self.business, 10, True, self.business, self.business.sector)
            self.city.business_market.add_sale(sale)

    def close_business(self):
        self.business.status = "closed"
        self.business.active = False


def create_business(business_type, owner, money):

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
    if business_type == "pharmacy":
        # Generate random name
        name = "Pharmacy " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Pharmacy(name, owner, money) 
    if business_type == "hospital":
        # Generate random name
        name = "Hospital " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Hospital(name, owner, money) 
    if business_type == "goods":
        # Generate random name
        name = "Goods " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = GoodsFactory(name, owner, money)
    if business_type == "copper mine":
        # Generate random name
        name = "Copper " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = CopperMine(name, owner, money)
    if business_type == "electric central":
        # Generate random name
        name = "Electricity " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = ElectricCentral(name, owner, money)
    if business_type == "oil extractor":
        # Generate random name
        name = "Oil " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = OilExtractor(name, owner, money)
    if business_type == "refinery":
        # Generate random name
        name = "Gas " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = Refinery(name, owner, money)
    if business_type == "engine factory":
        # Generate random name
        name = "Engine " + str(random.randint(1, 10000))
        with open("data/names.json", "r") as f:
            data = json.load(f)
            name = data["names"][random.randint(0, len(data["names"])-1)]
        b = EngineFactory(name, owner, money)




    
    with open("data/projects.json", "r") as f:
        data = json.load(f)
        maintenance = data["projects"][business_type]["maintenance"]
        b.maintenance = maintenance
    
    return b

        
def get_sector(product):
    industries = ["farm", "mine", "sawmill", "constructor", "chocolate", "housing", "furniture", "science", "pharmacy", "hospital", "goods", "copper mine", "electric central", "oil extractor", "refinery", "engine factory"]
    goods = ["food", "build", "wood", "iron", "chocolate", "house", "furniture", "science", "medicament", "health", "good", "copper", "electricity", "oil", "gas", "engine"]
    sectors = ["farming", "mining", "lumber", "construction", "chocolating", "housing", "furniture", "science", "pharmaceutical", "healthcare", "consumer", "copper", "electricity", "oil", "gas", "engine"]

    for i in range(len(goods)):
        if goods[i] == product:
            return sectors[i]

def get_building(product):
    industries = ["farm", "mine", "sawmill", "constructor", "chocolate", "housing", "furniture", "science", "pharmacy", "hospital", "goods", "copper mine", "electric central", "oil extractor", "refinery", "engine factory"]
    goods = ["food", "build", "wood", "iron", "chocolate", "house", "furniture", "science", "medicament", "health", "good", "copper", "electricity", "oil", "gas", "engine"]
    sectors = ["farming", "mining", "lumber", "construction", "chocolating", "housing", "furniture", "science", "pharmaceutical", "healthcare", "consumer", "copper", "electricity", "oil", "gas", "engine"]

    for i in range(len(goods)):
        if goods[i] == product:
            return industries[i]
