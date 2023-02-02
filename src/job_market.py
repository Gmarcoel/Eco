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
    total_contracts_price = 0
    total_contracts_ammount = 0
    average_contracts_price = 1

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
        checked = []
        for specialization in self.jobs:
            for job in self.jobs[specialization]:
                if job.contractor:
                    if job.entity not in checked:
                        job.entity.contracts_price[specialization] = round(job.entity.contracts_price[specialization] + job.entity.contracts_price[specialization]* 0.5,2)
                        checked.append(job.entity)
                else:
                    if not "food" in job.entity.items_price:
                        job.entity.items_price["food"] = 1
                    if job.entity.contracts_price[specialization] >= 2 * job.entity.items_price["food"]:
                        job.entity.contracts_price[specialization] = round(job.entity.contracts_price[specialization] - job.entity.contracts_price[specialization]* 0.1,2)
                        # Prueba
                        average = self.average_contracts_price
                        expected = job.entity.contracts_price[specialization]
                        job.entity.contracts_price[specialization] = round((average + expected + expected) / 3, 2)

        
        self.jobs = {}


    def sort_job(self, job):
        return job.money

    # Function to make all jobs on a free market
    def free_commerce(self):
        self.total_contracts_price = 0
        self.total_contracts_ammount = 0

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
            #"""
            print("ESPECIALIZACION ", specialization)
            print("============================================================================================================")
            print("OFERTA")
            print("-------")
            last_t = ''
            for t in contractor_jobs:
                if str(t) != str(last_t):
                    print(t)
                last_t = t
            print("DEMANDA")
            print("------")
            last_t = ''
            for t in contractee_jobs:
                if str(t) != str(last_t):
                    print(t)
                last_t = t
            #"""
            
            # If more contractors than contractees contractees decide the price
            if len(contractor_jobs) > len(contractee_jobs):
                contractor_jobs.sort(key=self.sort_job, reverse=True)
                random.shuffle(contractee_jobs)
            # If more contractees than contractors contractors decide the price
            elif len(contractee_jobs) > len(contractor_jobs):
                # Shuffle order of jobs
                random.shuffle(contractor_jobs)
                # random.shuffle(contractee_jobs)
                contractee_jobs.sort(key=self.sort_job)
            # If same number of contractors and contractees
            else:
                # Shuffle order of jobs
                random.shuffle(contractor_jobs)
                random.shuffle(contractee_jobs)
            # Put farming jobs first ###################### CHAPUZA A CAMBIAR EN EL FUTURO para que no mueran de hambre
            for job in contractor_jobs:
                if job.entity.sector == "farming":
                    contractor_jobs.remove(job)
                    contractor_jobs.insert(0, job)
            # Loop trough all the buy jobs
            for job in contractor_jobs:
                # Loop through all the contractor jobs
                for contractee_job in contractee_jobs:
                    found = False

                    # If hungry look for a job of farming sector
                    if contractee_job.entity.hungry > 3:
                        if job.entity.sector == "farming":
                            # Fill database data
                            self.total_contracts_price += job.money
                            self.total_contracts_ammount += 1
                            job.entity.manager.contracted += 1
                            job.entity.manager.contracted_price += job.money
                            # Create a contract
                            contract = job.entity.contract(contractee_job.entity, job.money, job.time)
                            # Add contract to the contratee
                            contractee_job.entity.contract = contract
                            # Set contract to 0 so it doesn't show again
                            job.money = 0
                            contractee_job.money = 0
                            # Remove the job from the market
                            self.jobs[specialization].remove(job)

                            if contractee_job in self.jobs: # NO SE POR QUE DA ERROR SI SE QUITA ESTO PERO IMPLICA QUE ALGO ESTA MUY MUY MUY MAL
                                self.jobs[specialization].remove(contractee_job)
                            # Change contract price 
                            
                            job.entity.contracts_price[specialization] = round(job.entity.contracts_price[specialization] - job.entity.contracts_price[specialization]* 0.1,2) # 0.05
                            contractee_job.entity.contracts_price[specialization] = round(contractee_job.entity.contracts_price[specialization] + contractee_job.entity.contracts_price[specialization]* 0.1,2)

                            # Prueba
                            average = self.average_contracts_price
                            expected = job.entity.contracts_price[specialization]
                            job.entity.contracts_price[specialization] = round((average + expected + expected) / 3, 2)
                            
                            found = True
                            break
                    
                    # If the buy money is higher or equal than the contractor money
                    if job.money >= contractee_job.money and job.time >= contractee_job.time and contractee_job.money != 0:
                        # Fill database data
                        self.total_contracts_price += job.money
                        self.total_contracts_ammount += 1
                        job.entity.manager.contracted += 1
                        job.entity.manager.contracted_price += job.money
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
                        
                        job.entity.contracts_price[specialization] = round(job.entity.contracts_price[specialization] - job.entity.contracts_price[specialization]* 0.1,2)
                        contractee_job.entity.contracts_price[specialization] = round(contractee_job.entity.contracts_price[specialization] + contractee_job.entity.contracts_price[specialization]* 0.1,2)
                        
                        # Prueba
                        average = self.average_contracts_price
                        expected = job.entity.contracts_price[specialization]
                        job.entity.contracts_price[specialization] = round((average + expected + expected) / 3, 2)


                        found = True
                        break

                        
        
        if self.total_contracts_ammount != 0:
            self.average_contracts_price = round(self.total_contracts_price / self.total_contracts_ammount,2)
        self.clean_market()

