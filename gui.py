from tkinter import *
from turtle import color
from venv import create
from loop import *
import matplotlib.pyplot as plt
from matplotlib import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a GUI
root = Tk()

callbacks = []

def menu_page():
    global callbacks
    callbacks.append(menu_page)
    clean_up()
    print("Menu clicked")
    # Put the background dark grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="ECONOMICS", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a world button
    myButton = Button(pages_panel, text="WORLDS", bg="#222", fg="white", command=worlds_page)
    # Make the button big
    myButton.config(font=("Courier", 44))
    # Put the button in the window
    myButton.pack()



def worlds_page():
    global callbacks
    callbacks.append(worlds_page)
    clean_up()
    print("Worlds clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="WORLDS", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each world if ret_worlds() is not empty
    worlds = ret_worlds()
    if worlds:
        for world in worlds:
            # Create a button for each world with lable world.name and the world as an argument
            myButton = Button(pages_panel, text=world.name, bg="#222", fg="white", command=lambda world=world: world_page(world))
            # Make the button big
            myButton.config(font=("Courier", 44))

            myButton.pack()
    
    # Create a back button
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=menu_page)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

current_world = None
def world_page(world = None):
    global callbacks
    callbacks.append(world_page)
    global current_world
    if world:
        current_world = world
    else :
        world = current_world
    clean_up()
    pages_panel.configure(background='#222')
    # Create a button for each city in the world
    for city_man in world.cities_managers:
        city = city_man.city
        myButton = Button(pages_panel, text=city.name, bg="#222", fg="white", command=lambda city=city_man: city_page(city_man))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack(expand=True)

    next_turn_button(world_page, pages_panel)
    # Create a back button
    # Create a go back button that executes go_back
    myButton = Button(pages_panel, text="Back", bg="blue", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))

current_citym = None


def city_page(citym = None):
    global callbacks
    callbacks.append(city_page)
    global current_world, current_citym, current_statem
    if citym:
        current_citym = citym
    else:
        citym = current_citym
    world = current_world
    
    city = citym.city
    current_statem = city.state.manager
    clean_up()
    print("City clicked")
    # Put the background light grey
    pages_panel.configure(background='#222') 

    # Create a panel for the city
    buttons_panel = PanedWindow(pages_panel, orient=VERTICAL, background="#222")
    buttons_panel.pack(fill=BOTH, expand=True)
    
    # Create a label
    myLabel = Label(buttons_panel, text=city.name, bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack(expand=True)

    # Show infrastructure
    myLabel = Label(buttons_panel, text="Infrastructure " + str(city.infrastructure), bg="#222", fg="white")
    myLabel.config(font=("Courier", 20))
    myLabel.pack(expand=True)


    # Show population and deaths
    myLabel = Label(buttons_panel, text="Population " + str(len(city.people)) + " Average salary: " + str(city.state.manager.job_market.average_contracts_price), bg="#222", fg="white")
    myLabel.config(font=("Courier", 20))
    myLabel.pack(expand=True)
    # Show deaths
    myLabel = Label(buttons_panel, text="Deaths " + str(citym.deaths), bg="#222", fg="white")
    myLabel.config(font=("Courier", 20))
    myLabel.pack(expand=True)


    
    # Create a button for the businesses
    myButton = Button(buttons_panel, text="Businesses", bg="#222", fg="white", command=lambda citym=citym: businesses_page(citym))
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)

    # Create a button for the closed businesses
    myButton = Button(buttons_panel, text="Closed Businesses", bg="#222", fg="white", command=lambda citym=citym: closed_businesses_page(citym))
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)

    # Create a button for the people
    myButton = Button(buttons_panel, text="People", bg="#222", fg="white", command=lambda citym=citym: people_page(citym))
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)

    # Create a button for the markets
    for market in city.markets:
        myButton = Button(buttons_panel, text=market.name, bg="#222", fg="white", command=lambda market=market.manager: market_page(market))
        myButton.config(font=("Courier", 20))
        myButton.pack(expand=True)
    
    # Create a button for the state
    myButton = Button(buttons_panel, text="State", bg="#222", fg="white", command=lambda statem=city.state.manager: state_page(statem))
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)


    
    # Create a go back button that executes go_back
    myButton = Button(buttons_panel, text="Back", bg="#222", fg="white", command=go_back)
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)
    
    # Next turn button
    next_turn_button(city_page,buttons_panel)

    # Create horizontal panel for graphics
    graphics_panel = PanedWindow(pages_panel, orient=HORIZONTAL)
    graphics_panel.pack(fill=BOTH, expand=True)

    # Create a vertical panel for charts
    charts_panel = PanedWindow(graphics_panel, orient=VERTICAL)
    # Create a frame for the charts
    charts_panel.pack(fill=BOTH, expand=True)
    graphics_panel.add(charts_panel)

    # Create a vertical panel for charts
    charts_panel2 = PanedWindow(graphics_panel, orient=VERTICAL)
    # Create a frame for the charts
    charts_panel2.pack(fill=BOTH, expand=True)
    graphics_panel.add(charts_panel2)


    chart = plot_pie_chart_public_private_bussiness(city.businesses, charts_panel)
    charts_panel.add(chart)
    chart = plot_pie_chart_deaths_natural_starvation(citym, charts_panel)
    charts_panel.add(chart)

    chart = None
    chart = plot_pie_chart_pib(citym, charts_panel2)
    if chart:
        charts_panel2.add(chart)
    
    chart = None
    chart = plot_pie_chart_people_status(citym, charts_panel2)
    if chart:
        charts_panel2.add(chart)


    charts_panel3 = PanedWindow(graphics_panel, orient=VERTICAL)
    charts_panel3.pack(fill=BOTH, expand=True)
    graphics_panel.add(charts_panel3)

    chart = plot_borns_deaths(citym, charts_panel3)
    charts_panel3.add(chart)

    if city.people != []:
        job_market = city.people[0].manager.job_market
        chart = plot_average_contract_price(job_market, charts_panel3)
        charts_panel3.add(chart)


    



current_entitym = None

