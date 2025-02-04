class Debt:
    owner = None
    amount = 0
    def __init__(self, owner, amount):
        self.owner = owner
        self.amount = amount
    
    def pay(self, entity):
        if self.owner is not None and entity.active:
            
