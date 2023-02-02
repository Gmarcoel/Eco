from  src.business import Business
from  src.person import Person
from  src.contract import Contract

class Constructor(Business):
    workspace = 0

    def __init__(self, name, owner, money, workspace=10):
        super().__init__(name=name, owner=owner, money=money)
        self.workspace = workspace
        self.product = "build"
        self.add_needed_goods("work",1,1)
        self.add_item("build",0)
        self.production = 10 # 5
        self.sector = "construction"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {self.workspace} workspace and {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"
    
    def add_workspace(self, workspace):
        self.workspace += workspace
    
    def subtract_workspace(self, workspace):
        if self.workspace >= workspace:
            self.workspace -= workspace
        else:
            print("No hay suficiente tierra")
            return False
        return True
    


