from  src.business import Business

class Bank(Business):
    interest_rate = 0.01


    def __init__(self, name, owner, money, interest_rate=0.01):
        super().__init__(name, owner, money)
        self.interest_rate = interest_rate
    
    def __str__(self):
        return f"{self.name} has {self.money} money and {self.interest_rate} interest rate"
    
    def add_interest(self):
        self.money += self.money * self.interest_rate

