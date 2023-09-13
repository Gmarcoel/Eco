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
    average_profit = 0.0
    def __init__(self, business, job_market, market, city, world):
        super().__init__(business)
        self.business = None
        self.job_market = None
        self.market = None
        self.city = None
        self.pib = 0.0
        self.average_profit = 0.0
        self.last_profits = []
        self.business = business
        self.job_market = job_market
        self.market = market
        self.city = city
        self.world = world
        self.last_profits = []
            # Fixed parameters
        self.fixed_sell_price = -1
        self.fixed_ammount_workers = -1
        self.fixed_contract_price = -1
        self.fixed_science_buy = -1
        self.fixed_science_price = -1

        # Set manager
        self.business.manager = self
        self.entity = self.business

        # Costes
        self.total_costs          = 0.0        # Costes totales del negocio
        self.product_cost         = 0.0        # Coste del producto que produce el negocio
        self.person_cost          = 0.0        # Coste por cada trabajador (sueldo y materiales)
        self.material_cost        = 0.0        # Coste materiales
        self.person_productivity  = 0.0        # Cantidad producida por cada trabajador

        self.number_products      = 0.0        # Cantidad de productos que produce el negocio
        self.market_value         = 0.0        # Valor del mercado del producto que produce el negocio
        self.number_sold_products = 0.0        # Cantidad de productos vendidos en el ultimo periodo
        self.product_margin       = 0.0        # Margen de beneficio del producto

        self.revenue              = 0.0        # Cantidad de dinero ganado el último esfuerzo
        self.profit               = 0.0        # Cantidad de dinero ganado el último esfuerzo menos dinero gastado

        self.salary_money         = 0.0        # Dinero para modificar salarios
        self.price_money          = 0.0        # Dinero para modificar precios

        self.contract_money       = 0.0        # Presupuesto para contratar trabajadores
        self.science_money        = 0.0        # Presupuesto para investigar
        self.invest_money         = 0.0        # Presupuesto para invertir
        self.minimum_liquidity    = 0.0        # Liquidez minima para mantener el negocio

        self.contracted           = 0.0
        self.contracted_price     = 0.0

        self.average_cotract_price = []
        self.average_sell_price    = []


        self.every_years = 1

    def do(self):


        self.manage_laws()
        self.check_balance()

        self.sell_strategy()
        self.buy_strategy()
        self.contract_strategy()

        self.calculate_average_profit()


        self.maintenance()
        self.manage_personnel()
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

        """
        # Cutrez que hay que arreglar
        if self.business.money >= self.total_costs * 10:
            # Dar al dueño el dinero sobrante
            excedent = self.business.money - (self.total_costs * 10)
            self.business.subtract_money(excedent)
            self.business.owner.add_money(excedent)
        """
    

    def check_balance(self):
        # Calcular costes
        self.total_costs          = 0.0
        self.person_cost          = 0.0
        self.product_cost         = 0.0
        self.material_cost        = 0.0
        self.person_productivity  = 0.0
        self.number_products      = 0.0
        self.market_value         = 0.0
        self.number_sold_products = 0.0
        self.product_margin       = 0.0

        # Costes de los trabajadores
        for con in self.business.work_contracts:
            self.total_costs      += con.money1
            self.number_products  += round(1 * self.business.productivity * self.business.production, 0)
        
        # Costes de los materiales
        for item in self.business.needed_goods:
            if item in self.business.items_price:
                self.total_costs += self.business.items_price[item] * self.business.needed_goods[item] * len(self.business.work_contracts)
                self.material_cost += self.business.items_price[item] * self.business.needed_goods[item] * len(self.business.work_contracts)
        
        # Coste y productividad por persona
        work_contracts = len(self.business.work_contracts)
        if work_contracts == 0: work_contracts = 1
        self.person_cost         = self.total_costs / work_contracts
        self.person_productivity = self.number_products / work_contracts

        # Valor de mercado del producto
        self.market_value = self.market.database.get_average_buy_price(self.business.product)
        if self.number_products == 0:
            self.product_cost = 0
        else:
            self.product_cost = self.total_costs / self.number_products
        self.product_margin = self.market_value - self.product_cost

        # Coste de contratacion minimo (1 persona y respectivos materiales)
        if self.total_costs <= 0:
            if self.business.specialization not in self.business.contracts_price:
                    self.business.contracts_price[self.business.specialization] = 5
            self.total_costs = self.business.contracts_price[self.business.specialization] + self.material_cost
        
        
        # Numero productos vendidos
        if not self.business.product in self.business.last_ammount_traded:
            self.number_sold_products = 0
        else:
            self.number_sold_products = self.business.last_ammount_traded[self.business.product]


        # Ganancias totales
        if self.business.product in self.business.items_price:
            self.revenue = self.business.items_price[self.business.product] * self.number_sold_products
            self.profit  = self.revenue - self.total_costs + self.entity.subsidy
        else:
            self.revenue = 0
            self.profit  = 0
        ######################################

        # Si hay ganancias
        # if self.profit > 0:
        self.salary_money = round(self.profit * .3,2) # 30% Para modificar salarios
        self.price_money  = round(self.profit * .3,2) # 30% Para modificar precios
                                                          # 40% Ahorro

        # Como mínimo el negocio tiene que tener liquidez de 10 veces el coste total
        # Si tiene mas de eso destina el 60% a ampliar negocio y el 40% a mejorar productividad
        self.minimum_liquidity = self.total_costs * 10
        if self.business.money < self.minimum_liquidity:
            self.contract_money = 0.0
            self.science_money  = 0.0
            self.invest_money   = 0.0
        else:
            self.contract_money = (self.business.money - self.minimum_liquidity) * 0.6
            if not isinstance(self.business.owner, state.State):
                self.science_money  = round((self.business.money - self.minimum_liquidity) * 0.3,2)
                self.invest_money   = round((self.business.money - self.minimum_liquidity) * 0.1,2)
                # self.science_money  = round(self.profit * .3,2)
                # self.invest_money   = round(self.profit * .1,2)
            else:
                self.science_money  = 0
                self.invest_money   = round((self.business.money - self.minimum_liquidity) * 0.4,2)
                # self.invest_money   = round(self.profit * .4,2)
        

    def sell_strategy(self):
        if self.every_years % 5 != 0:
            self.every_years += 1
            return
        # Cuentas
        #####################################################
        # Control errores
        if not self.business.product in self.business.items_price or self.total_costs <= 0 or self.number_products == 0:
            return
        # Calcular el margen real de producto
        ganancias_totales = self.revenue
        margen_real       = round((ganancias_totales - self.total_costs) / self.number_products,2)
        precio_actual     = self.business.items_price[self.business.product]
        precio_mercado    = self.market_value
        margen_minimo     = round((self.total_costs / self.number_products) * (20 / self.business.production),2)     # Un 20% de ganancia
        precio_minimo     = round((self.total_costs / self.number_products) + margen_minimo,2)
        dinero_precios    = self.price_money

        print(self.business.name)
        print("Precio sueldos + gastos:", self.total_costs, "Cantidad productos:", self.number_products, "Precio producto:", precio_actual, "Posible ganancia total:", precio_actual * self.number_products, "Precio minimo", precio_minimo,"\n")

        if precio_actual < precio_minimo:
            precio_actual = precio_minimo

        # Configuracion de precios
        #####################################################
        #if self.number_sold_products < self.number_products:
        #    precio_actual = round(precio_minimo * 0.8 + precio_actual * 0.2,2)
        if self.number_sold_products == 0:
            self.precio_actual = precio_minimo
        if self.number_sold_products < self.number_products * 0.5:
            self.precio_actual = precio_minimo * 0.8 + precio_actual * 0.2

        """
        if self.number_sold_products < self.number_products:
            if precio_actual > precio_minimo:
                precio_actual = precio_minimo
            else:
                if precio_actual * 0.8 > precio_mercado:
                    precio_actual = precio_mercado
                else:
                    precio_actual = round(precio_actual,2) 
        """
        """
        # Si no se vende toda la producción se rebajan los precios acercandose al margen
        if self.number_sold_products < self.number_products:
            # Si el precio actual supera el de mercado se impone el de mercado
            if precio_actual > precio_mercado:
                precio_actual = precio_mercado
            # Si no, se rebaja el margen de ganancia
            else:
                rebaja = margen_real * 0.8
                precio_actual = precio_actual - rebaja
        # Si se vende todo precio de mercado
        else:
            # precio_actual = precio_mercado
            pass
        # Se añade lo reservado
        # precio_actual -= self.price_money
        """


        # Estabilizacion de precios
        #####################################################
        print("precio pre average", precio_actual)

        if self.average_sell_price:
            avg = (sum(self.average_sell_price) + precio_actual) / (len(self.average_sell_price) + 1)
            if len(self.average_sell_price) > 2:
                self.average_sell_price.pop(0)
            precio_actual = avg
        else:
            avg = precio_actual
        
        precio_actual = round(precio_actual,2)
        
        print("precio post average", precio_actual)
        print("\n")



        # Precio mínimo
        #####################################################
        # if precio_minimo > precio_actual:
        #     precio_actual = precio_minimo

        # Fin
        #####################################################
        self.average_sell_price.append(avg)
        self.business.items_price[self.business.product] = precio_actual


    def buy_strategy(self):
        # Todos los materiales a comprar
        materiales = self.business.needed_goods

        for material in materiales:
            if not material in self.market.database.sell_price:
                continue
            self.business.items_price[material] = self.market.database.sell_price[material] * 1.5
        
        return

        for material in materiales:
            # Se comprueba oferta y demanda del material
            if self.business.product in self.market.database.last_offer:
                offer = self.market.database.last_offer[material]
                demand = self.market.database.last_demand[material]
            else:
                offer = 0
                demand = 0

    def contract_strategy(self):
        # Aumento/Disminucion basada en beneficios
        if len(self.business.work_contracts):
            human_cost = round((self.total_costs - self.material_cost)/len(self.business.work_contracts),2)
            self.business.contracts_price[self.business.specialization] = human_cost + self.salary_money
        
            # La productividad de una persona por el precio de mercado menos el coste de materiales da techo salario
            techo = round(self.person_productivity * self.market_value - (self.material_cost/len(self.business.work_contracts)),2)
            if self.business.contracts_price[self.business.specialization] > techo:
                self.business.contracts_price[self.business.specialization] = techo
        

        # Esto no
        if self.business.contracts_price[self.business.specialization] < 1:
            self.business.contracts_price[self.business.specialization] = 1
        # Esto no
        # if self.business.contracts_price[self.business.specialization] > 20:
        #     self.business.contracts_price[self.business.specialization] = 10

        # Arreglo basado en mercado
        if self.market.database.get_expected_salary() * 0.6 > self.business.contracts_price[self.business.specialization]:
            self.business.contracts_price[self.business.specialization] = self.market.database.get_expected_salary() * 0.6
        if self.market.database.get_expected_salary() * 3 < self.business.contracts_price[self.business.specialization]:
            self.business.contracts_price[self.business.specialization] = self.market.database.get_expected_salary() * 3
        
        if len(self.average_cotract_price) > 0:
            avg = (sum(self.average_cotract_price) + self.business.contracts_price[self.business.specialization]) / (len(self.average_cotract_price) + 1)
            if len(self.average_cotract_price) > 10:
                self.average_cotract_price.pop(0)
            self.business.contracts_price[self.business.specialization] = avg
        else:
            avg = self.business.contracts_price[self.business.specialization]
        self.average_cotract_price.append(avg)

        




    def manage_personnel(self):
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
        print("KKKKKKKKKK", work_used, self.business.items[self.business.product])
        if self.business.product in self.market.database.previous_average_price:
            self.pib = self.market.database.previous_average_price[self.business.product] * self.business.productivity * self.business.production * work_used
        else:
            self.pib = self.business.items[self.business.product]
        # if not self.business.produce(self.job_market):
        #     self.city.infrastructure += 1
        # print(self.business.name, " vendiendo ", self.business.items[self.business.product]," de ", self.business.product, " por ",  self.business.get_expected_price(self.business.product), "teniendo", self.business.money)
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
        if self.business.money < self.minimum_liquidity:
            if self.business.owner is not None:
                mon = self.minimum_liquidity
                if mon < self.business.owner.money * 0.5:
                    if self.business.owner.subtract_money(mon):
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
            

    def contract_workers(self):
        self.contracted = 0
        self.contracted_price = 0
        if self.fixed_ammount_workers == -1:
            # Se comprueba oferta y demanda del producto
            if self.business.product in self.market.database.last_offer:
                # offer = self.market.database.last_offer[self.business.product]
                # demand = self.market.database.last_demand[self.business.product]
                offer = self.market.database.get_average_offer(self.business.product)
                demand = self.market.database.get_average_demand(self.business.product)
            else:
                offer = 0
                demand = 0

            # Precio contrato
            if self.business.specialization not in self.business.contracts_price:
                self.business.contracts_price[self.business.specialization] = 5
            
            # Informacion de contratacion
            contract_price = self.business.contracts_price[self.business.specialization]
            n_contracts    = len(self.business.work_contracts)

            # Si la demanda menos la oferta es mayor que la productividad de una persona
            # y el valor esperado de la produccion es mayor que coste de una persona
            # y si hay presupuesto para contratar
            if demand - offer >= self.person_productivity:
                if self.market_value * self.number_products > self.person_cost:
                    if self.contract_money > contract_price:
                        self.business.expected_contracts += 1
            
            # Si hay menos demanda que oferta
            elif offer - demand > self.person_productivity:
                if self.business.expected_contracts > 0:
                    self.business.expected_contracts -= 1
            if self.business.expected_contracts == 0:
                self.business.expected_contracts = 1

            # Margen de persona es la productividad de una persona por el valor de mercado menos el coste de una persona
            person_margin = self.person_productivity * self.market_value - self.person_cost

            """
            # Si el numero de contratos menor que el numero de contrato esperados + 2 o es 0
            # se sube el sueldo un 0.2 del margen
            if n_contracts < self.business.expected_contracts + 2 or n_contracts == 0:
                self.business.contracts_price[self.business.specialization] += person_margin * 0.2
            
            # Maximo sueldo
            if self.business.contracts_price[self.business.specialization] > self.product_margin * self.person_productivity:
                self.business.contracts_price[self.business.specialization] = round(self.product_margin * self.person_productivity * 0.9,2)

            # uff
            if self.business.contracts_price[self.business.specialization] < 1:
                self.business.contracts_price[self.business.specialization] = 3 # Ay madre
            """

            if self.average_profit < 0:
                self.business.expected_contracts = 1

        
        # Se contrata a todos los que se necesiten
        print("XXXXXXXXXXXXXXXXXX", self.business.expected_contracts, len(self.business.work_contracts), self.business.name)
        if self.business.expected_contracts > len(self.business.work_contracts):
            cost = 0
            for i in range(self.business.expected_contracts - len(self.business.work_contracts)):
                cost += self.business.contracts_price[self.business.specialization]
                if self.business.money > cost:
                    self.business.hire(self.job_market)
                else:
                    break
        


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
            self.business.electricity = 1.5
        else:
            self.business.electricity = 1
        
        # If engine use gas
        if self.business.items["engine"] > 0 and self.business.items["gas"] > 0:
            self.business.items["gas"] -= 1
            self.business.engine = 2
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

        dinero_para_invertir = round(self.invest_money,2)
        # Try to buy electricity
        t = self.business.trade("electricity", dinero_para_invertir, False, 1)
        if t:
            self.market.add_trade(t)
        # Try to buy engine
        t = self.business.trade("engine", dinero_para_invertir, False, 1)
        if t:
            self.market.add_trade(t)

        

    def investigate(self):
        if self.business.product == "science":
            return
        if not "science" in self.business.items:
            self.business.items["science"] = 0
        if not "science" in self.business.items_price:
            self.business.items_price["science"] = 2
        if self.fixed_science_price == -1:
            self.business.items_price["science"] = self.science_money

        

        # If science money is enough buy science
        ammount = 0
        #if self.science_money > self.business.items_price["science"]:
        ammount = 1
        if self.fixed_science_buy != -1:
            ammount = self.fixed_science_buy
        
        if ammount > 0:
            #t = self.business.trade("science", self.business.items_price["science"], False, ammount)
            t = self.business.trade("science", self.business.items_price["science"], False, ammount)
            self.market.add_trade(t)

        # Use science to improve productivity
        while self.business.items["science"] > 0:
            self.business.productivity = round(self.business.productivity + 0.05, 1)
            self.business.items["science"] -= 1

        # Decrease productivity
        ran = random.randint(1, 5)
        if ran == 1:
            self.business.productivity = round(self.business.productivity - 0.05, 1)
            if self.business.productivity < 1:
                self.business.productivity = 1

    def calculate_average_profit(self):
        # profit = self.business.check_balance() + self.contracted_price
        profit = self.profit
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
        self.business.negative = 0
        self.business.no_contracts = 0
    
    def isPublic(self):
        if not isinstance(self.business.owner, state.State):
            return False
        return True


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

