from sre_parse import State
from src.world import World
from json.tool import main
from typing import List
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
from src import chocolate_factory
from src import housing
from src import furniture_factory
from src import science_hub
from src import consumer_goods_factory

from controls.state_control import StateControl

from managers import person_manager
from src.new import New

import os


import random

# Print variables
pp = False
pb = False
ps = False
pc = False
pm = False
pj = False
pt = False
ptr = False



def demo():
    global pp 
    global pb
    global ps
    global pc
    global pm
    global pj
    global pt 
    global ptr 

    # Create ten people
    people = []
    businesses = []

    for i in range(30):
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
    f.contract(people[2], 0.8, time=10)
    # f.contract(people[3], 0.8, time=10000)
    # f.contract(people[4], 1, time=10000)
    # f.contract(people[5], 1, time=10000)
    mi.contract(people[6], 2, time=10)
    # mi.contract(people[7], 2, time=10000)
    # mi.contract(people[8], 2, time=10000)

    g = person.Person("Guille", 20, 500)
    k = person.Person("Kelia", 20, 500)
    people.append(g)
    people.append(k)

    g.partner = k
    k.partner = g

    # Create a second farm 
    f2 = farm.Farm("Granja k", k, random.randint(1000, 2000), 5)
    k.businesses.append(f2)
    businesses.append(f2)

    # Create a sawmill
    saw = sawmill.Sawmill("Sawmill", g, random.randint(1000, 2000), 5)
    businesses.append(saw)

    # Create a constructor
    cons = constructor.Constructor("Constructor", g, random.randint(1000, 2000), 5)
    businesses.append(cons)

    # Contract more people to the sawmill
    saw.contract(people[7], 0.8, time=10)
    
    # Contract more people to the constructor
    cons.contract(people[8], 0.8, time=10)



    # Create a state
    s = state.State("Townhall", k, 500)
    s.add_city(c)
    c.state = s
    

    f2.contract(g, 1, time=20)
    f2.contract(k, 2, time=20)
    f.contract(people[11], 2, time=40)
    f.contract(people[12], 2, time=40)
    f.contract(people[13], 2, time=40)
    f.contract(people[14], 2, time=40)

    
    # f.set_owner(people[9])
    f.set_owner(s)
    s.businesses.append(f)
    mi.set_owner(s)
    s.businesses.append(mi)
    saw.set_owner(s)
    s.businesses.append(saw)
    cons.set_owner(s)
    s.businesses.append(cons)

    # Create job market
    jm = job_market.job_market("Job Market", s, 1000, 0.1)

    # Add business to the city
    for b in businesses:
        c.add_business(b)


    # Managers
    # pm = []
    # for p in people:
    #     pm.append(person_manager.PersonManager(p,jm,m,c))
    
    # Copy all the people in people to c.people
    c.people = people.copy()
    c.entities = businesses + c.people

    states = []
    states.append(s)
    
    w = World()
    for b in businesses:
        w.new_businesses.append(New(b, c, m, jm))
    for p in people:
        w.new_people.append(New(p, c, m, jm))
    for st in states:
        w.new_states.append(New(st, c, m, jm))
    w.update()

    k.inmortal = True
    g.inmortal = True

    

    turn = 0



    while True:
        

        


        # Wait for a turn


        give_input(c, m, s, jm, w)


        print("***************************")
        os.system('cls' if os.name == 'nt' else 'clear')
        # Do the turn
        w.update()
        w.do()

        if pp:
            print_people(w)
        if pb:
            print_businesses(w)
        if ps:
            print_states(w)

        
        # Market
        # change stdout

        data = m.free_commerce()
        if ptr:
            print("Trades")
            print(data)
            print("===========================")

        jm.free_commerce()

        # Print the city
        if pc:
            print("City:")
            print("===========================")
            print(c)
        
        # Print the market
        if pm:
            print("Market:")
            print(m)
            print("===========================")

        
        
        # Print the turn
        if pt:
            print("Turn: " + str(turn))
            print("===========================")
        if pm:
            print("Market prices:")
            m.database.print_database()
            print("===========================")





