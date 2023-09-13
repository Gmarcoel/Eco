from  src.business import Business
from  src.person import Person


class Hospital(Business):

    def __init__(self, name, owner, money):
        super().__init__(name=name, owner=owner, money=money)
        self.product = "health"
        self.add_needed_goods("work",1,1)
        self.add_needed_goods("medicament",1,1)
        self.add_item("health",0)
        self.production = 10 # 3
        self.sector = "healthcare"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has  {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"

