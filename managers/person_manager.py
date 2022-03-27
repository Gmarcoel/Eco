from managers.manager import Manager
from managers.business_manager import create_business
from src import person
from src.project import Project
import json
import random


class PersonManager(Manager):
    person = None
    job_market = None
    market = None
    inversion = False
    city = None


    project_resources = {}
    project = None

    def __init__(self, person, job_market, market, city):
        self.person = person
        self.job_market = job_market
        self.market = market
        self.city = city
        self.project_resources = {}
    
    def do(self):

        # Basic needs
        self.person.work(self.job_market)
        self.person.eat("food")
        self.person.create_trades(self.market)

        # Decissions:
        self.grow()

        # Jobs
        self.entrepreneur()
        self.invest()
        self.manage()

        # Family
        # self.marry()
        # self.children()
        # self.family()
        # self.die()
    
    # Function to grow
    def grow(self):
        self.person.age += 1
    
    # Function to entrepeneur
    def entrepreneur(self):

        entrepeneurship = 0.4
        
        # If already inversion return
        if self.inversion:
            return
        """
        # if balance negative return
        if self.person.check_balance() < 0:
            return
        # If is entrepeneur increase chance
        if "entrepeneur" in self.person.traits:
            entrepeneurship += 0.4
        
        # Random chance to become an entrepeneur
        if random.random() < entrepeneurship:
            return
        """
        if self.person.money < 100000:
            return

        
        # Buy terrain in city
        if not self.city.buy_terrain(self.person):
            return
        
        # Create project
        if self.person.specialization == "None":

            # Choose random project from list
            # l = ["farm", "mine", "infrastructure"]
            l = ["farm"]
            project = random.choice(l)
            # Open the projects json file
            with open("data/projects.json", "r") as f:
                data = json.load(f)
                # Get the resources needed for the project
                resources = data["projects"][project]["resources"]
                # Get the time needed for the project
                time = data["projects"][project]["time"]
                # Create the project
                p = Project(project, self.city, self.person, 0, resources, time)
                # Add the project to the list of projects
                self.project = p
            self.inversion = True


    # Invest in current project
    def invest(self):
        # If not inversion return
        if not self.inversion:
            return

        
        # If project is accomplished
        if self.project.accomplish(self.person):
            # Create new business
            b = create_business(self.project.name,self.person, self.person.money)
            self.person.money = 0
            # Remove project from list
            self.project = None
            # Set inversion to false
            self.inversion = False
            # Add business to list of businesses
            self.person.businesses.append(b)
            # Add business to city
            self.city.add_business(b)
            
            print("HE LLEGADO AQUI ESTO ES BASTANTE")
            print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
            print(b)
            return

        """
        # if balance negative return
        if self.person.check_balance() < 0:
            return
        """
        # Invest in project
        for res in self.project_resources:
            res = 0
        for key in self.project.resources:
            if not key in self.project_resources:
                self.project_resources[key] = 0
            self.project_resources[key] += self.project.resources[key]
        # Create trades for all needed resources
        for key in self.project_resources:
            t = self.person.trade(key, self.person.get_expected_price(
                key), False, self.project_resources[key])
            self.market.add_trade(t)
                

        
    # Manage current businesses

    def manage(self):
        pass


        
        
    
