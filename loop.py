import imp
from json.tool import main
import entity
import person
import farm
import mine
import city
import market
import state
import os


import random


def demo():

    # Create ten people
    people = []
    businesses = []

    for i in range(10):
        people.append(person.Person("Person " + str(i),
                      random.randint(0, 100), random.randint(0, 10)))
    # Create a farm
    f = farm.Farm("Farm", people[0], random.randint(100, 1000), 5)
    businesses.append(f)

    # Create a mine
    mi = mine.Mine("Mine", people[1], random.randint(100, 1000), 5)
    businesses.append(mi)
    # Create a city
    c = city.City("City", [f,mi], people, 0.1, 1000)

    # Create a market
    m = market.Market("Market", people[1], random.randint(0, 100), 0.1)
    # Create contracts for the farm
    f.contract(people[2], 2, time=10000)
    f.contract(people[3], 2, time=10000)
    f.contract(people[4], 2, time=10000)
    f.contract(people[5], 2, time=10000)
    mi.contract(people[6], 2, time=10000)
    mi.contract(people[7], 2, time=10000)
    mi.contract(people[8], 2, time=10000)

    g = person.Person("Guille", 20, 5000)
    k = person.Person("Kelia", 20, 5000)
    people.append(g)
    people.append(k)

    # Create a second farm 
    f2 = farm.Farm("Granja k", k, random.randint(100, 1000), 5)
    businesses.append(f2)


    # Create a state
    s = state.State("Townhall", k, 500)
    s.add_city(c)
    

    f2.contract(g, 2, time=400)
    f2.contract(k, 2, time=400)
    f.set_owner(people[9])

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
        for b in businesses:
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
        print("Proyects:")
        for pro in s.proyects:
            print(pro)
        print("Future proyects:")
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
        for p in people:
            p.work()
            p.eat("food")
            p.create_trades(m)
        
        # Businesses
        for business in businesses:
            new_cs = []
            for contract in business.work_contracts:
                new_c = contract.fullfill()
                if new_c is not None:
                    new_cs.append(contract)
            business.work_contracts = new_cs
            business.produce()
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
        print("PRE TAXES ", s.money)
        s.tax()
        print("POST TAXES ", s.money)
        s.work()
        s.process_needed_resourcess(m)
        if s.money > 50 and len(s.proyects) < 3:
            s.add_infrastructure(c)
        
        # Market
        m.free_commerce()







if __name__ == "__main__":
    demo()
