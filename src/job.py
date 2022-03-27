

class Job:
    entity = None
    money = 1
    time = 1
    contractor = False
    specialization = "None"

    def __init__(self, entity, money, time, specialization, contractor):
        self.entity = entity
        self.money = money
        self.time = time
        self.specialization = specialization
        self.contractor = contractor
    
    def __str__(self):
        return f"{self.entity.name} is a {self.specialization} job with {self.money} money and {self.time} time"
    

