from  src.business import Business

class Bank(Business):
    interest_rate = 0.01


    def __init__(self, name, owner, money, interest_rate=0.01):
        super().__init__(name=name, owner=owner, money=money)
        self.interest_rate = interest_rate

        self.product = "loan"
        self.add_needed_goods("work",1,1)
        self.add_item("loan",0)
        self.production = 20
        self.sector = "banking"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"