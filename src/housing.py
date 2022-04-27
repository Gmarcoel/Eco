from  src.business import Business


class Housing(Business):

    def __init__(self, name, owner, money):
        super().__init__(name=name, owner=owner, money=money)
        self.product = "house"
        self.add_needed_goods("work",1,1)
        self.add_needed_goods("wood",1,1)
        self.add_needed_goods("stone",1,1)
        self.add_needed_goods("build",1,1)
        self.add_item("house",0)
        self.items_price["house"] = 10
        self.production = 1
        self.sector = "housing"

    
    def __str__(self):
        if self.status == "closed":
            return "closed"
        return f"{self.name} has {self.money} money and a balance of {self.balance}, and owned by {self.owner.name}"
    

    

