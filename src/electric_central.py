from  src.business import Business


class ElectricCentral(Business):

    def __init__(self, name, owner, money):
        super().__init__(name=name, owner=owner, money=money)
        self.product = "electricity"
        self.add_needed_goods("work",1,1)
        self.add_needed_goods("copper",1,1)
        self.add_item("electricity",0)
        self.production = 10
        self.sector = "electricity"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"
    

    

