from  src.business import Business
from  src.person import Person
from  src.contract import Contract

class Mine(Business):
    space = 5


    def __init__(self, name, owner, money, space=5):
        super().__init__(name=name, owner=owner, money=money)
        self.space = space
        self.product = "stone"
        self.add_needed_goods("work",1,1)
        self.add_item("stone",0)
        self.production = 2
        self.sector = "mining"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has a size of {self.space} and {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"
    
    def add_space(self, space):
        self.space += space
    
    def subtract_space(self, space):
        if self.space >= space:
            self.space -= space
        else:
            print("No hay suficiente espacio")
            return False
        return True
    

