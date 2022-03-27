
from business import Business


from business import Business
from contract import Contract
from person import Person

class Job:
    business = None
    contract = None
    money = 0

    def __init__(self, business, contract, money):
        self.business = business
        self.contract = contract
        self.person = person
        self.money = money
    
    def __str__(self):
        return f"{self.business.name} has {self.contract.name} contract with {self.person.name}"
    
    def work(self):
        self.contract.fullfill()
