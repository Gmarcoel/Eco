from managers.manager import Manager
from src import business
from src.project import Project
import json
import random

from src.farm import Farm
from src.mine import Mine
from src.sawmill import Sawmill
from src.constructor import Constructor




class business_manager(Manager):
    business = None

    def __init__(self, business):
        self.business = business
    
    def do(self):
        pass

def create_business(business_type, owner, money):
    if business_type == "farm":
        # Generate random name
        name = "Farm " + str(random.randint(1, 10000))
        return Farm(name, owner, money)
    
    if business_type == "mine":
        # Generate random name
        name = "Mine " + str(random.randint(1, 10000))
        return Mine(name, owner, money)
    
    if business_type == "sawmill":
        # Generate random name
        name = "Sawmill " + str(random.randint(1, 10000))
        return Sawmill(name, owner, money)
    
    if business_type == "constructor":
        # Generate random name
        name = "Constructor " + str(random.randint(1, 10000))
        return Constructor(name, owner, money)

    
