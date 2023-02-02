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
        self.production = 10 # 5
        self.sector = "lumber"

    
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
    
