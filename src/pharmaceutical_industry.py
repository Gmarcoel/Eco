from  src.business import Business
from  src.person import Person


class Pharmacy(Business):

    def __init__(self, name, owner, money):
        super().__init__(name=name, owner=owner, money=money)
        self.product = "medicament"
        self.add_needed_goods("work",1,1)
        self.add_item("medicament",0)
        self.production = 11
        self.sector = "pharmaceutical"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has  {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"

