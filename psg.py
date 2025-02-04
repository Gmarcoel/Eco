from flask import Flask, render_template, jsonify, request
from loop import *  # Import your simulation logic
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Global variables to keep track of current state
current_world = None
current_citym = None
current_entitym = None
current_personm = None
current_businessm = None
current_marketm = None
current_statem = None

@app.route('/')
def menu_page():
    return render_template('menu.html')

@app.route('/worlds')
def worlds_page():
    worlds = ret_worlds()
    return render_template('worlds.html', worlds=worlds)

@app.route('/world/<int:world_id>')
def world_page(world_id):
    global current_world
    current_world = ret_worlds()[world_id]
    return render_template('world.html', world=current_world)

@app.route('/city/<int:city_id>')
def city_page(city_id):
    global current_citym
    current_citym = current_world.cities_managers[city_id]
    city = current_citym.city
    
    # Generate charts
    charts = generate_city_charts(current_citym)
    
    return render_template('city.html', city=city, charts=charts)

# Add more routes for other pages...

@app.route('/next_turn', methods=['POST'])
def next_turn():
    turns = int(request.form.get('turns', 1))
    for _ in range(turns):
        # Implement your turn logic here
        pass
    return jsonify({'success': True})

def generate_city_charts(citym):
    charts = {}
    
    # Generate each chart and convert to base64 string
    # Example for one chart:
    plt.figure()
    plot_pie_chart_public_private_bussiness(citym.city.businesses)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts['public_private'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # Repeat for other charts...
    
    return charts

if __name__ == '__main__':
    app.run(debug=True)