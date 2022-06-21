from  src.business import Business


class EngineFactory(Business):

    def __init__(self, name, owner, money):
        super().__init__(name=name, owner=owner, money=money)
        self.product = "engine"
        self.add_needed_goods("work",1,1)
        self.add_needed_goods("iron",5,1)
        self.add_item("engine",0)
        self.production = 1
        self.sector = "engine"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"
    

    

