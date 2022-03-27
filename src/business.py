# Business class
from  numpy import product
from  src.entity import Entity
from  src.job_market import job_market


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

    negative = 0
    dividend = 0.2



    specialization = "None"



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



    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {len(self.employees)} employees and {len(self.jobs)} jobs with  balance of {self.balance}"
    
    def add_job(self, job): # No se usa
        self.jobs.append(job)
    
    def add_employee(self, employee, job): # Tampoco se usa creo no se no me acuerdo
        self.employees.append(employee)
    
    def add_item(self, item, quantity):
        self.items[item] = quantity
    
    def subtract_item(self, item, quantity):
        print("item: ", item, "quantity: ", quantity, "items: ", self.items)
        if item == None:
            return True
        if self.items[item] >= quantity:
            self.items[item] -= quantity
        else:
            print("No hay suficiente producto")
            return False
        return True
    
        
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
            print("No hay suficiente producto")
            return False
        return True
    
    def delete_needed_good(self, item):
        del self.needed_goods[item]
    
    def produce(self, job_market):
        """
        if self.product == None:
            return
        for item in self.needed_goods:
            if self.items[item] < self.needed_goods[item]:
                return False
        for item in self.needed_goods:
            self.items[item] -= self.needed_goods[item]
        self.items[self.product] += 1
        return True
        """

        # Parte bancarrota
        if self.status == "closed":
            return
        if self.items["work"] == 0:
            self.negative += 1
        else:
            self.negative -= 1
            if self.negative < 0:
                self.negative = 0
        if self.negative > 5:
            # self.bankrupt()
            self.status = "closed"
            self.items_price[self.product] = round(self.needed_goods_price * 0.2, 2) # Una chapuza para quitar luego hace que al quebrar venda más barato



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
                self.items[self.product] += 1 * self.production
                work_used += 1
        
        # Aqui tengo información de la productividad del negocio
        # Para utilizar a futuro en la ia de contrato-despido
        # (work_used y work_left)
        work_left = self.items["work"]



        self.items["work"] = 0

        # Calcular el balance del negocio
        self.earnings[2] = self.earnings[1]
        self.earnings[1] = self.earnings[0]
        self.earnings[0] = self.money

        self.balance[2] = self.balance[1]
        self.balance[1] = self.balance[0]
        self.balance[0] = self.earnings[0] - self.earnings[1]

        # Si el balamce es positivo se intenta contratar
        if self.balance[0] > 0:
            # Si los contratos son más caros que la ganancia del negocio se reduce el precio de los contratos
            if self.specialization not in self.contracts_price:
                self.contracts_price[self.specialization] = 1
            if self.balance[0] < self.contracts_price[self.specialization]:
                self.contracts_price[self.specialization] = round(self.contracts_price[self.specialization] * 0.9, 2)
            else:
                self.hire(job_market)
                

        # Dar al dueño una parte de la ganancia
        if self.owner != None and self.balance[0] > 0:
            slice = round(self.money * self.dividend,2)
            self.owner.add_money(slice)
            self.money = round(self.money - slice,2)
        return True
        
    
    def add_work_contract(self, contract):
        self.work_contracts.append(contract)
    
    def delete_work_contract(self, contract):
        self.work_contracts.remove(contract)
    

    # create trades for all needed goods
    def create_trades(self, market):
        self.needed_goods_price = 0
        for item in self.needed_goods:
            if item is not "work":
                t = self.trade(item, self.get_expected_price(item, market), False, self.needed_goods[item])
                self.needed_goods_price = round(self.needed_goods_price + t.price,2)
                market.add_trade(t)

    """
    def get_expected_price(self, item, market):
        if not item in self.needed_goods_price:
            self.needed_goods_price[item] = 1 # ESTA FUNCION ENTERA ES BASURA
        return self.needed_goods_price[item]
    """
    
    def sell(self, market):
        if not self.product in self.items:
            self.items[self.product]
        # If bussiness is close to bankrupt item at a lower cost
        if self.money < self.needed_goods_price * 1.5:
            self.items_price[self.product] = round(self.needed_goods_price * 0.8,2)


        t = self.trade(self.product, self.get_expected_price(self.product), True, self.items[self.product])
        market.add_trade(t)


    #def bankrupt(self):
    #    for item in self.items:
    #        self.items[item] = 0
    #    for employee in self.employees:
    #        employee.employer = None
    #    for contract in self.work_contracts:
    #        contract.employer = None
    #    self.employees = []
    #    self.jobs = []
    #    self.owner = None
    #    self.status = "closed"
    #    self.negative = 0

    def set_owner(self, owner):
        self.owner = owner
    
    def remove_owner(self):
        self.owner = None
    

    def hire(self, job_market):
        # salary, time, specialization, contractor
        j = self.create_job(self.contracts_price[self.specialization], 10, self.specialization, True)
        job_market.add_job(j)
