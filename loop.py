import imp
from json.tool import main
from src import entity
from src import person
from src import farm
from src import mine
from src import city
from src import market
from src import state
from src import job_market
from src import sawmill
from src import constructor

from managers import person_manager

import os


import random


def demo():

    # Create ten people
    people = []
    businesses = []

    for i in range(10):
        people.append(person.Person("Person " + str(i),
                      random.randint(18, 80), random.randint(80, 800)))
    # Create a farm
    f = farm.Farm("Farm", people[0], random.randint(1000, 2000), 5)
    businesses.append(f)

    # Create a mine
    mi = mine.Mine("Mine", people[1], random.randint(3000, 5000), 5)
    businesses.append(mi)
    # Create a city
    c = city.City("City", [], people, 0.1, 1000)

    # Create a market
    m = market.Market("Market", people[1], random.randint(0, 100), 0.1)
    # Create contracts for the farm
    f.contract(people[2], 0.8, time=10000)
    # f.contract(people[3], 0.8, time=10000)
    # f.contract(people[4], 1, time=10000)
    # f.contract(people[5], 1, time=10000)
    mi.contract(people[6], 2, time=10000)
    # mi.contract(people[7], 2, time=10000)
    # mi.contract(people[8], 2, time=10000)

    g = person.Person("Guille", 20, 50)
    k = person.Person("Kelia", 20, 500000)
    people.append(g)
    people.append(k)

    # Create a second farm 
    f2 = farm.Farm("Granja k", k, random.randint(1000, 2000), 5)
    businesses.append(f2)

    # Create a sawmill
    saw = sawmill.Sawmill("Sawmill", g, random.randint(1000, 2000), 5)
    businesses.append(saw)

    # Create a constructor
    cons = constructor.Constructor("Constructor", g, random.randint(1000, 2000), 5)
    businesses.append(cons)

    # Contract more people to the sawmill
    saw.contract(people[7], 0.8, time=10000)
    
    # Contract more people to the constructor
    cons.contract(people[8], 0.8, time=10000)



    # Create a state
    s = state.State("Townhall", k, 500)
    s.add_city(c)
    

    f2.contract(g, 2, time=400)
    f2.contract(k, 2, time=400)
    
    # f.set_owner(people[9])
    f.set_owner(s)
    mi.set_owner(s)
    saw.set_owner(s)
    cons.set_owner(s)

    # Create job market
    jm = job_market.job_market("Job Market", s, 1000, 0.1)

    # Add business to the city
    for b in businesses:
        c.add_business(b)


    # Managers
    pm = []
    for p in people:
        pm.append(person_manager.PersonManager(p,jm,m,c))

    



    turn = 0
    while True:
        
        # Print the contracts
        print("===========================")
        print("===========================")
        print("Contracts:")
        print("===========================")
        for b in businesses:
            for contract in b.work_contracts:
                print(contract)
        print("===========================")
        print("===========================")
        
        print("Business:")
        print("===========================")
        for b in c.businesses:
            print(b)
        print("===========================")
        
        print("===========================")
        print("People:")
        print("===========================")
        for p in people:
            print(p)
        # Print the city
        print("===========================")
        print("===========================")
        print("City:")
        print("===========================")
        print(c)
        
        # Print the market
        print("===========================")
        print("===========================")
        print("Market:")
        print("===========================")
        print(m)
        print("===========================")
        print("===========================")
        
        # Print the state
        print("===========================")
        print("===========================")
        print("State:")
        print("===========================")
        print(s)
        print("projects:")
        for pro in s.projects:
            print(pro)
        print("Future projects:")
        print(s.in_construction)
        # Print the turn
        print("===========================")
        print("===========================")
        print("Turn: " + str(turn))
        print("===========================")
        print("===========================")
        print("Market prices:")
        print("===========================")
        m.database.print_database()
        print("===========================")
        print("===========================")
        # Wait for a turn
        input("Press enter to continue...")
        print("***************************")
        os.system('cls' if os.name == 'nt' else 'clear')
        # Do the turn
        
        # Persons
        for perm in pm:
            perm.do()
        # for p in people:
        #     p.work(jm)
        #     p.eat("food")
        #     p.create_trades(m)
        
        # Businesses
        for business in c.businesses:
            new_cs = []
            for contract in business.work_contracts:
                new_c = contract.fullfill()
                if new_c is not None:
                    new_cs.append(contract)
            business.work_contracts = new_cs
            business.produce(jm)
            business.sell(m)
            business.create_trades(m)
        # Give money to the busssinesses
        for business in businesses:
            debt_money = 0
            for contract in business.work_contracts:
                debt_money += contract.money1
            if business.owner is not None and business.money < debt_money :
                business.owner.subsidize(business, business.owner.money * 0.3)
                business.negative = 0

        # State
        s.work()
        s.process_needed_resourcess(m)
        if s.money > 50 and len(s.projects) < 3:
            s.add_infrastructure(c)
        
        # Market
        m.free_commerce()
        jm.free_commerce()







if __name__ == "__main__":
    demo()
