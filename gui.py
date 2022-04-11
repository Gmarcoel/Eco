from tkinter import *
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
    root.configure(background='grey')

    # Create a label
    myLabel = Label(root, text="ECONOMICS", bg="grey", fg="white")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a world button
    myButton = Button(root, text="WORLDS", bg="grey", fg="white", command=worlds_page)
    # Make the button big
    myButton.config(font=("Courier", 44))
    # Put the button in the window
    myButton.pack()

    # Create the main loop
    root.mainloop()

def worlds_page():
    global callbacks
    callbacks.append(worlds_page)
    clean_up()
    print("Worlds clicked")
    # Put the background light grey
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text="WORLDS", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each world if ret_worlds() is not empty
    worlds = ret_worlds()
    if worlds:
        for world in worlds:
            # Create a button for each world with lable world.name and the world as an argument
            myButton = Button(root, text=world.name, bg="lightgrey", fg="black", command=lambda world=world: world_page(world))
            # Make the button big
            myButton.config(font=("Courier", 44))

            myButton.pack()
    
    # Create a back button
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=menu_page)
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
        myButton = Button(root, text=city.name, bg="grey", fg="white", command=lambda city=city_man: city_page(city_man))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack()

    next_turn_button(world_page)
    # Create a back button
    # Create a go back button that executes go_back
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))

current_citym = None

