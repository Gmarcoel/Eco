from managers.manager import Manager
from src import business
from src.project import Project
import json
import random

from src.farm import Farm
from src.mine import Mine



class business_manager(Manager):
    business = None

    def __init__(self, business):
        self.business = business
    
    def do(self):
        pass

def create_business(business_type, owner, money):
    print("business_type: %s", business_type)
    if business_type == "farm":
        # Generate random name
        name = "Farm" + str(random.randint(1, 10000))
        return Farm(name, owner, money)
    
