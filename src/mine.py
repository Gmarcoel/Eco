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
        self.production = 5

    
    def __str__(self):
        return f"{self.name} has a size of {self.space} and {self.money} money and a balance of {self.balance}"
    
    def add_space(self, space):
        self.space += space
    
    def subtract_space(self, space):
        if self.space >= space:
            self.space -= space
        else:
            print("No hay suficiente espacio")
            return False
        return True
    
    def contract(self, person, money, time= 10 ):
        contract = Contract(self,person, money,0,None,"work",0,1, time=time)
        self.work_contracts.append(contract)
        person.contract = contract
        return contract
    

