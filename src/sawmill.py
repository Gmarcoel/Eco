from  src.business import Business
from  src.person import Person
from  src.contract import Contract

class Sawmill(Business):
    land = 0

    def __init__(self, name, owner, money, land=100):
        super().__init__(name=name, owner=owner, money=money)
        self.land = land
        self.product = "wood"
        self.add_needed_goods("work",1,1)
        self.add_item("wood",0)
        self.production = 5

    
    def __str__(self):
        return f"{self.name} has {self.land} acres of land and {self.money} money and a balance of {self.balance}"
    
    def add_land(self, land):
        self.land += land
    
    def subtract_land(self, land):
        if self.land >= land:
            self.land -= land
        else:
            print("No hay suficiente tierra")
            return False
        return True
    
    def contract(self, person, money, time= 10 ):
        contract = Contract(self,person, money,0,None,"work",0,1, time=time)
        self.work_contracts.append(contract)
        person.contract = contract
        return contract
    

