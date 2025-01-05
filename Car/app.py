import requests
from flask import Flask, request, render_template
import pandas as pd
import os
from dotenv import load_dotenv  # Import the library to load environment variables

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Get the API key from the environment variable
API_KEY = os.getenv('API_KEY')

# Function to fetch car data from the API
def fetch_car_data(make, model, year):
    """
    Fetches car data from the API based on make, model, and year.

    Parameters:
        make (str): Car make
        model (str): Car model
        year (str): Car year

    Returns:
        dict: JSON response from the API containing car details, or None if an error occurs.
    """
    url = f"https://api.api-ninjas.com/v1/cars?make={make}&model={model}&year={year}"
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    if response.status_code != 200:  # Check if the API request was successful
        return None
    return response.json()  # Return the JSON response

# Function to convert car data into a Pandas DataFrame
def create_dataframe(car_data):
    """
    Converts car data into a Pandas DataFrame for easier display.

    Parameters:
        car_data (list): List of dictionaries containing car details

    Returns:
        pd.DataFrame: A DataFrame representation of the car data
    """
    if not car_data:  # Check if car data is empty or None
        return pd.DataFrame()  # Return an empty DataFrame
    df = pd.DataFrame(car_data)
    return df

# Route for the main page (index)
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page where users can fetch car information based on make, model, and year.

    If the request method is POST, it fetches data from the API, processes it, and displays it.
    Otherwise, it renders the default form.
    """
    if request.method == 'POST':
        # Get form data
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        
        # Fetch car data from the API
        car_data = fetch_car_data(make, model, year)
        if car_data:
            # Create a DataFrame and render it as an HTML table
            df = create_dataframe(car_data)
            return render_template('index.html', tables=[df.to_html(classes='data', header="true")])
        else:
            # Display an error message if no data is found
            return render_template('index.html', error="No data found for the specified car.")
    
    # Render the default index page
    return render_template('index.html')

# Route for the compare cars page
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    """
    Handles the compare cars page where users can input details of two cars
    and view a side-by-side comparison.

    If the request method is POST, it fetches data for both cars from the API
    and displays it in two separate tables.
    """
    if request.method == 'POST':
        # Get form data for both cars
        make1 = request.form['make1']
        model1 = request.form['model1']
        year1 = request.form['year1']
        make2 = request.form['make2']
        model2 = request.form['model2']
        year2 = request.form['year2']
        
        # Fetch car data for both cars
        car_data1 = fetch_car_data(make1, model1, year1)
        car_data2 = fetch_car_data(make2, model2, year2)
        
        # Create DataFrames for both cars
        df1 = create_dataframe(car_data1)
        df2 = create_dataframe(car_data2)
        
        # Render the comparison page with both tables
        return render_template('compare.html', 
                               table1=df1.to_html(classes='data', header="true"), 
                               table2=df2.to_html(classes='data', header="true"))
    
    # Render the default compare page
    return render_template('compare.html')

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
