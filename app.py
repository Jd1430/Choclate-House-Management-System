from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    initialize_tables,
    add_seasonal_flavor,
    update_ingredient_quantity,
    add_new_ingredient,
    add_customer_suggestion,
    get_seasonal_flavors,
    get_ingredient_inventory,
    get_customer_suggestions
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  #for flash messages

@app.route('/')
def index():
    """Home page."""
    return render_template('base.html')

@app.route('/add_flavor', methods=['GET', 'POST'])
def add_flavor():
    """Add a new seasonal flavor."""
    if request.method == 'POST':
        flavor_name = request.form['flavor_name']
        availability_start = request.form['availability_start']
        availability_end = request.form['availability_end']
        add_seasonal_flavor(flavor_name, availability_start, availability_end)
        flash('Seasonal flavor added successfully!', 'success')
        return redirect(url_for('add_flavor'))
    return render_template('add_flavor.html')

@app.route('/add_ingredient', methods=['GET', 'POST'])
def add_ingredient_view():
    """Add a new ingredient to the inventory."""
    if request.method == 'POST':
        ingredient_name = request.form['ingredient_name']
        quantity = int(request.form['quantity'])
        add_new_ingredient(ingredient_name, quantity)  
        flash('Ingredient added successfully!', 'success')
        return redirect(url_for('view_inventory'))
    return render_template('add_ingredient.html')

@app.route('/update_inventory', methods=['GET', 'POST'])
def update_inventory():
    """Update ingredient quantity in inventory."""
    if request.method == 'POST':
        ingredient_name = request.form['ingredient_name']
        quantity_change = int(request.form['quantity_change'])
        update_ingredient_quantity(ingredient_name, quantity_change)
        flash('Ingredient inventory updated successfully!', 'success')
        return redirect(url_for('view_inventory'))
    return render_template('update_inventory.html')

@app.route('/customer_suggestions', methods=['GET', 'POST'])
def customer_suggestions():
    """Record customer flavor suggestions and allergy concerns."""
    if request.method == 'POST':
        flavor_suggestion = request.form['flavor_suggestion']
        allergy_info = request.form['allergy_info']
        add_customer_suggestion(flavor_suggestion, allergy_info)
        flash('Customer suggestion recorded successfully!', 'success')
        return redirect(url_for('customer_suggestions'))
    return render_template('customer_suggestions.html')

@app.route('/view_flavors')
def view_flavors():
    """View all seasonal flavors."""
    flavors = get_seasonal_flavors()
    return render_template('view_flavors.html', flavors=flavors)

@app.route('/view_inventory')
def view_inventory():
    """View ingredient inventory."""
    ingredients = get_ingredient_inventory()
    return render_template('view_inventory.html', ingredients=ingredients)

@app.route('/view_suggestions')
def view_suggestions():
    """View customer suggestions."""
    suggestions = get_customer_suggestions()
    return render_template('view_suggestions.html', suggestions=suggestions)

if __name__ == '__main__':
    initialize_tables()  # Ensure database tables are created
    app.run(debug=True)
