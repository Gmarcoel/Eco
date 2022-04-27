from  src.business import Business


class ChocolateFactory(Business):

    def __init__(self, name, owner, money):
        super().__init__(name=name, owner=owner, money=money)
        self.product = "chocolate"
        self.add_needed_goods("work",1,1)
        self.add_needed_goods("food",1,1)
        self.add_item("chocolate",0)
        self.production = 2
        self.sector = "chocolating"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"
    

    

