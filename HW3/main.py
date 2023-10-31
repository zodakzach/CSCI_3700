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
        sql_insert = "INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');"
        success = util.run_and_fetch_sql(cursor, sql_insert)

        #Commits change to database
        connection.commit()
        
        # Disconnect from the database
        util.disconnect_from_db(connection, cursor)
        
        if success:
            return "Success!"  # Return success message
        else:
            return "Error from PostgreSQL"  # Return error message
        
@app.route('/api/unique', methods=['GET'])
def unique_fruits():
    try:
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)
        
        # Query for unique fruits in basket_a
        query_a = "SELECT DISTINCT fruit_a FROM basket_a;"
        cursor.execute(query_a)
        unique_fruits_a = [row[0] for row in cursor.fetchall()]
        
        # Query for unique fruits in basket_b
        query_b = "SELECT DISTINCT fruit_b FROM basket_b;"
        cursor.execute(query_b)
        unique_fruits_b = [row[0] for row in cursor.fetchall()]
        
        # Disconnect from the database
        util.disconnect_from_db(connection, cursor)
        
        # Create an HTML table to display unique fruits
        html_table = """
          <style>
                table {
                    width: 100%;
                    border-collapse: collapse; /* Collapse the borders */
                }
                th, td {
                    padding: 10px; /* Add padding to cells for spacing */
                    border-left: 1px solid #000; /* Add a left border to separate columns */
                }
                th:first-child,
                td:first-child {
                    border-left: none; /* Remove the left border for the first column */
                }
            </style>

            <table>
                <tr>
                    <th>Unique Fruits in Basket A</th>
                    <th>Unique Fruits in Basket B</th>
                </tr>
            """
        # Determine the maximum number of rows in both lists
        max_rows = max(len(unique_fruits_a), len(unique_fruits_b))
        
        for i in range(max_rows):
            html_table += "<tr>"
            # Display unique fruits in basket_a
            if i < len(unique_fruits_a):
                html_table += f"<td>{unique_fruits_a[i]}</td>"
            else:
                html_table += "<td></td>"
            # Display unique fruits in basket_b
            if i < len(unique_fruits_b):
                html_table += f"<td>{unique_fruits_b[i]}</td>"
            else:
                html_table += "<td></td>"
            html_table += "</tr>"
        
        html_table += "</table>"
        return html_table
    except Exception as e:
        return f"Error: {e}"


if __name__ == '__main__':
	# set debug mode
    app.debug = True
    # your local machine ip
    ip = '127.0.0.1'
    app.run(host=ip)
