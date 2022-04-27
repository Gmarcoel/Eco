from  src.business import Business
from  src.person import Person


class ScienceHub(Business):

    def __init__(self, name, owner, money, land=100):
        super().__init__(name=name, owner=owner, money=money)
        self.land = land
        self.product = "science"
        self.add_needed_goods("work",1,1)
        self.add_item("science",0)
        self.production = 3
        self.sector = "science"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has  {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"

