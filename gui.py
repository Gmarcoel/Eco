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
    pages_panel.configure(background='grey')

    # Create a label
    myLabel = Label(pages_panel, text="ECONOMICS", bg="grey", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a world button
    myButton = Button(pages_panel, text="WORLDS", bg="grey", fg="white", command=worlds_page)
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
    pages_panel.configure(background='lightgrey')

    # Create a label
    myLabel = Label(pages_panel, text="WORLDS", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each world if ret_worlds() is not empty
    worlds = ret_worlds()
    if worlds:
        for world in worlds:
            # Create a button for each world with lable world.name and the world as an argument
            myButton = Button(pages_panel, text=world.name, bg="lightgrey", fg="black", command=lambda world=world: world_page(world))
            # Make the button big
            myButton.config(font=("Courier", 44))

            myButton.pack()
    
    # Create a back button
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=menu_page)
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
    # Create a button for each city in the world
    for city_man in world.cities_managers:
        city = city_man.city
        myButton = Button(pages_panel, text=city.name, bg="grey", fg="white", command=lambda city=city_man: city_page(city_man))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack(expand=True)

    next_turn_button(world_page, pages_panel)
    # Create a back button
    # Create a go back button that executes go_back
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    pages_panel.configure(background='lightblue') 

    # Create a panel for the city
    buttons_panel = PanedWindow(pages_panel, orient=VERTICAL)
    buttons_panel.pack(fill=BOTH, expand=True)
    
    # Create a label
    myLabel = Label(buttons_panel, text=city.name, bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 44))
    myLabel.pack(expand=True)

    # Show infrastructure
    myLabel = Label(buttons_panel, text="Infrastructure " + str(city.infrastructure), bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 20))
    myLabel.pack(expand=True)


    # Show population and deaths
    myLabel = Label(buttons_panel, text="Population " + str(len(city.people)), bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 20))
    myLabel.pack(expand=True)
    # Show deaths
    myLabel = Label(buttons_panel, text="Deaths " + str(citym.deaths), bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 20))
    myLabel.pack(expand=True)


    
    # Create a button for the businesses
    myButton = Button(buttons_panel, text="Businesses", bg="lightgrey", fg="black", command=lambda citym=citym: businesses_page(citym))
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)

    # Create a button for the people
    myButton = Button(buttons_panel, text="People", bg="lightgrey", fg="black", command=lambda citym=citym: people_page(citym))
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)

    # Create a button for the markets
    for market in city.markets:
        myButton = Button(buttons_panel, text=market.name, bg="lightgrey", fg="black", command=lambda market=market.manager: market_page(market))
        myButton.config(font=("Courier", 20))
        myButton.pack(expand=True)
    
    # Create a button for the state
    myButton = Button(buttons_panel, text="State", bg="lightgrey", fg="black", command=lambda statem=city.state.manager: state_page(statem))
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)


    
    # Create a go back button that executes go_back
    myButton = Button(buttons_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
    myButton.config(font=("Courier", 20))
    myButton.pack(expand=True)
    
    # Next turn button
    next_turn_button(city_page,buttons_panel)

    # Create horizontal panel for graphics
    graphics_panel = PanedWindow(pages_panel, orient=HORIZONTAL)
    graphics_panel.pack(fill=BOTH, expand=True)

    # Create a vertical panel for charts
    charts_panel = PanedWindow(graphics_panel, orient=VERTICAL)
    charts_panel.pack(fill=BOTH, expand=True)
    graphics_panel.add(charts_panel)




    chart = plot_pie_chart_public_private_bussiness(city.businesses, charts_panel)
    charts_panel.add(chart)
    chart = plot_pie_chart_deaths_natural_starvation(citym, charts_panel)
    charts_panel.add(chart)
    chart = plot_borns_deaths(citym, graphics_panel)
    graphics_panel.add(chart)



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
    print("People clicked")
    # Put the background light grey
    pages_panel.configure(background='lightgrey')

    # Create a label
    myLabel = Label(pages_panel, text="People", bg="lightgrey", fg="black")
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
            # button = Button(text, text=person.name, bg="lightgrey", fg="black", command=lambda personm=personm: person_page(personm, callback))
            button = Button(pages_panel, text=person.name, bg="lightgrey", fg="black", command=lambda personm=personm: person_page(personm))
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
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    print("Person clicked")
    # Put the background light grey
    pages_panel.configure(background='lightgrey')

    # Create a label
    myLabel = Label(pages_panel, text=person.name, bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's age
    myLabel = Label(pages_panel, text="Age: " + str(person.age), bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's money
    myLabel = Label(pages_panel, text="Money: " + str(person.money), bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's happiness and hunger
    myLabel = Label(pages_panel, text="Happiness: " + str(person.happiness) + ", Hunger: " + str(person.hungry), bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's items
    for it in person.items:
        myLabel = Label(pages_panel, text=str(it) + ": " + str(person.items[it]), bg="lightgrey", fg="black")
        myLabel.config(font=("Courier", 44))
        myLabel.pack()




    # Print the place the person works in and the money they make
    if person.contract:
        myLabel = Label(pages_panel, text="Works in: " + person.contract.entity1.name + " for " + str(person.contract.money1), bg="lightgrey", fg="black")
    else:
        myLabel = Label(pages_panel, text="Unenployed", bg="lightgrey", fg="black")
    # Make the label big    
    myLabel.config(font=("Courier", 44))
    myLabel.pack()


    # Create a graph
    plot_linear_graph_earnings_expenses(person)

    # Create a button for each business in the city
    for business in person.businesses:
        businessm = business.manager
        myButton = Button(pages_panel, text=business.name, bg="lightgrey", fg="black", command=lambda businessm=businessm: business_page(businessm))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack()

    # Create a go back button that executes go_back
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)

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
    print("Businesses clicked")
    # Put the background light grey
    pages_panel.configure(background='lightgrey')

    # Create a label
    myLabel = Label(pages_panel, text="Businesses", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each business if ret_businesses() is not empty
    businesses = entitym.entity.businesses
    aux = []
    for business in businesses:
        if not business.status == "closed":
            aux.append(business)
    businesses = aux
    if businesses:
        if len(businesses) > 1:
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
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(businesses_page)

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
    pages_panel.configure(background='lightgrey')

    # Show total money
    myLabel = Label(pages_panel, text="Total Money: " + str(business.money) + " Productivity: " + str(business.productivity), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Show 
    # total_costs
    # expected_earnings
    # expected_one_earning
    # expected_product_price
    myLabel = Label(pages_panel, text="Total costs: " + str(businessm.total_costs) + " Expected earnings: " + str(businessm.expected_earnings), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()
    myLabel = Label(pages_panel, text="Minimum product price to be profitable: " + str(businessm.expected_product_price) + "\n Expected earnings per worker: " + str(businessm.expected_one_earning), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()


    # Show the owner
    myLabel = Label(pages_panel, text="Owner: " + business.owner.name, bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Show product name and price
    if business.product in business.items_price:
        myLabel = Label(pages_panel, text="Product: " + business.product + " Price: " + str(business.items_price[business.product]), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()


    # Create a label
    myLabel = Label(pages_panel, text=business.name, bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a button for workers
    myButton = Button(pages_panel, text="Workers", bg="lightgrey", fg="black", command=lambda businessm=businessm: workers_page(businessm))
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()



    # Create a graph
    plot_linear_graph_earnings_expenses(business)
    
    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    pages_panel.configure(background='lightgrey')

    # Create a label
    myLabel = Label(pages_panel, text="Workers", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a button for each worker
    
    workers = []
    for contract in business.work_contracts:
        worker = contract.entity2
        # workerm = worker.manager
        # myButton = Button(pages_panel, text=worker.name, bg="lightgrey", fg="black", command=lambda workerm=workerm: person_page(workerm))
        # Make the button big
        # myButton.config(font=("Courier", 44))
        # myButton.pack()
        workers.append(worker)

    create_scroll(workers, person_page, "person")

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    pages_panel.configure(background='lightgrey')

    # Create a label
    myLabel = Label(pages_panel, text="Market", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a graph
    plot_last_average_price_market(market)
    plot_pie_chart_weight_product_economy(marketm)


    # For each product in the market show the price and the amount of the product
    for product in market.database.average_price:
        myLabel = Label(pages_panel, text=product + " Price: " + str(market.database.average_price[product]) + " Amount: " + str(market.database.previous_ammount[product]), bg="lightgrey", fg="black")
        # myLabel = Label(pages_panel, text=product + " Price: " + str(market.database.average_price[product]))
        # Make the label big
        myLabel.config(font=("Courier", 44))
        # Put the label in the window
        myLabel.pack()

    

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    pages_panel.configure(background='lightgrey')

    # Create a label
    myLabel = Label(pages_panel, text="State", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Show state money
    myLabel = Label(pages_panel, text="Money: " + str(state.money), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 20))
    # Put the label in the window
    myLabel.pack()

    # Create a button of the governor
    if state.governor:
        myButton = Button(pages_panel, text=state.governor.name, bg="lightgrey", fg="black", command=lambda statem=statem: person_page(state.governor.manager))
        myButton.config(font=("Courier", 44))
        myButton.pack()


    # Show all projects with labels
    myLabel = Label(pages_panel, text="Projects", bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()
    for project in state.projects:
        myLabel = Label(pages_panel, text=project.name + str(project.resources), bg="lightgrey", fg="black")
        myLabel.config(font=("Courier", 20))
        myLabel.pack()
    

    
    # Show all current laws
    myLabel = Label(pages_panel, text="Laws", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()
    for law in statem.current_laws:
        myLabel = Label(pages_panel, text=law + " " + str(statem.current_laws[law]), bg="lightgrey", fg="black")
        myLabel.config(font=("Courier", 20))
        myLabel.pack()

    

    
    

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(pages_panel, text="Back", bg="lightgrey", fg="black", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Show a take control button
    if not statem.manual:
        myButton = Button(pages_panel, text="Take control", bg="lightgrey", fg="black", command=lambda statem=statem: set_control(statem, "state"))
        myButton.config(font=("Courier", 44))
        myButton.pack()
    else:
        myButton = Button(pages_panel, text="Stop control", bg="lightgrey", fg="black", command=lambda statem=statem: stop_control_state(statem))
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
    ax.pie(np.array([ratio, 1-ratio]), labels=["Public", "Private"], autopct='%1.1f%%', startangle=90)

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

def create_scroll(entities, function, extra=None):
    canvas = Canvas(pages_panel)
    sb = Scrollbar(pages_panel, orient="vertical", command=canvas.yview)

    pages_panel.grid_rowconfigure(0, weight=1)
    pages_panel.grid_columnconfigure(0, weight=1)
    canvas.configure(yscrollcommand=sb.set)
    # canvas.grid(row=0, column=0, sticky="nsew")
    # sb.grid(row=0, column=1, sticky="ns")

    size = 43
    i = 0
    for e in entities:
        # if not e.manager:
        #     continue
        manager = e.manager
        if extra == "businesse":
            business_panel = PanedWindow(pages_panel,orient=HORIZONTAL)
            business_panel.pack(fill=BOTH, expand=False)
            if is_public(e):
                myButton = Button(business_panel, text=e.name, bg="blue", fg="white", command=lambda business=e: business_page(business.manager))
            else:
                myButton = Button(business_panel, text=e.name, bg="orange", fg="white", command=lambda businessm=e.manager: business_page(businessm))
            myButton.config(font=("Courier", 20))
            myButton.pack()
            myLabel = Label(business_panel, bg="Brown", fg="white", text="Produces: " + str(e.product))
            myLabel.config(font=("Courier", 10))
            myLabel.pack()
            if e.check_balance():
                myLabel = Label(business_panel, bg="green", fg="white", text="Total Money: " + str(e.money) + ", Balance: " + str(e.balance[-1]) + " Productivity: " + str(e.productivity))
            else:
                myLabel = Label(business_panel, bg="red", fg="white", text="Total Money: " + str(e.money) + ", Balance: " + str(e.balance[-1]) + " Productivity: " + str(e.productivity))
            myLabel.config(font=("Courier", 10))
            myLabel.pack()
            """
            pages_panel.add(business_panel)

            canvas.create_window(0, size*i, window=business_panel, anchor="nw",)
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            """
        elif extra == "person":
            myButton = Button(canvas, text=e.name + ", Money= " + str(e.money) + ", Status: " + str(e.status) + ", Business: " + str(len(e.businesses)), bg="lightgrey", fg="black", command=lambda manager=manager: function(manager))
            myButton.config(font=("Courier", 20))
            myButton.pack()
            canvas.create_window(0, size*i, window=myButton, anchor="nw",)
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))


        else:
            myButton = Button(canvas, text=e.name, bg="lightgrey", fg="black", command=lambda manager=manager: function(manager))
            myButton.config(font=("Courier", 20))
            myButton.pack()
            canvas.create_window(0, size*i, window=myButton, anchor="nw",)
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
    ax.plot(entity.total_sum_money, label="Earnings")
    ax.plot(entity.total_sub_money, label="Expenses")
    ax.legend()

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
        ax.plot(market.database.last_average_price[good], label=good)
    ax.legend()

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

current_control = None
control_type = ""

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
        panel = PanedWindow(orient=VERTICAL)
        panel.pack(fill=BOTH, expand=True)
    


    # Create an horizontal panel for sliders
    # panel_sliders = PanedWindow(orient=HORIZONTAL)
    # panel_sliders.pack(fill=BOTH, expand=True)

    # Create a check button of manual 
    # man = IntVar(statem.manual)
    # Set man value to statem.manual value

    # manual_control = Checkbutton(panel_sliders, text="Manual control", onvalue=True, offvalue=False, indicatoron=True, function=statem.set_manual())
    # statem.manual = man.get()
    # manual_control = Checkbutton(panel_sliders,text="Manual control", onvalue=True, offvalue=False, variable=man, function=change_man(statem, man.get()))
    # manual_control.pack(side=LEFT)

    # Create a check button of basics manual control
    # bas = IntVar()
    # Set bas value to statem.basics_manual value
    # bas.initialize(statem.basics_manual)
    # basics_manual_control = Checkbutton(panel_sliders, text="Basics manual control", onvalue=True, offvalue=False, indicatoron=True, function= statem.set_basics_manual())
    # statem.basics_manual = bas.get()

    # basics_manual_control.pack(side=RIGHT)


    # panel.add(panel_sliders)
    industries = ["farm", "mine", "sawmill", "constructor", "chocolate", "housing", "furniture", "science"]
    goods = ["food", "build", "wood", "stone", "chocolate", "house", "furniture", "science"]
    sectors = ["farming", "mining", "lumber", "construction", "chocolating", "housing", "furniture", "science"]

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
    button = Button(taxes_panel, text="Business tax", command=lambda: statem.set_business_tax(int(tax_field.get())))
    button.config(font=("Courier", 20))
    button.pack()
    button2 = Button(taxes_panel, text="Business tax", command=lambda: statem.set_people_tax(int(tax_field.get())))
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


    # Create a button to create an industry with a option menu for the industry and a option meny for the city
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

    # print(controls_panel.winfo_children())
    # for widget in controls_panel.winfo_children():
    #     widget.destroy()
    # print(controls_panel.winfo_children())
    # print("MAMA")


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
    