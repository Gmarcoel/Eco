class Debt:
    owner = None
    ammount = 0
    def __init__(self, owner, ammount):
        self.owner = owner
        self.ammount = ammount
    
    def pay(self, entity):
        if self.owner is not None and entity.active:
            
