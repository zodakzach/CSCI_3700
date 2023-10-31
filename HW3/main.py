from flask import request, Flask
import util

# create an application instance
# all requests it receives from clients to this object for handling
# we are instantiating a Flask object by passing __name__ argument to the Flask constructor. 
# The Flask constructor has one required argument which is the name of the application package. 
# Most of the time __name__ is the correct value. The name of the application package is used 
# by Flask to find static assets, templates and so on.
app = Flask(__name__)

# evil global variables
# can be placed in a config file
# here is a possible tutorial how you can do this
username='zacharycervenka'
password='test'
host='127.0.0.1'
port='5432'
database='dvdrental'

@app.route('/api/update_basket_a', methods=['GET'])
def update_basket_a():
    # Check if the request is a GET request
    if request.method == 'GET':
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)
        
        # Insert a new row into basket_a
        sql_insert = "INSERT INTO basket_a VALUES (5, 'Cherry');"
        success = util.run_and_fetch_sql(cursor, sql_insert)
        
        # Disconnect from the database
        util.disconnect_from_db(connection, cursor)
        
        if success:
            return "Success!"  # Return success message
        else:
            return "Error from PostgreSQL"  # Return error message
        
@app.route('/api/unique', methods=['GET'])
def unique_fruits():
    # Connect to the database
    cursor, connection = util.connect_to_db(username, password, host, port, database)
    
    # Query for unique fruits in basket_a and basket_b
    sql_query = """
    SELECT DISTINCT fruit_a FROM basket_a
    UNION
    SELECT DISTINCT fruit_b FROM basket_b;
    """
    records = util.run_and_fetch_sql(cursor, sql_query)
    
    # Disconnect from the database
    util.disconnect_from_db(connection, cursor)
    
    if records == -1:
        return "Error from PostgreSQL"  # Return error message
    else:
        # Create an HTML table to display unique fruits
        html_table = "<table><tr><th>Unique Fruits</th></tr>"
        for record in records:
            html_table += f"<tr><td>{record[0]}</td></tr>"
        html_table += "</table>"
        return html_table

if __name__ == '__main__':
	# set debug mode
    app.debug = True
    # your local machine ip
    ip = '127.0.0.1'
    app.run(host=ip)