def give_input(c,m,jm,s,w):
    global pp 
    global pb
    global ps
    global pc
    global pm
    global pj
    global pt 
    global ptr 
    inp = input("Press enter to continue...\n")
    if inp == 's':
        o = sawmill.Sawmill("New Sawmill", s, 1000)
        n = New(o, c, m, jm)
        w.new_businesses.append(n)
        c.businesses.append(o)
        s.businesses.append(o)
    elif inp == 'c':
        o = constructor.Constructor("New Constructor", s, 1000)
        n = New(o, c, m, jm)
        w.new_businesses.append(n)
        c.businesses.append(o)
        s.businesses.append(o)
    elif inp == 'f':
        o = farm.Farm("New Farm", s, 1000, 5)
        n = New(o, c, m, jm)
        w.new_businesses.append(n)
        c.businesses.append(o)
        s.businesses.append(o)
    elif inp == 'm':
        o = mine.Mine("New Mine", s, 1000, 5)
        n = New(o, c, m, jm)
        w.new_businesses.append(n)
        c.businesses.append(o)
        s.businesses.append(o)
    elif inp == 'p':
        # Person
        o = person.Person("New Person", s, 1000)
        n = New(o, c, m, jm)
        w.new_people.append(n)
        c.people.append(o)
    
    elif inp == 'pp':
        pp = not pp
    elif inp == 'pb':
        pb = not pb
    elif inp == 'ps':
        ps = not ps
    elif inp == 'pc':
        pc = not pc
    elif inp == 'pm':
        pm = not pm
    elif inp == 'pj':
        pj = not pj
    elif inp == 'pt':
        pt = not pt
    elif inp == 'ptr':
        ptr = not ptr


def pass_turn(w):
    w.update()
    w.do()


