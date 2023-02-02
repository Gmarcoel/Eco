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
    electricity = 1
    engine = 1

    negative = 0
    dividend = 0.2
    last_dividend = 0


    after_close = 0


    specialization = "None"

    maintenance = {}

    condition = 10

    # Law related attributes
    minimum_wage = -1
    maximum_price = -1
    minimum_price = -1
    public_price = -1

    sector = "None"

    expected_contracts = 1

    bad_balance = 0

    no_contracts = 0



    def __init__(self, name = "", employees = [], tech_level = 0, owner = None, product = None, money = 0):
        super().__init__(money=money + 100) # EL +100 ESTE LO PEOR QUE HE HECHO PERO ES QUE NO HAY BANCOS
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
        self.bad_balance = 0

        self.maintenance = {}

        self.last_ammount_traded[product] = 0



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
        if self.items[self.product] > 10:
            self.items[self.product] = round(self.items[self.product]* 0.8,0)
        
        # TEMPORAL TEMPORAL Destroy all stock TEMPORAL TEMPORAL
        # self.items[self.product] = 0

        # Parte bancarrota
        if self.status == "closed":
            self.owner.add_money(self.money)
            self.money = 0
            # return True
            return 0
        # Check if there is enough money to pay the employees
        contracts_money = 0
        for contract in self.work_contracts:
            contracts_money += contract.money1
        if self.check_balance() < 0:
            self.bad_balance += 1
        else:
            self.bad_balance = 0
        if self.money < contracts_money or self.bad_balance > 3:
            self.bad_balance = 0
            self.negative += 1
        else:
            self.negative = 0
        # if self.negative > 5 or self.condition <= 0:
        if self.work_contracts == []:
            self.no_contracts += 1
        else:
            self.no_contracts = 0
        if self.negative > 30 or self.no_contracts > 10 or self.money < 1: ## Cambiar lo del money esta MUY MAL
            if self.manager: # RE cutre
                if not self.manager.isPublic():
                    # self.bankrupt()
                    self.status = "closed"
                    self.negative = 0
                    self.no_contracts = 0
                    
                    self.active = False
                    if round(self.needed_goods_price * 0.8, 2) != 0:
                        self.items_price[self.product] = round(self.needed_goods_price * 0.8, 2) # Una chapuza para quitar luego hace que al quebrar venda más barato
                    for contract in self.work_contracts:
                        contract.entity2.contract = None
                    self.work_contracts = []
                    # return False
                    return 0




        work_used = 0
        if self.product == None:
            return 0
        while self.items["work"] > 0: # Muy optimizable
            enough_goods = True
            for item in self.needed_goods:
                if self.items[item] < self.needed_goods[item]:
                    enough_goods = False
                    break
            if enough_goods:
                for item in self.needed_goods:
                    self.items[item] -= self.needed_goods[item]
                self.items[self.product] += round(1 * self.production * self.productivity * self.electricity * self.engine,0)
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
            if self.money > slice:
                if slice > 20000: slice = 20000 # Cutrez que hay que quitar
                self.owner.add_money(slice)
                self.subtract_money(slice)
                self.last_dividend = slice
            else:
                self.last_dividend = 0

        else:
            self.last_dividend = 0

        return work_used
        
    def check_balance(self):
        return super().check_balance() + self.last_dividend
        

    def add_work_contract(self, contract):
        self.work_contracts.append(contract)
    
    def delete_work_contract(self, contract):
        self.work_contracts.remove(contract)
    

    # create trades for all needed goods
    def create_trades(self, market):
        self.needed_goods_price = 0
        for item in self.needed_goods:
            if item != "work":
                t = self.trade(item, self.get_expected_price(item), False, self.needed_goods[item] * len(self.work_contracts) * 5)
                if t:
                    self.needed_goods_price = round(self.needed_goods_price + t.price,2)
                    market.add_trade(t)
        if not self.product in self.items_price:
            self.items_price[self.product] = round(self.needed_goods_price * 1.2,2)


    
    def sell(self, market):
        if self.status == "closed":
            self.after_close += 1
        else:
            self.after_close = 0
        if self.after_close > 3:
            return
        if not self.product in self.items:
            self.items[self.product]
        if self.items[self.product] == 0:
            return
        # If bussiness is close to bankrupt item at a lower cost
        if self.money < self.needed_goods_price * 1.5:
            self.items_price[self.product] = round(self.needed_goods_price * 0.8,2)

        if self.product in self.maintenance:
            manteinance = self.maintenance[self.product]
        else:
            manteinance = 0
        t = self.trade(self.product, self.get_expected_price(self.product), True, self.items[self.product] - manteinance)
        market.add_trade(t)



    def set_owner(self, owner):
        self.owner = owner
    
    def remove_owner(self):
        self.owner = None
    

    def hire(self, jm):
        # salary, time, specialization, contractor
        if self.specialization not in self.contracts_price:
            self.contracts_price[self.specialization] = 5

        j = None
        if self.minimum_wage > self.contracts_price[self.specialization]:
            if self.money > self.minimum_wage:
                j = self.create_job(self.minimum_wage, 10, self.specialization, True)
        else:
            if self.contracts_price[self.specialization] < self.money:
                j = self.create_job(self.contracts_price[self.specialization], 20, self.specialization, True)
            # else:
            #     j = self.create_job(self.money, 20, self.specialization, True)
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
            self.subtract_money(div)


    def trade(self, product, price, sell, quantity):
        # print("EN EL TRADE DE ", self.name, "el precio es ", price)
        if self.public_price != -1:
            price = self.public_price
            self.items_price[product] = price
        else:
            if self.maximum_price != -1:
                if price > self.maximum_price:
                    price = self.maximum_price
            if self.minimum_price != -1:
                if price < self.minimum_price:
                    price = self.minimum_price
        # print("ahora el precio es ", price)
        return super().trade(product, price, sell, quantity)

    def restart_economics(self):
        if not self.total_sum_money:
            self.total_sum_money.append(0)
            self.total_sub_money.append(0)
            #return
        self.total_sum_money.append(self.sum_money)
        self.total_sub_money.append((self.sub_money + self.last_dividend))
        # If greater than 300 pop
        if len(self.total_sum_money) > 300:
            self.total_sum_money.pop(0)
            self.total_sub_money.pop(0)

        
        self.last_ammount_traded[self.product] = 0

        
        self.sum_money = 0
        self.sub_money = 0

        for price in self.items_price:
            if self.items_price[price] < 0.1:
                self.items_price[price] = 0.2