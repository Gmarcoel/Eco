from  src.business import Business
from  src.person import Person


class Carecenter(Business):

    def __init__(self, name, owner, money):
        super().__init__(name=name, owner=owner, money=money)
        self.product = "food"
        self.add_needed_goods("work",1,1)
        self.add_needed_goods("food",10,1)
        self.add_item("food",0)
        self.production = 10
        self.sector = "care"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {self.land} acres of land and {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"
    
    def add_land(self, land):
        self.land += land
    
    def subtract_land(self, land):
        if self.land >= land:
            self.land -= land
        else:
            print("No hay suficiente tierra")
            return False
        return True
    
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
        if self.negative > 5 or self.no_contracts > 6 or self.money < 1: ## Cambiar lo del money esta MUY MAL
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