def generate_world():
    # Create ten people
    people = []
    businesses = []

    for i in range(100):
        people.append(person.Person("Person " + str(i),
                      random.randint(18, 80), random.randint(20, 80)))
    # Create a farm
    f = farm.Farm("Farm", people[0], random.randint(50, 100), 5)
    businesses.append(f)
    people[0].businesses.append(f)



    # Create a mine
    mi = mine.Mine("Mine", people[1], random.randint(50, 100), 5)
    businesses.append(mi)
    people[1].businesses.append(mi)
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

    g = person.Person("personaje", 20, 500)
    k = person.Person("alcalde", 20, 500)
    people.append(g)
    people.append(k)

    g.partner = k
    k.partner = g

    # Create a second farm 
    f2 = farm.Farm("Farm 2", k, random.randint(50, 100), 5)
    k.businesses.append(f2)
    businesses.append(f2)

    # Create a sawmill
    saw = sawmill.Sawmill("Sawmill", g, random.randint(50, 100), 5)
    businesses.append(saw)
    g.businesses.append(saw)

    #saw2 = sawmill.Sawmill("Sawmill 2", people[3], random.randint(50, 100), 5)
    #businesses.append(saw2)
    #people[3].businesses.append(saw2)

    # Create a constructor
    cons = constructor.Constructor("Constructor", g, random.randint(50, 100), 5)
    businesses.append(cons)
    g.businesses.append(cons)

    # Create a constructor
    #cons2 = constructor.Constructor("Constructor 2", people[4], random.randint(50, 100), 5)
    #businesses.append(cons2)
    #people[4].businesses.append(cons2)

    # Create a chocolate factory
    choco = chocolate_factory.ChocolateFactory("Chocolateastic", g, random.randint(50, 100))
    businesses.append(choco)
    g.businesses.append(choco)

    # Create a chocolate factory
    #choco2 = chocolate_factory.ChocolateFactory("Chocolate Factory 2", people[5], random.randint(50, 100))
    #businesses.append(choco2)
    #people[5].businesses.append(choco2)

    # Create a housing business
    #hous = housing.Housing("Housing", k, 2000)
    #businesses.append(hous)
    #k.businesses.append(hous)

    # Create a chocolate factory
    #fur = furniture_factory.FurnitureFactory("Ikoa", people[2], random.randint(50, 100))
    #businesses.append(fur)
    #people[2].businesses.append(fur)

    # Create a science hub
    sci = science_hub.ScienceHub("Tech Labs", people[6], random.randint(50, 100))
    businesses.append(sci)
    people[6].businesses.append(sci)

    # Create a science hub
    sci2 = science_hub.ScienceHub("Science & More", people[7], random.randint(50, 100))
    businesses.append(sci2)
    people[7].businesses.append(sci2)

    # Create a consumer goods factory
    goo = consumer_goods_factory.GoodsFactory("The Big Factory", people[10], random.randint(50, 100))
    businesses.append(goo)
    people[10].businesses.append(goo)

    # Contract more people to the sawmill
    saw.contract(people[7], 0.8, time=10)
    
    # Contract more people to the constructor
    cons.contract(people[8], 0.8, time=10)

    c.markets.append(m)

    # Create a state
    s = state.State("Townhall", k, 500)
    s.add_city(c)
    c.state = s
    

    f2.contract(g, 1, time=400)
    f2.contract(k, 2, time=400)
    f.contract(people[11], 2, time=10)
    f.contract(people[12], 2, time=10)
    f.contract(people[13], 2, time=10)
    f.contract(people[14], 2, time=10)

    """
    # f.set_owner(people[9])
    f.set_owner(s)
    s.businesses.append(f)
    mi.set_owner(s)
    s.businesses.append(mi)
    saw.set_owner(s)
    s.businesses.append(saw)
    cons.set_owner(s)
    s.businesses.append(cons)
    """

    # Create job market
    jm = job_market.job_market("Job Market", s, 1000, 0.1)

    # Add business to the city
    for b in businesses:
        c.add_business(b)


    # Managers
    # pm = []
    # for p in people:
    #     pm.append(person_manager.PersonManager(p,jm,m,c))
    
    # Copy all the people in people to c.people
    c.people = people.copy()
    c.entities = businesses + c.people

    states = []
    states.append(s)
    
    w = World()
    for b in businesses:
        w.new_businesses.append(New(b, c, m, jm))
    for p in people:
        w.new_people.append(New(p, c, m, jm))
    for st in states:
        w.new_states.append(New(st, c, m, jm))

    w.new_cities.append(New(c, c, m, jm))

    w.new_markets.append(New(m, c, m, jm))
    w.new_job_markets.append(New(jm, c, m, jm))

    w.update()

    k.inmortal = True
    g.inmortal = True

    f.manager.fixed_sell_price      = 3
    f.manager.fixed_amount_workers = -1
    f.manager.fixed_contract_price  = 10
    f.manager.fixed_science_buy     = 5
    f.manager.fixed_science_price   = 10

    return w

worlds = []
worlds.append(generate_world())

def ret_worlds():
    return worlds


def print_people(w):
    print("People:")
    print("===========================")
    for p in w.people_managers:
        print(p.person)

def print_businesses(w):
    print("Businesses:")
    print("===========================")
    public = []
    private = []
    for b in w.business_managers:
        bus = b.business
        if bus.owner == None or isinstance(bus.owner, state.State):
            public.append(bus)
        else:
            private.append(bus)
    print("Public:")
    for b in public:
        print(b)
        for con in b.work_contracts:
            print("\t" + str(con))
    print("Private:")
    for b in private:
        print(b)
        for con in b.work_contracts:
            print("\t" + str(con))

def print_states(w):
    print("States:")
    print("===========================")
    for s in w.states_managers:
        print(s.state)


def get_public_private_ratio(businesses):
    public = 0
    private = 0
    for b in businesses:
        if b.owner == None or isinstance(b.owner, state.State):
            public += 1
        else:
            private += 1
    if public + private == 0:
        return 0
    return public / (public + private)


def set_state_control(sm):
    return StateControl(sm)


def show_last_law(sm):
    return sm.last_law

def get_deaths_natural_starvation_ratio(city_manager):
    if city_manager.deaths == 0:
        return 1
    return  1 - city_manager.deaths_by_hunger / city_manager.deaths


def is_public(business):
    return business.owner == None or isinstance(business.owner, state.State)


# if __name__ == "__main__":
#     demo()
