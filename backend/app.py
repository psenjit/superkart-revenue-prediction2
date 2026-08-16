
# Import necessary libraries
import numpy as np
import joblib 
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name
superkart_api = Flask("SuperKart Sales Forcast")

# Load the trained churn prediction model
model = joblib.load("superkart_revenue_prediction_model_v1.0.joblib")

# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to SuperKart Sales Forcast App"

# # Define an endpoint for single prediction
@superkart_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()

    
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a churn prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})

# Define an endpoint for batch prediction (POST request)
@superkart_api.post('/v1/predictbatch')
def predict_in_batch():
    
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make a churn prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})
    

# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
