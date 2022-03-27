from  src.entity import Entity
from  src.job import Job
import random
from  src.contract import Contract

class job_market(Entity):
    name = "Job Market"
    business = []
    people = []
    owner = None
    money = 0
    tax_rate = 0.1
    jobs = {}
    specializations = {} # Esto aún hay que implementarlo
    # database = MarketDatabase()

    def __init__(self, name, owner, money, tax_rate):
        self.name = name
        self.owner = owner
        self.money = money
        self.tax_rate = tax_rate
        self.jobs = {}
        self.specializations = {}

    def __str__(self):
        return f"{self.name} has {len(self.business)} businesses and {len(self.people)} people"

    def add_business(self, business):
        self.business.append(business)

    def add_person(self, person):
        self.people.append(person)

    # Sin uso
    # def add_specialization(self, specialization):
    #     self.specializations[specialization.name] = specialization.value

    def add_job(self, job):
        if not job:
            return 0
        if not job.specialization in self.jobs:
            self.jobs[job.specialization] = []
        self.jobs[job.specialization].append(job)

    def sort_job(self, job):
        return job.money

    def clean_market(self):
        self.jobs = {}


    # Function to make all jobs on a free market
    def free_commerce(self):
        # For each specialization on market
        for specialization in self.jobs:
            # Get all buy jobs on market
            contractor_jobs = []
            for job in self.jobs[specialization]:
                if job.contractor:
                    contractor_jobs.append(job)
            # Get all contractor jobs on market
            contractee_jobs = []
            for job in self.jobs[specialization]:
                if not job.contractor:
                    contractee_jobs.append(job)
            print("ESPECIALIZACION ", specialization)
            print("============================================================================================================")
            print("OFERTA")
            print("-------")
            for t in contractor_jobs:
                print(t)
            print("DEMANDA")
            print("------")
            for t in contractee_jobs:
                print(t)
            

            # Shuffle order of jobs
            random.shuffle(contractor_jobs)
            random.shuffle(contractee_jobs)
            # Loop trough all the buy jobs
            for job in contractor_jobs:
                # Loop through all the contractor jobs
                for contractee_job in contractee_jobs:
                    found = False

                    # If the buy money is higher or equal than the contractor money
                    if job.money >= contractee_job.money and job.time >= contractee_job.time and contractee_job.money != 0:
                        # Create a contract
                        contract = job.entity.contract(contractee_job.entity, job.money, job.time)
                        # Add contract to the contratee
                        contractee_job.entity.contract = contract
                        # Set contract to 0 so it doesn't show again
                        job.money = 0
                        contractee_job.money = 0
                        # Remove the job from the market
                        self.jobs[specialization].remove(job)
                        self.jobs[specialization].remove(contractee_job)
                        # Change contract price 
                        job.entity.contracts_price[specialization] = round(job.entity.contracts_price[specialization] - job.entity.contracts_price[specialization]* 0.05,2)
                        contractee_job.entity.contracts_price[specialization] = round(contractee_job.entity.contracts_price[specialization] + contractee_job.entity.contracts_price[specialization]* 0.05,2)
                        found = True
                        break
                    if not found:
                        contractee_job.entity.contracts_price[specialization] = round(contractee_job.entity.contracts_price[specialization] - contractee_job.entity.contracts_price[specialization]* 0.05,2)


                        
 
        self.clean_market()