def city_page(citym = None):
    global callbacks
    callbacks.append(city_page)
    global current_world, current_citym
    if citym:
        current_citym = citym
    else:
        citym = current_citym
    world = current_world
    city = citym.city
    clean_up()
    print("City clicked")
    # Put the background light grey
    root.configure(background='lightblue') 

    
    # Create a label
    myLabel = Label(root, text=city.name, bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()
    
    plot_pie_chart_public_private_bussiness(city.businesses)
    
    # Create a button for the businesses
    myButton = Button(root, text="Businesses", bg="lightgrey", fg="black", command=lambda citym=citym: businesses_page(citym))
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Create a button for the people
    myButton = Button(root, text="People", bg="lightgrey", fg="black", command=lambda citym=citym: people_page(citym))
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Create a button for the markets
    for market in city.markets:
        myButton = Button(root, text=market.name, bg="lightgrey", fg="black", command=lambda market=market.manager: market_page(market))
        myButton.config(font=("Courier", 44))
        myButton.pack()
    
    # Create a button for the state
    myButton = Button(root, text="State", bg="lightgrey", fg="black", command=lambda statem=city.state.manager: state_page(statem))
    myButton.config(font=("Courier", 44))
    myButton.pack()


    
    # Create a go back button that executes go_back
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()
    
    next_turn_button(city_page)

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
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text="People", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each person in the city
    # Create a sidebar if there are more than 10 people
    if len(entity.people) > 10:
        # Create a scrollbar
        create_scroll(entity.people, person_page)
        


        """
        # Create a scrollbar
        text = Text(root, height=len(entity.people), width=20)
        text.pack(side="left")

        sb = Scrollbar(root, command=text.yview)
        # Set the scrollbar to scroll through the windows
        sb.pack(side="right", fill="y")
        text.configure(yscrollcommand=sb.set)
        
        ...
        for person in entity.people:
            personm = person.manager
            # Create a button for each person with lable person.name and the person as an argument and a width of 1/5 of the screen
            # button = Button(text, text=person.name, bg="lightgrey", fg="black", command=lambda personm=personm: person_page(personm, callback))
            button = Button(root, text=person.name, bg="lightgrey", fg="black", command=lambda personm=personm: person_page(personm))
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
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text=person.name, bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Print the person's age
    myLabel = Label(root, text="Age: " + str(person.age), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    myLabel.pack()

    # Print the person's money
    myLabel = Label(root, text="Money: " + str(person.money), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    myLabel.pack()




    # Print the place the person works in and the money they make
    if person.contract:
        myLabel = Label(root, text="Works in: " + person.contract.entity1.name + " for " + str(person.contract.money1), bg="lightgrey", fg="black")
    else:
        myLabel = Label(root, text="Unenployed", bg="lightgrey", fg="black")
    # Make the label big    
    myLabel.config(font=("Courier", 44))
    myLabel.pack()


    # Create a graph
    plot_linear_graph_earnings_expenses(person)

    # Create a button for each business in the city
    for business in person.businesses:
        myButton = Button(root, text=business.name, bg="lightgrey", fg="black", command=lambda business=business: business_page(business.manager))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack()

    # Create a go back button that executes go_back
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)

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
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text="Businesses", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()

    # Create a button for each business if ret_businesses() is not empty
    businesses = entitym.entity.businesses
    if businesses:
        for business in businesses:
            # Create a button for each business with lable business.name and the business as an argument
            # If owner is instance of State turn color to blue
            if is_public(business):
                myButton = Button(root, text=business.name, bg="blue", fg="white", command=lambda business=business: business_page(business.manager))
            else:
                myButton = Button(root, text=business.name, bg="orange", fg="white", command=lambda businessm=business.manager: business_page(businessm))
            # Make the button big
            myButton.config(font=("Courier", 44))

            myButton.pack()
    
    # Create a back button
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    root.configure(background='lightgrey')

    # Show total money
    myLabel = Label(root, text="Total Money: " + str(business.money), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Show the owner
    myLabel = Label(root, text="Owner: " + business.owner.name, bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Show product name and price
    if business.product in business.items_price:
        myLabel = Label(root, text="Product: " + business.product + " Price: " + str(business.items_price[business.product]), bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()


    # Create a label
    myLabel = Label(root, text=business.name, bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a button for workers
    myButton = Button(root, text="Workers", bg="lightgrey", fg="black", command=lambda businessm=businessm: workers_page(businessm))
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()



    # Create a graph
    plot_linear_graph_earnings_expenses(business)
    
    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text="Workers", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a button for each worker
    for contract in business.work_contracts:
        worker = contract.entity2
        workerm = worker.manager
        myButton = Button(root, text=worker.name, bg="lightgrey", fg="black", command=lambda workerm=workerm: person_page(workerm))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack()

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text="Market", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a graph
    plot_last_average_price_market(market)

    # For each product in the market show the price and the amount of the product
    for product in market.database.average_price:
        myLabel = Label(root, text=product + " Price: " + str(market.database.average_price[product]) + " Amount: " + str(market.database.previous_ammount[product]), bg="lightgrey", fg="black")
        # myLabel = Label(root, text=product + " Price: " + str(market.database.average_price[product]))
        # Make the label big
        myLabel.config(font=("Courier", 44))
        # Put the label in the window
        myLabel.pack()

    

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
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
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text="State", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()

    # Create a button of the governor
    myButton = Button(root, text=state.governor.name, bg="lightgrey", fg="black", command=lambda statem=statem: person_page(state.governor.manager))
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()


    # Show all projects with labels
    myLabel = Label(root, text="Projects", bg="lightgrey", fg="black")
    myLabel.config(font=("Courier", 44))
    myLabel.pack()
    for project in state.projects:
        myLabel = Label(root, text=project.name + str(project.resources), bg="lightgrey", fg="black")
        myLabel.config(font=("Courier", 20))
        myLabel.pack()
    

    
    # Show all current laws
    myLabel = Label(root, text="Laws", bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))
    # Put the label in the window
    myLabel.pack()
    for law in statem.current_laws:
        myLabel = Label(root, text=law + " " + str(statem.current_laws[law]), bg="lightgrey", fg="black")
        myLabel.config(font=("Courier", 20))
        myLabel.pack()

    

    
    

    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=go_back)
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(state_page)


def go_back():
    global callbacks
    if callbacks:
        callbacks.pop()
        callbacks.pop()()

def next_turn_button(function):
    global callbacks
    
    # If pressed refresh the page
    myButton = Button(root, text="Next Turn", bg="green", fg="white", command=lambda function=function: turn(function))
    myButton.pack(side=BOTTOM)
    # Make the button big
    myButton.config(font=("Courier", 44))
    # Put the button in the window
    myButton.pack()

def turn(function):
    global current_world
    pass_turn(current_world)
    callbacks.pop()
    function()

def clean_up():
    # Remove all the widgets from the window
    for widget in root.winfo_children():
        widget.destroy()


def plot_pie_chart_public_private_bussiness(businesses):
    ratio = get_public_private_ratio(businesses)
    # Create a figure
    fig = plt.figure()
    # Add an ax to the figure
    ax = fig.add_subplot(111)
    # Create a pie chart
    ax.pie(np.array([ratio, 1-ratio]), labels=["Public", "Private"], autopct='%1.1f%%', startangle=90)

    # Create the chart
    chart = FigureCanvasTkAgg(fig, root)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    

    #     pie = plt.pie(np.array([ratio, 1-ratio]), labels=["Public", "Private"], colors=["red", "blue"], startangle=90, shadow=True, explode=(0, 0.1), autopct='%1.1f%%')

def create_scroll(entities, function):
    canvas = Canvas(root)
    sb = Scrollbar(root, orient="vertical", command=canvas.yview)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    canvas.configure(yscrollcommand=sb.set)
    # canvas.grid(row=0, column=0, sticky="nsew")
    # sb.grid(row=0, column=1, sticky="ns")

    size = 80
    i = 0
    for e in entities:
        manager = e.manager
        myButton = Button(canvas, text=e.name, bg="lightgrey", fg="black", command=lambda manager=manager: function(manager))
        myButton.config(font=("Courier", 44))
        myButton.pack()
        canvas.create_window(0, size*i, window=myButton, anchor="nw",)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        i +=1
    
    canvas.pack(side="left", fill="y", expand=True)
    sb.pack(side="left", fill="y")


    canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))




    """
    # Put the figure into a canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
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
    chart = FigureCanvasTkAgg(fig, root)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

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
    chart = FigureCanvasTkAgg(fig, root)
    chart.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    

if __name__ == "__main__":
    menu_page()