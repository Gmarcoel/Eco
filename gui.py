from tkinter import *
from loop import *
import matplotlib.pyplot as plt
from matplotlib import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a GUI
root = Tk()

def menu_page():
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

def world_page(world):
    global current_world
    current_world = world
    clean_up()
    # Create a button for each city in the world
    for city_man in world.cities_managers:
        city = city_man.city
        myButton = Button(root, text=city.name, bg="grey", fg="white", command=lambda city=city_man: city_page(city_man))
        # Make the button big
        myButton.config(font=("Courier", 44))
        myButton.pack()

    next_turn_button(world, world_page, world)
    # Create a back button
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=worlds_page)
    # Make the button big
    myButton.config(font=("Courier", 44))

current_citym = None

def city_page(citym):
    global current_world, current_citym
    current_citym = citym
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
    myButton = Button(root, text="Businesses", bg="lightgrey", fg="black", command=lambda citym=citym: businesses_page(citym, city_page))
    myButton.config(font=("Courier", 44))
    myButton.pack()
    
    # Create a back button that goes to the world page with argument current_world
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=lambda world=current_world: world_page(world))
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()
    
    next_turn_button(current_world, city_page, citym)
    

def businesses_page(entitym, callback = city_page):
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
            myButton = Button(root, text=business.name, bg="lightgrey", fg="black", command=lambda businessm=business.manager: business_page(businessm, callback))
            # Make the button big
            myButton.config(font=("Courier", 44))

            myButton.pack()
    
    # Create a back button
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=lambda entitym=entitym: callback(entitym))
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    next_turn_button(current_world, businesses_page, entitym, city_page)

def business_page(businessm, callback):
    business = businessm.entity
    clean_up()
    print("Business clicked")
    # Put the background light grey
    root.configure(background='lightgrey')

    # Create a label
    myLabel = Label(root, text=business.name, bg="lightgrey", fg="black")
    # Make the label big
    myLabel.config(font=("Courier", 44))

    # Put the label in the window
    myLabel.pack()
    
    # Create a back button that goes to the businesses page with argument current_city
    myButton = Button(root, text="Back", bg="lightgrey", fg="black", command=lambda entitym=current_citym: businesses_page(entitym, callback))
    # Make the button big
    myButton.config(font=("Courier", 44))
    myButton.pack()

    # Create a next turn button that goes to the businesses page with argument current_city
    next_turn_button(current_world, business_page, businessm, businesses_page)


def next_turn_button(world, callback, entitym, extra = None):
    # Create a green square button at the bottom of the screen
    # If pressed refresh the page
    myButton = Button(root, text="Next Turn", bg="green", fg="white", command=lambda world=world: turn(world, callback, entitym, extra))
    myButton.pack(side=BOTTOM)
    # Make the button big
    myButton.config(font=("Courier", 44))
    # Put the button in the window
    myButton.pack()

def turn(world, callback, entitym, extra = None):
    pass_turn(world)
    if extra:
        callback(entitym,extra)
    else:
        callback(entitym)
    

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



    """
    # Put the figure into a canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    # Put the canvas into the window
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    # Show the figure
    canvas.draw()
    """


    

if __name__ == "__main__":
    menu_page()