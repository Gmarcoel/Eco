from controls.control import Control

class StateControl(Control):
    statem = None

    def __init__(self, statem):
        super().__init__()
        self.statem = statem

    
    def manual(self):
        self.statem.manual = not self.statem.manual
    
    def basics_manual(self):
        self.statem.basics_manual = not self.statem.basics_manual

    def print_money(self, ammount):
        self.statem.print_money(ammount)
    
    def privatize(self, business):
        self.statem.privatize(business)
    

        
