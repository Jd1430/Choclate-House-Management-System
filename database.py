import sqlite3

# Database file name
DB_NAME = "chocolate_house.db"

# Connect to the SQLite database
def connect_db():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

# Initialize tables
def initialize_tables():
    """Create tables if they don't already exist in the database."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Table for seasonal flavors 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasonal_flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_name TEXT NOT NULL UNIQUE,
        availability_start DATE,
        availability_end DATE
    )
    ''')
    
    # Table for ingredient 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredient_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL UNIQUE,
        quantity INTEGER NOT NULL DEFAULT 0
    )
    ''')
    
    # Table for customer suggestions 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_suggestion TEXT,
        allergy_info TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

#allow to insert items in the sseasonal_flavor table
def add_seasonal_flavor(flavor_name, availability_start, availability_end):
    """Add a new seasonal flavor to the database if it doesn't already exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM seasonal_flavors WHERE flavor_name = ?', (flavor_name,))
        if cursor.fetchone() is None:
            cursor.execute('''
            INSERT INTO seasonal_flavors (flavor_name, availability_start, availability_end)
            VALUES (?, ?, ?)
            ''', (flavor_name, availability_start, availability_end))
            conn.commit()
            print(f"Flavor '{flavor_name}' added.")
        else:
            print(f"Flavor '{flavor_name}' already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        

#allow to insert items in the ingredient_inventoryr table
def add_new_ingredient(ingredient_name, quantity):
    """Add a new ingredient to the inventory if it doesn't already exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM ingredient_inventory WHERE ingredient_name = ?', (ingredient_name,))
        if cursor.fetchone() is None:
            cursor.execute('''
            INSERT INTO ingredient_inventory (ingredient_name, quantity)
            VALUES (?, ?)
            ''', (ingredient_name, quantity))
            conn.commit()
            print(f"Ingredient '{ingredient_name}' added with quantity {quantity}.")
        else:
            print(f"Ingredient '{ingredient_name}' already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()



#we can Upgrade the quantity of item if it is changed
def update_ingredient_quantity(ingredient_name, quantity_change):
    """Update the quantity of an existing ingredient."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Check if the ingredient exists
        cursor.execute('SELECT quantity FROM ingredient_inventory WHERE ingredient_name = ?', (ingredient_name,))
        result = cursor.fetchone()
        
        if result is not None:
            # Update the quantity
            new_quantity = result[0] + quantity_change
            cursor.execute('''
            UPDATE ingredient_inventory
            SET quantity = ?
            WHERE ingredient_name = ?
            ''', (new_quantity, ingredient_name))
            conn.commit()
            print(f"Ingredient '{ingredient_name}' quantity updated by {quantity_change}. New quantity: {new_quantity}.")
        else:
            print(f"Ingredient '{ingredient_name}' does not exist in the inventory.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# allow to add a customer suggestion
def add_customer_suggestion(flavor_suggestion, allergy_info):
    """Record a customer flavor suggestion and allergy concerns."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO customer_suggestions (flavor_suggestion, allergy_info)
        VALUES (?, ?)
        ''', (flavor_suggestion, allergy_info))
        conn.commit()
        print(f"Customer suggestion '{flavor_suggestion}' added.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Retrieve seasonal flavors
def get_seasonal_flavors():
    """Retrieve all seasonal flavors from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM seasonal_flavors')
        flavors = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        flavors = []
    finally:
        conn.close()
    return flavors

# Retrieve ingredient inventory
# Function to retrieve all ingredients
def get_ingredient_inventory():
    """Retrieve the ingredient inventory, reflecting both additions and updates."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM ingredient_inventory')
        ingredients = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        ingredients = []
    finally:
        conn.close()
    return ingredients

# Retrieve customer suggestions
def get_customer_suggestions():
    """Retrieve all customer suggestions and allergy concerns."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM customer_suggestions')
        suggestions = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        suggestions = []
    finally:
        conn.close()
    return suggestions

# Test block to verify functionality
if __name__ == "__main__":
    # Initialize tables
    initialize_tables()
    
    #adding data
    add_seasonal_flavor("Cherry Cola Pop", "2024-07-01", "2024-08-01")
    add_seasonal_flavor("Pumpkin Spice", "2024-10-01", "2024-12-01")
    add_seasonal_flavor("Peppermint Snowfall", "2024-12-01", "2025-01-31")


    # Test adding and updating ingredients
    add_new_ingredient("Cocoa", 100)          # Add new ingredient
    add_new_ingredient("Vanilla", 200)        # Add new ingredient

    

    add_customer_suggestion("Cherry Cola Pop", "Consider using natural cherry flavor")
    add_customer_suggestion("Maple Pecan", "Nut allergy")
    add_customer_suggestion("Peppermint Snowfall", "Prefer reduced sugar")
    
    # Retrieve and print data to verify
    #retrieving data
    print("Seasonal Flavors:", get_seasonal_flavors())
    print("Ingredient Inventory:", get_ingredient_inventory())
    print("Customer Suggestions:", get_customer_suggestions())
    
