# Business class
from  numpy import product
from  src.entity import Entity
# from  src.job_market import job_market
from  src.contract import Contract

class Business(Entity):
    name = ""
    employees = []
    jobs = [] # No se usa
    tech_level = 0
    owner = None
    work_contracts = []
    status = "open"

    needed_goods = {}
    needed_goods_price = 20 # Placeholder
    product = None
    production = 1
    productivity = 1

    negative = 0
    dividend = 0.2
    last_divident = 0

    after_close = 0


    specialization = "None"

    maintenance = {}

    condition = 10

    # Law related attributes
    minimum_wage = 0
    maximum_price = 0
    minimum_price = 0

    sector = "None"

    expected_contracts = 1




    def __init__(self, name = "", employees = [], tech_level = 0, owner = None, product = None, money = 0):
        super().__init__(money=money)
        self.name = name
        self.employees = employees
        self.tech_level = tech_level
        self.owner = owner
        self.product = product
        self.add_item("work",0)
        self.needed_goods = {}
        self.work_contracts = []
        self.employees = []
        self.jobs = [] # No se usa
        self.status = "open"
        self.negative = 0

        self.maintenance = {}



    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {len(self.employees)} employees and {len(self.jobs)} jobs with  balance of {self.balance}, owned by {self.owner.name}"
    
    def add_job(self, job): # No se usa
        self.jobs.append(job)
    
    def add_employee(self, employee, job): # Tampoco se usa creo no se no me acuerdo
        self.employees.append(employee)
    

    
        
    def add_needed_goods(self, item, quantity):
        self.needed_goods[item] = quantity
        self.items_price[item] = 1

    def add_needed_goods(self, item, quantity, price):
        self.needed_goods[item] = quantity
        self.items_price[item] = price
    
    def subtract_needed_goods(self, item, quantity):
        if self.needed_goods[item] >= quantity:
            self.needed_goods[item] -= quantity
        else:
            # print("No hay suficiente producto")
            return False
        return True
    
    def delete_needed_good(self, item):
        del self.needed_goods[item]
    
    def produce(self, job_market):

        # if not employees hire
        if len(self.work_contracts) == 0:
            self.hire(job_market)

        # Destroy some of the existing stock
        if not self.product in self.items:
            self.items[self.product] = 1

        self.items[self.product] = round(self.items[self.product]* 0.8,0)

        # Parte bancarrota
        if self.status == "closed":
            self.owner.add_money(self.money)
            self.money = 0
            return True
        # Check if there is enough money to pay the employees
        contracts_money = 0
        for contract in self.work_contracts:
            contracts_money += contract.money1
        if self.money < contracts_money:
            self.negative += 1
        else:
            self.negative = 0
        if self.negative > 5 or self.condition <= 0:
            # self.bankrupt()
            self.status = "closed"
            if round(self.needed_goods_price * 0.8, 2) != 0:
                self.items_price[self.product] = round(self.needed_goods_price * 0.8, 2) # Una chapuza para quitar luego hace que al quebrar venda más barato
            for contract in self.work_contracts:
                contract.entity2.contract = None
            self.work_contracts = []
            return False



        work_used = 0
        if self.product == None:
            return
        while self.items["work"] > 0: # Muy optimizable
            enough_goods = True
            for item in self.needed_goods:
                if self.items[item] < self.needed_goods[item]:
                    enough_goods = False
                    break
            if enough_goods:
                for item in self.needed_goods:
                    self.items[item] -= self.needed_goods[item]
                self.items[self.product] += round(1 * self.production * self.productivity,0)
                work_used += 1
            self.items["work"] -= 1
        
        # Aqui tengo información de la productividad del negocio
        # Para utilizar a futuro en la ia de contrato-despido
        # (work_used y work_left)
        work_left = self.items["work"]



        self.items["work"] = 0

        self.add_earnings(self.money)
        self.add_balance()

                

        # Dar al dueño una parte de la ganancia
        if self.owner != None and self.check_balance():
            slice = round(self.last_balance() * self.dividend,2)
            self.owner.add_money(slice)
            self.money = round(self.money - slice,2)
            self.last_divident = slice
        else:
            self.last_divident = 0

        return True
        
    
    def add_work_contract(self, contract):
        self.work_contracts.append(contract)
    
    def delete_work_contract(self, contract):
        self.work_contracts.remove(contract)
    

    # create trades for all needed goods
    def create_trades(self, market):
        self.needed_goods_price = 0
        for item in self.needed_goods:
            if item != "work":
                t = self.trade(item, self.get_expected_price(item), False, self.needed_goods[item] * len(self.work_contracts))
                if t:
                    self.needed_goods_price = round(self.needed_goods_price + t.price,2)
                    market.add_trade(t)


    
    def sell(self, market):
        if self.status == "closed":
            self.after_close += 1
        if self.after_close > 3:
            return
        if not self.product in self.items:
            self.items[self.product]
        if self.items[self.product] == 0:
            return
        # If bussiness is close to bankrupt item at a lower cost
        if self.money < self.needed_goods_price * 1.5:
            self.items_price[self.product] = round(self.needed_goods_price * 0.8,2)


        t = self.trade(self.product, self.get_expected_price(self.product), True, self.items[self.product])
        market.add_trade(t)



    def set_owner(self, owner):
        self.owner = owner
    
    def remove_owner(self):
        self.owner = None
    

    def hire(self, jm):
        # salary, time, specialization, contractor
        if self.specialization not in self.contracts_price:
            self.contracts_price[self.specialization] = 5
        # if self.balance[-1] < self.contracts_price[self.specialization]:
        #     self.contracts_price[self.specialization] = round(self.contracts_price[self.specialization] * 0.9, 2)
        # else:
        j = None
        if self.minimum_wage > self.contracts_price[self.specialization]:
            j = self.create_job(self.minimum_wage, 10, self.specialization, True)
        else:
            j = self.create_job(self.contracts_price[self.specialization], 20, self.specialization, True)
        if j:
            jm.add_job(j)

    def contract(self, person, money, time= 10 ):
        con = Contract(self,person, money,0,None,"work",0,1, time=time, fine = round(money * 3,2))
        self.work_contracts.append(con)
        person.contract = con
        return con
    
    def fire(self, person):
        for c in self.work_contracts:
            if c.entity2.name == person:
                c = Contract(self,person,c.fine,0,None,None,0,0, time=0, fine = c.fine)

        

    
    def fire(self, specialization):
        if not self.work_contracts:
            return
        min = None
        for c in self.work_contracts:
            if c.entity2.specialization == specialization:
                if min == None:
                    min = c
                elif c.time < min.time:
                    min = c
        if min != None:
            min.entity2.contract = None
            min = Contract(self,min.entity2,c.fine,0,None,None,0,0, time=0, fine = c.fine)
        
    def extra_dividend(self):
        if self.owner != None:
            div = round(self.money * self.dividend,2)
            self.owner.add_money(div)
            self.money = round(self.money - div,2)


    def trade(self, product, price, sell, quantity):
        # print("EN EL TRADE DE ", self.name, "el precio es ", price)
        if self.maximum_price != 0:
            if price > self.maximum_price:
                price = self.maximum_price
        if self.minimum_price != 0:
            if price < self.minimum_price:
                price = self.minimum_price
        # print("ahora el precio es ", price)
        return super().trade(product, price, sell, quantity)