def people_page(entitym = None):
    global callbacks
    callbacks.append(people_page)
    global current_entitym 
    if entitym:
        current_entitym = entitym
    else:
        entitym = current_entitym
        
    entity = entitym.entity

    clean_up()
    pages_panel.configure(background='#222')
    print("People clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="People", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each person in the city
    # Create a sidebar if there are more than 10 people
    if len(entity.people) > 10:
        # Create a scrollbar
        create_scroll(entity.people, person_page, "person")
        


        """
        # Create a scrollbar
        text = Text(pages_panel, height=len(entity.people), width=20)
        text.pack(side="left")

        sb = Scrollbar(pages_panel, command=text.yview)
        # Set the scrollbar to scroll through the windows
        sb.pack(side="right", fill="y")
        text.configure(yscrollcommand=sb.set)
        
        ...
        for person in entity.people:
            personm = person.manager
            # Create a button for each person with lable person.name and the person as an argument and a width of 1/5 of the screen
            # button = Button(text, text=person.name, bg="#222", fg="white", command=lambda personm=personm: person_page(personm, callback))
            button = Button(pages_panel, text=person.name, bg="#222", fg="white", command=lambda personm=personm: person_page(personm))
            # Make the button big
            button.config(font=("Courier", 44))
            # Put the button inside a canvas
            
            text.window_create("end", window=button)
            text.insert("end", "\n")
            
        # Make buttons inside text scrollable
        # text.bind("<Configure>", lambda event: text.configure(scrollregion=text.bbox("all")))
        






        text.configure(state="disabled")
        # Make the text fill the rest of the space
        text.pack(side="top", fill="y", expand=True)
        """

    # Create a go back button that executes go_back
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(people_page)

current_personm = None

def person_page(personm = None):
    global callbacks, current_personm
    callbacks.append(person_page)
    if personm:
        current_personm = personm
    else:
        personm = current_personm
    

    person = personm.entity
    clean_up()
    pages_panel.configure(background='#222')
    print("Person clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    if person.contract:
        print(person.contract)

    # Create a label
    myLabel = Label(pages_panel, text=person.name, bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's age
    myLabel = Label(pages_panel, text="Age: " + str(person.age), bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's money
    myLabel = Label(pages_panel, text="Money: " + str(person.money), bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's happiness and hunger
    myLabel = Label(pages_panel, text="Happiness: " + str(person.happiness) + ", Hunger: " + str(person.hungry), bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's items
    for it in person.items:
        myLabel = Label(pages_panel, text=str(it) + ": " + str(person.items[it]), bg="#222", fg="white")
        myLabel.config(font=("Courier", 44))
        myLabel.pack()




    # Print the place the person works in and the money they make
    if person.contract:
        myLabel = Label(pages_panel, text="Works in: " + person.contract.entity1.name + " for " + str(person.contract.money1), bg="#222", fg="white")
    else:
        myLabel = Label(pages_panel, text="Unenployed", bg="#222", fg="white")
    # Make the label big    
    myLabel.config(font=("Courier", 44))
    myLabel.pack()


    # Create a graph
    plot_linear_graph_earnings_expenses(person)

    # Create a button for each business in the city
    for business in person.businesses:
        businessm = business.manager
        myButton = Button(pages_panel, text=business.name, bg="#222", fg="white", command=lambda businessm=businessm: business_page(businessm))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack()

    # Create a go back button that executes go_back
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)

    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(person_page)


def businesses_page(entitym = None):
    global callbacks, current_entitym
    callbacks.append(businesses_page)
    if entitym:
        current_entitym = entitym
    else:
        entitym = current_entitym
    
    entity = entitym.entity
    clean_up()
    pages_panel.configure(background='#222')
    print("Businesses clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="Businesses", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each business if ret_businesses() is not empty
    # select only businesses with manager from businesses = entitym.entity.businesses
    businesses = [business for business in entitym.entity.businesses if business.manager]
    businesses.sort(key=lambda x: x.manager.average_profit, reverse=True)
    aux = []
    for business in businesses:
        if not business.status == "closed":
            aux.append(business)
    businesses = aux
    if businesses:
        if len(businesses) > 0:
            # Create a scrollbar
            create_scroll(businesses, business_page, "business")
        else:
            for business in businesses:
                if not business.manager:
                    continue
                # Create a button for each business with lable business.name and the business as an argument
                # If owner is instance of State turn color to blue
                if is_public(business):
                    myButton = Button(pages_panel, text=business.name, bg="blue", fg="white", command=lambda business=business: business_page(business.manager))
                else:
                    myButton = Button(pages_panel, text=business.name, bg="orange", fg="white", command=lambda businessm=business.manager: business_page(businessm))
                # Make the button big
                myButton.config(font=("Courier", 44))

                myButton.pack()
    
    # Create a back button
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(businesses_page)

def closed_businesses_page(entitym = None):
    global callbacks, current_entitym
    callbacks.append(closed_businesses_page)
    if entitym:
        current_entitym = entitym
    else:
        entitym = current_entitym
    
    entity = entitym.entity
    clean_up()
    print("Businesses clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="Businesses", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each business if ret_businesses() is not empty
    businesses = entitym.entity.closed_businesses
    if businesses:
        if len(businesses) > 0:
            # Create a scrollbar
            create_scroll(businesses, business_page, "business")    
    # Create a back button
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(closed_businesses_page)



current_businessm = None

def business_page(businessm = None):
    # Initial setup
    global callbacks, current_businessm
    callbacks.append(business_page)
    if businessm:
        current_businessm = businessm
    else:
        businessm = current_businessm
    


    # Begin business page
    business = businessm.entity
    clean_up()
    print("Business clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Show total money
    myLabel = Label(pages_panel, text="Total Money: " + str(business.money) + " Productivity: " + str(business.productivity), bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # If public or subsidized show
    if is_public(business):
        if business.subsidized:        
            myLabel = Label(pages_panel, text="Public Subsidized", bg="#222", fg="white")
            myLabel.config(font=("Courier", 44))
            myLabel.pack()
        else:
            myLabel = Label(pages_panel, text="Public", bg="#222", fg="white")
            myLabel.config(font=("Courier", 44))
            myLabel.pack()
        
    else:
        if business.subsidized:
            myLabel = Label(pages_panel, text="Private Subsidized", bg="#222", fg="white")
            myLabel.config(font=("Courier", 44))
            myLabel.pack()
        else:
            myLabel = Label(pages_panel, text="Private", bg="#222", fg="white")
            myLabel.config(font=("Courier", 44))
            myLabel.pack()

    # Show 
    # total_costs
    # expected_earnings
    # expected_one_earning
    # expected_product_price
    #myLabel = Label(pages_panel, text="Total costs: " + str(businessm.total_costs) + " Expected earnings: " + str(businessm.expected_earnings), bg="#222", fg="white")
    #myLabel.config(font=("Courier", 44))
    #myLabel.pack()

    #myLabel = Label(pages_panel, text="Price to be profitable: " + str(businessm.expected_product_price) + "\n Expected earnings per worker: " + str(businessm.expected_one_earning), bg="#222", fg="white")
    #myLabel.config(font=("Courier", 44))
    #myLabel.pack()
    myLabel = Label(pages_panel, text="Profit: " + str(businessm.profit), bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    myLabel = Label(pages_panel, text="Profit usage:\n " +
        "Salaries: "  + str(businessm.salary_money) + "\n "
        "Prices: "    + str(businessm.price_money)            + "\n "
        "Contracts: " + str(businessm.contract_money)         + "\n "
        "Science: "   + str(businessm.science_money)          + "\n "
        "Invest: "    + str(businessm.invest_money)           + "\n "
    , bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    myLabel = Label(pages_panel, text="Min liquidity: " + str(businessm.minimum_liquidity), bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Show the products produced and sold
    myLabel = Label(pages_panel, text="Products produced: " + str(businessm.number_products) + " Products sold: " + str(businessm.number_sold_products), bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()


    # Show the average profit
    if businessm.average_profit >= 0:
        myLabel = Label(pages_panel, text="Average profit " + str(businessm.average_profit), bg="#222", fg="green")
    else:
        myLabel = Label(pages_panel, text="Average profit " + str(businessm.average_profit), bg="#222", fg="red")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()


    # Show the owner
    myLabel = Label(pages_panel, text="Owner: " + business.owner.name, bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Show product name and price
    if business.product in business.items_price:
        myLabel = Label(pages_panel, text="Product: " + business.product + " Price: " + str(business.items_price[business.product]), bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()


    # Create a label
    myLabel = Label(pages_panel, text=business.name, bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a button for workers
    myButton = Button(pages_panel, text="Workers", bg="#222", fg="white", command=lambda businessm=businessm: workers_page(businessm))
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Show a take control button
    if not businessm.manual:
        myButton = Button(pages_panel, text="Take control", bg="#222", fg="white", command=lambda businessm=businessm: set_control(businessm, "business"))
        myButton.config(font=("Courier", 44))
        myButton.pack()
    else:
        myButton = Button(pages_panel, text="Stop control", bg="#222", fg="white", command=lambda businessm=businessm: stop_control_state(businessm))
        myButton.config(font=("Courier", 44))
        myButton.pack()



    # Create a graph
    plot_linear_graph_earnings_expenses(business)
    
    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Create a next turn button that goes to the businesses page with argument current_city
    next_turn_button(business_page)

def workers_page(businessm = None):
    global callbacks, current_businessm
    callbacks.append(workers_page)
    if businessm:
        current_businessm = businessm
    else:
        businessm = current_businessm
    
    business = businessm.entity
    clean_up()
    print("Workers clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="Workers", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a button for each worker
    
    workers = []
    for contract in business.work_contracts:
        worker = contract.entity2
        # workerm = worker.manager
        # myButton = Button(pages_panel, text=worker.name, bg="#222", fg="white", command=lambda workerm=workerm: person_page(workerm))
        # Make the button big
        # myButton.config(font=("Courier", 44))
        # myButton.pack()
        workers.append(worker)

    create_scroll(workers, person_page, "person")

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(workers_page)

current_marketm = None
def market_page(marketm = None):
    global callbacks, current_marketm
    callbacks.append(market_page)
    if marketm:
        current_marketm = marketm
    else:
        marketm = current_marketm
    
    market = marketm.entity
    clean_up()
    print("Market clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="Market", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a graph
    plot_last_average_price_market(market)
    plot_pie_chart_weight_product_economy(marketm)


    # For each product in the market show the price and the amount of the product
    for product in market.database.average_price:
        offer = market.database.last_offer[product]
        demand = market.database.last_demand[product]
        ammount = market.database.previous_ammount[product]
        if offer >= demand:
            if ammount >= demand:
                myLabel = Label(pages_panel, text=product + " Price: " + str(market.database.average_price[product]) + " Amount: " + str(market.database.previous_ammount[product])+ " Offer: " + str(offer) + " Demand: " + str(demand), bg="#222", fg="green")
            else:
                myLabel = Label(pages_panel, text=product + " Price: " + str(market.database.average_price[product]) + " Amount: " + str(market.database.previous_ammount[product])+ " Offer: " + str(offer) + " Demand: " + str(demand), bg="#222", fg="lightblue")
        elif offer > 0:
            myLabel = Label(pages_panel, text=product + " Price: " + str(market.database.average_price[product]) + " Amount: " + str(market.database.previous_ammount[product])+ " Offer: " + str(offer) + " Demand: " + str(demand), bg="#222", fg="orange")
        else:
            myLabel = Label(pages_panel, text=product + " Price: " + str(market.database.average_price[product]) + " Amount: " + str(market.database.previous_ammount[product])+ " Offer: " + str(offer) + " Demand: " + str(demand), bg="#222", fg="red")


        # myLabel = Label(pages_panel, text=product + " Price: " + str(market.database.average_price[product]))
        # Make the label big
        myLabel.config(font=("Courier", 20))
        # Put the label in the window
        myLabel.pack()

    

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(market_page)

current_statem = None
def state_page(statem = None):
    global callbacks, current_statem
    callbacks.append(state_page)
    if statem:
        current_statem = statem
    else:
        statem = current_statem
    
    state = statem.entity
    clean_up()
    print("State clicked")
    # Put the background light grey
    pages_panel.configure(background='#222')

    # Create a label
    myLabel = Label(pages_panel, text="State", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Show state money
    myLabel = Label(pages_panel, text="Money: " + str(state.money), bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 20))
    # Put the label in the window
    myLabel.pack()

    # Create a button of the governor
    if state.governor:
        myButton = Button(pages_panel, text=state.governor.name, bg="#222", fg="white", command=lambda statem=statem: person_page(state.governor.manager))
        myButton.config(font=("Courier", 44))
        myButton.pack()


    # Show all projects with labels
    myLabel = Label(pages_panel, text="Projects", bg="#222", fg="white")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()
    for project in state.projects:
        myLabel = Label(pages_panel, text=project.name + str(project.resources), bg="#222", fg="white")
        myLabel.config(font=("Courier", 20))
        myLabel.pack()
    

    
    # Show all current laws
    myLabel = Label(pages_panel, text="Laws", bg="#222", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()
    for law in statem.current_laws:
        myLabel = Label(pages_panel, text=law + " " + str(statem.current_laws[law]), bg="#222", fg="white")
        myLabel.config(font=("Courier", 20))
        myLabel.pack()

    

    
    

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="#222", fg="white", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Show a take control button
    if not statem.manual:
        myButton = Button(pages_panel, text="Take control", bg="#222", fg="white", command=lambda statem=statem: set_control(statem, "state"))
        myButton.config(font=("Courier", 44))
        myButton.pack()
    else:
        myButton = Button(pages_panel, text="Stop control", bg="#222", fg="white", command=lambda statem=statem: stop_control_state(statem))
        myButton.config(font=("Courier", 44))
        myButton.pack()

    next_turn_button(state_page)


def go_back():
    global callbacks
    if callbacks:
        callbacks.pop()
        callbacks.pop()()

def next_turn_button(function, panel = None):
    global callbacks, current_statem
    if not panel:
        panel = pages_panel

            
    
    # If pressed refresh the page
    myButton = Button(panel, text="Next Turn", bg="green", fg="white", command=lambda function=function: turn(function))
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Pas 10 turns button
    myButton = Button(panel, text="10 Turns", bg="green", fg="white", command=lambda function=function: turn(function,10))
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Pas 20 turns button
    myButton = Button(panel, text="20 Turns", bg="green", fg="white", command=lambda function=function: turn(function,20))
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Pas 100 turns button
    myButton = Button(panel, text="100 Turns", bg="green", fg="white", command=lambda function=function: turn(function,100))
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Get last law
    if current_statem:
        last_law = show_last_law(current_statem)
        if last_law:
            # Print the last law on a red label at the bottom of the screen
            myLabel = Label(panel, text=last_law, bg="red", fg="white")
            myLabel.config(font=("Courier", 44))
            myLabel.pack(side=BOTTOM)

    


def turn(function, time = 1):
    global current_world
    clean_up()
    for i in range(time):
        bus = current_world.cities_managers[0].city.businesses
        for b in bus:
            if b.money > 1000000:
                return
        pass_turn(current_world)
    callbacks.pop()
    function()
    # Control test
    # control(controls_panel)

def clean_up():
    # global controls_panel
    # # Remove all the widgets from the window
    # for widget in pages_panel.winfo_children():
    #     widget.destroy()
    # controls_panel = PanedWindow(main_panel, orient=VERTICAL)
    # # for widget in controls_panel.winfo_children():
    # #     widget.destroy()
    global pages_panel, controls_panel, main_panel
    # Create one horizontal panel to divide pages and control
    for widget in root.winfo_children():
        widget.destroy()
    main_panel = PanedWindow(root, orient=HORIZONTAL)
    main_panel.pack(fill=BOTH, expand=1)
    pages_panel = PanedWindow(main_panel, orient=VERTICAL)
    controls_panel = PanedWindow(main_panel, orient=VERTICAL)
    controls_panel.pack(fill=BOTH, expand=0)
    pages_panel.pack(fill=BOTH, expand=0)
    
    main_panel.add(controls_panel)
    main_panel.add(pages_panel)
    control(controls_panel)


def plot_pie_chart_public_private_bussiness(businesses, panel = None):
    ratio = get_public_private_ratio(businesses)
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a pie chart
    ax.pie(np.array([ratio, 1-ratio]), labels=["Public", "Private"], autopct='%1.1f%%', startangle=90, colors=["red", "yellow"])

    # Create the chart
    chart = FigureCanvasTkAgg(fig, panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)
    

    return chart.get_tk_widget()

def plot_pie_chart_deaths_natural_starvation(city_manager, panel = None):
    ratio = get_deaths_natural_starvation_ratio(city_manager)
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a pie chart
    ax.pie(np.array([ratio, 1-ratio]), labels=["Natural", "Starvation"], autopct='%1.1f%%', startangle=90, colors=["green", "red"])

    # Create the chart
    chart = FigureCanvasTkAgg(fig, panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)

    return chart.get_tk_widget()
    
def plot_pie_chart_weight_product_economy(market_manager, panel = None):
    if panel == None:
        panel = pages_panel
    m = market_manager.market
    names = []
    values = []
    for product in m.database.previous_ammount:
        if product in m.database.previous_ammount and product in m.database.previous_average_price:
            names.append(product)
            v = round(m.database.previous_average_price[product] * m.database.previous_ammount[product],2)
            if v is not np.NaN:
                values.append(v)

    if not values:
        return None
    # If all values are cero return
    if sum(values) == 0:
        return None
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a pie chart
    ax.pie(np.array(values), labels=names, autopct='%1.1f%%', startangle=90)

    # Create the chart
    chart = FigureCanvasTkAgg(fig, panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)

    return chart.get_tk_widget()
    
    #     pie = plt.pie(np.array([ratio, 1-ratio]), labels=["Public", "Private"], colors=["red", "blue"], startangle=90, shadow=True, explode=(0, 0.1), autopct='%1.1f%%')

def plot_pie_chart_pib(city_manager, panel = None):
    products = {}
    for b in city_manager.city.businesses:
        if not b.manager:
            continue
        if b.product in products:
            products[b.product] += b.manager.pib
        else:
            products[b.product] = b.manager.pib
    if not products:
        return None
    
    all_zero = True
    for p in products.values():
        if p != 0:
            all_zero = False
            break
    if all_zero:
        return None
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a pie chart
    ax.pie(np.array(list(products.values())), labels=list(products.keys()), autopct='%1.1f%%', startangle=90)

    # Create the chart
    chart = FigureCanvasTkAgg(fig, panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)

    return chart.get_tk_widget()

def plot_pie_chart_people_status(city_manager, panel = None):
    if not city_manager.city.people:
        return None
    st = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for p in city_manager.city.people:
        st[p.status] += 1
    #st[6] = 0
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a pie chart
    ax.pie(np.array([st[0], st[1], st[2], st[3], st[4], st[5], st[6]]), labels=["Starving", "Poor", "Lower Class", "Middle Class", "Wealthy", "Rich", "Children"], autopct='%1.1f%%', startangle=90)

    # Create the chart
    chart = FigureCanvasTkAgg(fig, panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)

    return chart.get_tk_widget()


def create_scroll(entities, function, extra=None):
    canvas = Canvas(pages_panel, background="#222")
    sb = Scrollbar(pages_panel, orient="vertical", command=canvas.yview)
    sb.pack()
    #pages_panel.grid_rowconfigure(0, weight=1)
    #pages_panel.grid_columnconfigure(0, weight=1)
    canvas.configure(yscrollcommand=sb.set)
    # canvas.grid(row=0, column=0, sticky="nsew")
    #sb.grid(row=0, column=1, sticky="ns")

    size = 43
    i = 0

    for e in entities:
        # if not e.manager:
        #     continue
        manager = e.manager
        if extra == "business":
            font_size = 20
            # Create horizontal panel for each button, production and profitability
            business_panel = PanedWindow(canvas, orient=HORIZONTAL, background="#222")
            # business_panel = Frame(pages_panel)
            # Set minimum size for panel
            
            business_panel.pack(fill=BOTH, expand=1)

            # Create a button for the button
            if is_public(e):
                if e.subsidized:
                    myButton = Button(business_panel, text=e.name, bg="darkblue", fg="white", command=lambda business=e: business_page(business.manager), font=("Helvetica", font_size))
                else:
                    myButton = Button(business_panel, text=e.name, bg="blue", fg="white", command=lambda business=e: business_page(business.manager), font=("Helvetica", font_size))

            else:
                if e.subsidized:
                    myButton = Button(business_panel, text=e.name, bg="darkorange", fg="white", command=lambda businessm=e.manager: business_page(businessm),font=("Helvetica", font_size))
                else:
                    myButton = Button(business_panel, text=e.name, bg="orange", fg="white", command=lambda businessm=e.manager: business_page(businessm),font=("Helvetica", font_size))

            myButton.pack(fill=BOTH, expand=1)


            # Create a label for the production
            label = Label(business_panel, text="Produces: " + str(e.product), font=("Helvetica", font_size), background="#222", fg="white")
            label.pack()
            # Create a label for the profitability
            label = Label(business_panel, text="Total Money: " + str(e.money) + ", Balance: " + str(e.check_balance()) + " Productivity: " + str(e.productivity), font=("Helvetica", font_size), background="#222", fg="white")
            label.pack()

            # Show the average profit
            if manager is not None:
                if manager.average_profit >= 0:
                    myLabel = Label(business_panel, text="Average profit " + str(manager.average_profit), bg="#222", fg="green", font=("Helvetica", font_size))
                else:
                    myLabel = Label(business_panel, text="Average profit " + str(manager.average_profit), bg="#222", fg="red", font=("Helvetica", font_size))
                myLabel.pack()
            
            # pages_panel.add(business_panel)
            business_panel.pack(fill=BOTH, expand=1)
            # Width of windows should be as wide as the screen
            # canvas.create_window(size,(150)*(i+1), window=business_panel, anchor="center",width=pages_panel.winfo_width())
            # canvas.create_window(0, size*(i+2), window=business_panel, anchor="nw",)
            # canvas.create_window(size,(150)*(i+2), window=business_panel, anchor="center",width=pages_panel.winfo_width())

            canvas.create_window(size,(150)*(i+2), window=business_panel, anchor="center")
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            # pages_panel.add(canvas)
            
        elif extra == "person":
            if e.contract:
                if e.contract.money1 > 10000:
                    myButton = Button(canvas, text=e.name + ", Money= " + str(e.money) + ", Status: " + str(e.status) + ", Business: " + str(len(e.businesses)) + ", Age: " + str(e.age),  command=lambda manager=manager: function(manager), fg="white", bg="orange")
                else:
                    myButton = Button(canvas, text=e.name + ", Money= " + str(e.money) + ", Status: " + str(e.status) + ", Business: " + str(len(e.businesses)) + ", Age: " + str(e.age), command=lambda manager=manager: function(manager), fg="white", bg="green")
            elif e.age < 16:
                myButton = Button(canvas, text=e.name + ", Money= " + str(e.money) + ", Status: " + str(e.status) + ", Business: " + str(len(e.businesses)) + ", Age: " + str(e.age), command=lambda manager=manager: function(manager), fg="white", bg="darkgrey")
            else:
                myButton = Button(canvas, text=e.name + ", Money= " + str(e.money) + ", Status: " + str(e.status) + ", Business: " + str(len(e.businesses)) + ", Age: " + str(e.age), command=lambda manager=manager: function(manager), fg="white", bg="darkblue")
            myButton.config(font=("Courier", 20))
            myButton.pack(fill="y")
            canvas.create_window(0, size*(i+1), window=myButton, anchor="nw")
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))


        else:
            myButton = Button(canvas, text=e.name, bg="#222", fg="white", command=lambda manager=manager: function(manager))
            myButton.config(font=("Courier", 20))
            myButton.pack()
            canvas.create_window(0, size*(i+1), window=myButton, anchor="nw")
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        

        i +=1
    
    
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    
    return sb


    canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))




    """
    # Put the figure into a canvas
    canvas = FigureCanvasTkAgg(fig, master=pages_panel)
    # Put the canvas into the window
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    # Show the figure
    canvas.draw()
    """

def plot_linear_graph_earnings_expenses(entity):
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a line graph
    ax.plot(entity.total_sum_money[-20:], label="Earnings")
    ax.plot(entity.total_sub_money[-20:], label="Expenses")
    ax.legend()
    # Make plot fancy
    ax.set_title("Earnings and Expenses")
    ax.set_xlabel("Time")
    ax.set_ylabel("Money")
    ax.grid(True)

    # Create the chart
    chart = FigureCanvasTkAgg(fig, pages_panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)

    return chart.get_tk_widget()

def plot_last_average_price_market(market):
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a line graph
    for good in market.database.last_average_price:
        num = 10
        if len(market.database.last_average_price[good]) < num:
            num = len(market.database.last_average_price[good])
        if num > 0:
            ax.plot(market.database.last_average_price[good][-num:], label=good)
    ax.legend()

    # Make plot fancy
    ax.set_title("Last Average Price")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.grid(True)


    # Create the chart
    chart = FigureCanvasTkAgg(fig, pages_panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)

    return chart.get_tk_widget()

def plot_borns_deaths(city_manager, panel = None):
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a line graph
    ax.plot(city_manager.last_borns, label="Born", color="green")
    ax.plot(city_manager.last_deaths, label="Deaths", color="red")
    ax.legend()

    # Create the chart
    chart = FigureCanvasTkAgg(fig, panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)
    return chart.get_tk_widget()

def plot_average_contract_price(job_market, panel = None):
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a line graph
    if len(job_market.average_contracts_prices) > 50:
        ax.plot(job_market.average_contractor_prices[-50:], label="Average Contract Price", color="red")
        ax.plot(job_market.average_contractee_prices[-50:], label="Average Contractee Price", color="blue")
        ax.plot(job_market.average_contracts_prices[-50:], label="Average Contract Price", color="green")

    else:
        ax.plot(job_market.average_contractor_prices, label="Average Contractor Price", color="red")
        ax.plot(job_market.average_contractee_prices, label="Average Contractee Price", color="blue")
        ax.plot(job_market.average_contracts_prices, label="Average Contract Price", color="green")

        
    ax.legend()
    # Make chart fancy
    ax.set_title("Average Wage")
    ax.set_xlabel("Time")
    ax.set_ylabel("Average Wage")
    ax.grid(True)


    # Create the chart
    chart = FigureCanvasTkAgg(fig, panel)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    # Close the chart
    plt.close(fig)
    return chart.get_tk_widget()

current_control = None
control_type = ""

secondary_control = None
secondary_type = ""

# Controls
"""
from controls.state_control import StateControl
def control_gui(control = None):
    global current_control

    if not control and not current_control:
        return
    if not control:
        control = current_control
    else:
        current_control = control
    
    if control_type == "state":
        control_gui_state(control)
"""

from tkinter import ttk

def control(panel = None):
    global current_control, control_type
    if not current_control:
        return
    if control_type == "state":
        control_state(current_control, panel)
    elif control_type == "business":
        control_business(current_control, panel)

def set_control(control, type):
    global current_control, control_type
    current_control = control
    control_type = type


def stop_control_state(statem):
    global current_control
    current_control = None
    statem.manual = False

def control_state(statem, panel = None):
    global current_control
    
    current_control = statem
    

    # Set manual to true
    statem.manual = True

    # Create an horizontal panel
    if not panel:
        panel = PanedWindow(orient=VERTICAL,background="#222")
        panel.pack(fill=BOTH, expand=True)
    
    # panel.add(panel_sliders)
    industries = ["farm", "mine", "sawmill", "constructor", "chocolate", "housing", "furniture", "science", "pharmacy", "hospital", "goods", "copper mine", "electric central", "oil extractor", "refinery", "engine factory"]
    goods = ["food", "build", "wood", "iron", "chocolate", "house", "furniture", "science", "medicament", "health", "good", "copper", "electricity", "oil", "gas", "engine"]
    sectors = ["farming", "mining", "lumber", "construction", "chocolating", "housing", "furniture", "science", "pharmaceutical", "healthcare", "consumer", "copper", "electricity", "oil", "gas", "engine"]

    # Create a button to add money with a field for the ammount of money
    print_money_panel = PanedWindow(panel, orient=HORIZONTAL)
    print_money_panel.pack()
    money_field = Entry(print_money_panel)
    money_field.config(font=("Courier", 20))
    money_field.pack()
    button = Button(print_money_panel, text="Print money", command=lambda: statem.print_money(int(money_field.get())))
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(print_money_panel)

    # Create a button to change taxes
    taxes_panel = PanedWindow(panel, orient=HORIZONTAL)
    taxes_panel.pack()
    tax_field = Entry(taxes_panel)
    tax_field.config(font=("Courier", 20))
    tax_field.pack()
    button = Button(taxes_panel, text="Business tax", command=lambda: statem.set_business_tax(float(tax_field.get())))
    button.config(font=("Courier", 20))
    button.pack()
    button2 = Button(taxes_panel, text="People tax", command=lambda: statem.set_people_tax(float(tax_field.get())))
    button2.config(font=("Courier", 20))
    button2.pack()
    panel.add(taxes_panel)



    # Create a privatize sector button with a scroll menu for the sector 
    
    privatize_panel = PanedWindow(panel, orient=HORIZONTAL)
    privatize_panel.pack(fill=BOTH, expand=False)
    variable_privatize = StringVar(privatize_panel)
    variable_privatize.set(sectors[0])
    sector_menu = OptionMenu(privatize_panel, variable_privatize, *sectors)
    sector_menu.config(font=("Courier", 20))
    sector_menu.pack(fill=BOTH, expand=False)
    button = Button(privatize_panel, text="Privatize sector", command=lambda: statem.privatize_sector(variable_privatize.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(privatize_panel)

    # Create a nationalize sector button with a scroll menu for the sector
    nationalize_panel = PanedWindow(panel, orient=HORIZONTAL)
    nationalize_panel.pack(fill=BOTH, expand=False)
    variable_nationalize = StringVar(nationalize_panel)
    variable_nationalize.set(sectors[0])
    sector_menu2 = OptionMenu(nationalize_panel, variable_nationalize, *sectors)
    sector_menu2.config(font=("Courier", 20))
    sector_menu2.pack(fill=BOTH, expand=False)
    button = Button(nationalize_panel, text="Nationalize sector", command=lambda: statem.nationalize_sector(variable_nationalize.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(nationalize_panel)

    # Create a button to change the minimum wage
    change_wage_panel = PanedWindow(panel, orient=HORIZONTAL)
    change_wage_panel.pack(fill=BOTH, expand=False)
    wage_field = Entry(change_wage_panel)
    wage_field.config(font=("Courier", 20))
    wage_field.pack(fill=BOTH, expand=False)
    button = Button(change_wage_panel, text="Change minimum wage", command=lambda: statem.set_minimum_wage(float(wage_field.get())))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(change_wage_panel)

    # Create a button to change the minimum price of goods with a scroll menu for the good
    change_price_panel = PanedWindow(orient=HORIZONTAL)
    change_price_panel.pack(fill=BOTH, expand=False)
    price_field = Entry(change_price_panel)
    price_field.config(font=("Courier", 20))
    price_field.pack(fill=BOTH, expand=False)
    price_variable = StringVar(change_price_panel)
    price_variable.set(goods[0])
    good_menu = OptionMenu(change_price_panel, price_variable, *goods)
    good_menu.config(font=("Courier", 20))
    # good_menu = ttk.Combobox(change_price_panel, values=goods)
    good_menu.pack(fill=BOTH, expand=False)
    button = Button(change_price_panel, text="Change minimum price", command=lambda: statem.set_minimum_price(float(price_field.get()),price_variable.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(change_price_panel)

    # Create a button to change the maximum price of goods with a scroll menu for the good
    change_price_panel2 = PanedWindow(panel, orient=HORIZONTAL)
    change_price_panel2.pack(fill=BOTH, expand=False)
    price_field2 = Entry(change_price_panel2)
    price_field2.config(font=("Courier", 20))
    price_field2.config(font=("Courier", 20))
    price_field2.pack(fill=BOTH, expand=False)
    variable0 = StringVar(change_price_panel2)
    variable0.set('Good')
    good_menu2 = OptionMenu(change_price_panel2, variable0, *goods)
    good_menu2.config(font=("Courier", 20))
    good_menu2.pack(fill=BOTH, expand=False)
    button = Button(change_price_panel2, text="Change maximum price", command=lambda: statem.set_maximum_price(float(price_field2.get()),variable0.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(change_price_panel2)

    # Create a button to remove minimum price of a goog with a option menu for the good
    remove_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    remove_price_panel.pack(fill=BOTH, expand=False)
    variable4 = StringVar(remove_price_panel)
    variable4.set('Product')
    product_menu = OptionMenu(remove_price_panel, variable4, *goods)
    product_menu.config(font=("Courier", 20))
    product_menu.pack(fill=BOTH, expand=False)
    button = Button(remove_price_panel, text="Remove minimum price", command=lambda: statem.remove_minimum_price(variable4.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(remove_price_panel)

    # Create a button to remove maximum price of a goog with a option menu for the good
    remove_price_panel2 = PanedWindow(panel, orient=HORIZONTAL)
    remove_price_panel2.pack(fill=BOTH, expand=False)
    variable5 = StringVar(remove_price_panel2)
    variable5.set('Product')
    product_menu2 = OptionMenu(remove_price_panel2, variable5, *goods)
    product_menu2.config(font=("Courier", 20))
    product_menu2.pack(fill=BOTH, expand=False)
    button = Button(remove_price_panel2, text="Remove maximum price", command=lambda: statem.remove_maximum_price(variable5.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(remove_price_panel2)

    # Create a button to set public price of a good with a option menu for the good and a label for the price
    set_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    set_price_panel.pack(fill=BOTH, expand=False)
    variable6 = StringVar(set_price_panel)
    variable6.set('Product')
    product_menu3 = OptionMenu(set_price_panel, variable6, *goods)
    product_menu3.config(font=("Courier", 20))
    product_menu3.pack(fill=BOTH, expand=False)
    price_field3 = Entry(set_price_panel)
    price_field3.config(font=("Courier", 20))
    price_field3.pack(fill=BOTH, expand=False)
    button = Button(set_price_panel, text="Set public price", command=lambda: statem.set_public_price(float(price_field3.get()),variable6.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(set_price_panel)

    # Create a button to remove public price of a good with a option menu for the good
    remove_price_panel3 = PanedWindow(panel, orient=HORIZONTAL)
    remove_price_panel3.pack(fill=BOTH, expand=False)
    variable7 = StringVar(remove_price_panel3)
    variable7.set('Product')
    product_menu4 = OptionMenu(remove_price_panel3, variable7, *goods)
    product_menu4.config(font=("Courier", 20))
    product_menu4.pack(fill=BOTH, expand=False)
    button = Button(remove_price_panel3, text="Remove public price", command=lambda: statem.remove_public_price(variable7.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(remove_price_panel3)
    
    



    # Create a button to create an industry with a option menu for the industry and a option menu for the city
    create_industry_panel = PanedWindow(panel, orient=HORIZONTAL)
    create_industry_panel.pack(fill=BOTH, expand=False)
    variable = StringVar(create_industry_panel)
    variable.set('Industry')
    industry_menu = OptionMenu(create_industry_panel, variable, *industries)
    industry_menu.config(font=("Courier", 20))
    industry_menu.pack(fill=BOTH, expand=False)
    cities = statem.state.cities
    variable2 = StringVar(create_industry_panel)
    variable2.set(cities[0].name)
    city_menu = OptionMenu(create_industry_panel, variable2, *cities)
    city_menu.config(font=("Courier", 20))
    city_menu.pack(fill=BOTH, expand=False)
    button = Button(create_industry_panel, text="Create industry", command=lambda: statem.build_industry(variable.get(),variable2.get()))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(create_industry_panel)

    # Create a button to build infrastructure with a option for the city
    build_infrastructure_panel = PanedWindow(panel, orient=HORIZONTAL)
    build_infrastructure_panel.pack(fill=BOTH, expand=False)
    cities = statem.state.cities
    variable3 = StringVar(build_infrastructure_panel)
    variable3.set(cities[0].name)
    city_menu2 = OptionMenu(build_infrastructure_panel, variable3, *cities)
    city_menu2.config(font=("Courier", 20))
    city_menu2.pack()
    button = Button(build_infrastructure_panel, text="Build infrastructure", command=lambda: statem.build_infrastructure(variable3.get()))
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(build_infrastructure_panel)


    # Create a button to give money aid with a option menu for the status from 0 to 5 and a label for the amount
    status = [0,1,2,3,4,5]
    give_money_aid_panel = PanedWindow(panel, orient=HORIZONTAL)
    give_money_aid_panel.pack(fill=BOTH, expand=False)
    variable4 = StringVar(give_money_aid_panel)
    variable4.set('Status')
    status_menu = OptionMenu(give_money_aid_panel, variable4, *status)
    status_menu.config(font=("Courier", 20))
    status_menu.pack(fill=BOTH, expand=False)
    amount_field = Entry(give_money_aid_panel)
    amount_field.config(font=("Courier", 20))
    amount_field.pack(fill=BOTH, expand=False)
    button = Button(give_money_aid_panel, text="Give money aid", command=lambda: statem.give_money_aid(int(variable4.get()),float(amount_field.get())))
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(give_money_aid_panel)

    # Create a button to nationalize all businesses
    nationalize_all_panel = PanedWindow(panel, orient=HORIZONTAL)
    nationalize_all_panel.pack(fill=BOTH, expand=False)
    button = Button(nationalize_all_panel, text="Nationalize all businesses", command=lambda: statem.nationalize_all(), fg="white", bg="darkblue")
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(nationalize_all_panel)

    # Create a button to privatize all businesses
    privatize_all_panel = PanedWindow(panel, orient=HORIZONTAL)
    privatize_all_panel.pack(fill=BOTH, expand=False)
    button = Button(privatize_all_panel, text="Privatize all businesses", command=lambda: statem.privatize_all(),fg="white", bg="darkorange")
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(privatize_all_panel)

    # Create a button to close all businesses of a sector with a option menu for the sector
    close_all_panel = PanedWindow(panel, orient=HORIZONTAL)
    close_all_panel.pack(fill=BOTH, expand=False)
    variable5 = StringVar(close_all_panel)
    variable5.set('Sector')
    sector_menu = OptionMenu(close_all_panel, variable5, *sectors)
    sector_menu.config(font=("Courier", 20))
    sector_menu.pack(fill=BOTH, expand=False)
    button = Button(close_all_panel, text="Close all businesses", command=lambda: statem.close_all(variable5.get()),fg="white", bg="red")
    button.config(font=("Courier", 20))
    button.pack(fill=BOTH, expand=False)
    panel.add(close_all_panel)


    # If on business page
    if callbacks[-1] == business_page and current_businessm != None:
        businessm = current_businessm
        business = businessm.business
        # If a business is public
        if is_public(business):
            # Create a button to privatize the business
            privatize_panel = PanedWindow(panel, orient=HORIZONTAL)
            privatize_panel.pack(fill=BOTH, expand=False)
            button = Button(privatize_panel, text="Privatize business", command=lambda: statem.privatize(business), fg="white", bg="orange")
            button.config(font=("Courier", 20))
            button.pack(fill=BOTH, expand=False)
            panel.add(privatize_panel)
        else:
            # Create a button to nationalize the business
            nationalize_panel = PanedWindow(panel, orient=HORIZONTAL)
            nationalize_panel.pack(fill=BOTH, expand=False)
            button = Button(nationalize_panel, text="Nationalize business", command=lambda: statem.nationalize(business),fg="white", bg="blue")
            button.config(font=("Courier", 20))
            button.pack(fill=BOTH, expand=False)
            panel.add(nationalize_panel)

        if business.status == "open":
            # Create a button to close the business
            close_business_panel = PanedWindow(panel, orient=HORIZONTAL)
            close_business_panel.pack(fill=BOTH, expand=False)
            button = Button(close_business_panel, text="Close business", command=lambda: businessm.close_business(),fg="white", bg="red")
            button.config(font=("Courier", 20))
            button.pack(fill=BOTH, expand=False)
            panel.add(close_business_panel)

            if not business.subsidized:
                # Create a button to subsidize with a field for ammount
                subsidize_panel = PanedWindow(panel, orient=HORIZONTAL)
                subsidize_panel.pack(fill=BOTH, expand=False)
                ammount_field = Entry(subsidize_panel)
                ammount_field.config(font=("Courier", 20))
                ammount_field.pack(fill=BOTH, expand=False)
                button = Button(subsidize_panel, text="Subsidize", command=lambda: statem.subsidize_business(business, float(ammount_field.get())),fg="white", bg="green")
                button.config(font=("Courier", 20))
                button.pack(fill=BOTH, expand=False)
                panel.add(subsidize_panel)
            else:
                # Create a button to unsubsidize
                unsubsidize_panel = PanedWindow(panel, orient=HORIZONTAL)
                unsubsidize_panel.pack(fill=BOTH, expand=False)
                button = Button(unsubsidize_panel, text="Unsubsidize", command=lambda: statem.unsubsidize_business(business),fg="white", bg="red")
                button.config(font=("Courier", 20))
                button.pack(fill=BOTH, expand=False)
                panel.add(unsubsidize_panel)
        
        else:
            # Create a button to open the business
            open_business_panel = PanedWindow(panel, orient=HORIZONTAL)
            open_business_panel.pack(fill=BOTH, expand=False)
            button = Button(open_business_panel, text="Open business", command=lambda: statem.open_business(business),fg="white", bg="green")
            button.config(font=("Courier", 20))
            button.pack(fill=BOTH, expand=False)
            panel.add(open_business_panel)


        





def control_business(businessm, panel = None):
    global current_control
    
    current_control = businessm
    

    # Set manual to true
    businessm.manual = True

    # Create an horizontal panel
    if not panel:
        panel = PanedWindow(orient=VERTICAL)
        panel.pack(fill=BOTH, expand=True)
    
    industries = ["farm", "mine", "sawmill", "constructor", "chocolate", "housing", "furniture", "science", "pharmacy", "hospital", "goods", "copper mine", "electric central", "oil extractor", "refinery", "engine factory"]
    goods = ["food", "build", "wood", "iron", "chocolate", "house", "furniture", "science", "medicament", "health", "good", "copper", "electricity", "oil", "gas", "engine"]
    sectors = ["farming", "mining", "lumber", "construction", "chocolating", "housing", "furniture", "science", "pharmaceutical", "healthcare", "consumer", "copper", "electricity", "oil", "gas", "engine"]


    # Show business name
    name_label = Label(panel, text=businessm.business.name)
    name_label.config(font=("Courier", 20))
    name_label.pack(fill=BOTH, expand=False)
    panel.add(name_label)

    # Show business money
    money_label = Label(panel, text="Money: " + str(businessm.business.money))
    money_label.config(font=("Courier", 20))
    money_label.pack(fill=BOTH, expand=False)
    panel.add(money_label)


    # Create a button to set sell price of business
    set_sell_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    set_sell_price_panel.pack()
    price_field = Entry(set_sell_price_panel)
    price_field.config(font=("Courier", 20))
    price_field.pack()
    button = Button(set_sell_price_panel, text="Set sell price", command=lambda: businessm.set_sell_price(float(price_field.get())))
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(set_sell_price_panel)

    # Create a button to unset sell price of business
    unset_sell_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    unset_sell_price_panel.pack()
    button = Button(unset_sell_price_panel, text="Unset sell price", command=lambda: businessm.unset_sell_price())
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(unset_sell_price_panel)

    # Create a button to set ammount of workers
    set_workers_panel = PanedWindow(panel, orient=HORIZONTAL)
    set_workers_panel.pack()
    workers_field = Entry(set_workers_panel)
    workers_field.config(font=("Courier", 20))
    workers_field.pack()
    button = Button(set_workers_panel, text="Set workers", command=lambda: businessm.set_ammount_workers(int(workers_field.get())))
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(set_workers_panel)

    # Create a button to unset ammount of workers
    unset_workers_panel = PanedWindow(panel, orient=HORIZONTAL)
    unset_workers_panel.pack()
    button = Button(unset_workers_panel, text="Unset workers", command=lambda: businessm.unset_ammount_workers())
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(unset_workers_panel)

    # Create a button to set contract price
    set_contract_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    set_contract_price_panel.pack()
    price_field_2 = Entry(set_contract_price_panel)
    price_field_2.config(font=("Courier", 20))
    price_field_2.pack()
    button = Button(set_contract_price_panel, text="Set contract price", command=lambda: businessm.set_contract_price(float(price_field_2.get())))
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(set_contract_price_panel)

    # Create a button to unset contract price
    unset_contract_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    unset_contract_price_panel.pack()
    button = Button(unset_contract_price_panel, text="Unset contract price", command=lambda: businessm.unset_contract_price())
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(unset_contract_price_panel)

    # Create a button to set science buy
    set_science_buy_panel = PanedWindow(panel, orient=HORIZONTAL)
    set_science_buy_panel.pack()
    science_buy_field = Entry(set_science_buy_panel)
    science_buy_field.config(font=("Courier", 20))
    science_buy_field.pack()
    button = Button(set_science_buy_panel, text="Set science buy", command=lambda: businessm.set_science_buy(int(science_buy_field.get())))
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(set_science_buy_panel)

    # Create a button to unset science buy
    unset_science_buy_panel = PanedWindow(panel, orient=HORIZONTAL)
    unset_science_buy_panel.pack()
    button = Button(unset_science_buy_panel, text="Unset science buy", command=lambda: businessm.unset_science_buy())
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(unset_science_buy_panel)

    # Create a button to set science price
    set_science_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    set_science_price_panel.pack()
    science_price_field = Entry(set_science_price_panel)
    science_price_field.config(font=("Courier", 20))
    science_price_field.pack()
    button = Button(set_science_price_panel, text="Set science price", command=lambda: businessm.set_science_price(float(science_price_field.get())))
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(set_science_price_panel)

    # Create a button to unset science price
    unset_science_price_panel = PanedWindow(panel, orient=HORIZONTAL)
    unset_science_price_panel.pack()
    button = Button(unset_science_price_panel, text="Unset science price", command=lambda: businessm.unset_science_price())
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(unset_science_price_panel)

    # Create a button to close business
    close_business_panel = PanedWindow(panel, orient=HORIZONTAL)
    close_business_panel.pack()
    button = Button(close_business_panel, text="Close business", command=lambda: businessm.close_business(), fg="white", bg="red")
    button.config(font=("Courier", 20))
    button.pack()
    panel.add(close_business_panel)









main_panel = None
pages_panel = None
controls_panel = None
def first_turn():
    global pages_panel, controls_panel, main_panel
    # Create one horizontal panel to divide pages and control
    # main_panel = PanedWindow(root, orient=HORIZONTAL)
    # main_panel.pack(fill=BOTH, expand=1)
    # pages_panel = PanedWindow(main_panel, orient=VERTICAL)
    # controls_panel = PanedWindow(main_panel, orient=VERTICAL)
    # pages_panel.pack(fill=BOTH, expand=1)
    # controls_panel.pack(fill=BOTH, expand=1)
    clean_up()
    menu_page()
    # Create the main loop
    root.mainloop()



if __name__ == "__main__":
    first_turn()
    