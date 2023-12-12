# Import necessary Python packages
import os  
import git  
import json  
import pandas as pd  
import mysql.connector  
import streamlit as st  
import requests  
import numpy as np  
import plotly.express as px  
import time  
from PIL import Image 

def github_cloning():
    try:
        # Try to clone the GitHub repository
        git.Repo.clone_from("https://github.com/PhonePe/pulse.git", 'pulse')
    except Exception as e:
        # If an exception occurs (e.g., repository already exists), catch it and do nothing
        pass

# Set Streamlit page configuration: title and layout
st.set_page_config(page_title="Phonepe", layout="wide")

# Function to retrieve aggregated transaction data
def aggregated_transaction():
    # Define the path to the transaction data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\aggregated\transaction\country\india\state"
    agg_state_trans = os.listdir(path)
    # Initialize a dictionary to store aggregated transaction data
    Agg_trans = {'States': [], 'Years': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}
    # Loop through states, years, and JSON files to gather transaction data
    for state in agg_state_trans:
        present_state = os.path.join(path, state)
        agg_year_trans = os.listdir(present_state)
        for year in agg_year_trans:
            present_year = os.path.join(present_state, year)
            agg_json_trans = os.listdir(present_year)
            for file in agg_json_trans:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                for i in json_data["data"]["transactionData"]:
                    Name = i["name"]
                    Count = i["paymentInstruments"][0]["count"]
                    Amount = i["paymentInstruments"][0]["amount"]
                    Agg_trans["States"].append(state)
                    Agg_trans["Years"].append(year)
                    Agg_trans["Quarter"].append(int(file.strip('.json')))
                    Agg_trans["Transaction_type"].append(Name)
                    Agg_trans["Transaction_count"].append(Count)
                    Agg_trans["Transaction_amount"].append(Amount)
    return Agg_trans

# Function to retrieve aggregated user data
def aggregated_user():
    # Define the path to the user data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\aggregated\user\country\india\state"
    agg_state_user = os.listdir(path)
    # Initialize a dictionary to store aggregated user data
    Agg_user = {'States': [], 'Years': [], 'Quarter': [], 'Brands': [], 'User_count': [], 'User_percentage': []}
    # Loop through states, years, and JSON files to gather user data
    for state in agg_state_user:
        present_state = os.path.join(path, state)
        agg_year_user = os.listdir(present_state)
        for year in agg_year_user:
            present_year = os.path.join(present_state, year)
            agg_json_user = os.listdir(present_year)
            for file in agg_json_user:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                try:
                    for i in json_data["data"]["usersByDevice"]:
                        Brands = i["brand"]
                        Count = i["count"]
                        Percentage = i["percentage"]
                        Agg_user["States"].append(state)
                        Agg_user["Years"].append(year)
                        Agg_user["Quarter"].append(int(file.strip('.json')))
                        Agg_user["Brands"].append(Brands)
                        Agg_user["User_count"].append(Count)
                        Agg_user["User_percentage"].append(Percentage * 100)
                except:
                    pass
    return Agg_user

# Function to retrieve map transaction data
def map_transaction():
    # Define the path to the map transaction data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\map\transaction\hover\country\india\state"
    map_state_trans = os.listdir(path)
    # Initialize a dictionary to store map transaction data
    Map_trans = {'States': [], 'Years': [], 'Quarter': [], 'Districts': [], 'Transaction_count': [], 'Transaction_amount': []}
    # Loop through states, years, and JSON files to gather map transaction data
    for state in map_state_trans:
        present_state = os.path.join(path, state)
        map_year_trans = os.listdir(present_state)
        for year in map_year_trans:
            present_year = os.path.join(present_state, year)
            map_json_trans = os.listdir(present_year)
            for file in map_json_trans:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                for i in json_data["data"]["hoverDataList"]:
                    Name = i["name"]
                    Count = i["metric"][0]["count"]
                    Amount = i["metric"][0]["amount"]
                    Map_trans["States"].append(state)
                    Map_trans["Years"].append(year)
                    Map_trans["Quarter"].append(int(file.strip('.json')))
                    Map_trans["Districts"].append(Name)
                    Map_trans["Transaction_count"].append(Count)
                    Map_trans["Transaction_amount"].append(Amount)
    return Map_trans

# Function to retrieve map user data
def map_user():
    # Define the path to the map user data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\map\user\hover\country\india\state"
    map_state_user = os.listdir(path)
    # Initialize a dictionary to store map user data
    Map_user = {'States': [], 'Years': [], 'Quarter': [], "Districts": [], "Registered_user": [], "App_opens": []}
    # Loop through states, years, and JSON files to gather map user data
    for state in map_state_user:
        present_state = os.path.join(path, state)
        map_year_user = os.listdir(present_state)
        for year in map_year_user:
            present_year = os.path.join(present_state, year)
            map_json_user = os.listdir(present_year)
            for file in map_json_user:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                    for district, data in json_data["data"]["hoverData"].items():
                        Name = district
                        Registered_user = data["registeredUsers"]
                        App_opens = data["appOpens"]
                        Map_user["States"].append(state)
                        Map_user["Years"].append(year)
                        Map_user["Quarter"].append(int(file.strip('.json')))
                        Map_user["Districts"].append(Name)
                        Map_user["Registered_user"].append(Registered_user)
                        Map_user["App_opens"].append(App_opens)
    return Map_user

# Function to retrieve top transaction pincodes data
def top_transaction_pincodes():
    # Define the path to the top transaction pincodes data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\top\transaction\country\india\state"
    top_state_trans = os.listdir(path)
    # Initialize a dictionary to store top transaction pincodes data
    Top_trans_pin = {'States': [], 'Years': [], 'Quarter': [], 'Pincodes': [], 'Transaction_count': [], 'Transaction_amount': []}
    # Loop through states, years, and JSON files to gather top transaction pincodes data
    for state in top_state_trans:
        present_state = os.path.join(path, state)
        top_year_trans = os.listdir(present_state)
        for year in top_year_trans:
            present_year = os.path.join(present_state, year)
            top_json_trans = os.listdir(present_year)
            for file in top_json_trans:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                for i in json_data["data"]["pincodes"]:
                    Name = i["entityName"]
                    Count = i['metric']['count']
                    Amount = i['metric']['amount']
                    Top_trans_pin["States"].append(state)
                    Top_trans_pin["Years"].append(year)
                    Top_trans_pin["Quarter"].append(int(file.strip('.json')))
                    Top_trans_pin["Pincodes"].append(Name)
                    Top_trans_pin["Transaction_count"].append(Count)
                    Top_trans_pin["Transaction_amount"].append(Amount)
    return Top_trans_pin

# Function to retrieve top transaction districts data
def top_transaction_districts():
    # Define the path to the top transaction districts data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\top\transaction\country\india\state"
    top_state_trans = os.listdir(path)
    # Initialize a dictionary to store top transaction districts data
    Top_trans_dist = {'States': [], 'Years': [], 'Quarter': [], 'Districts': [], 'Transaction_count': [], 'Transaction_amount': []}
    # Loop through states, years, and JSON files to gather top transaction districts data
    for state in top_state_trans:
        present_state = os.path.join(path, state)
        top_year_trans = os.listdir(present_state)
        for year in top_year_trans:
            present_year = os.path.join(present_state, year)
            top_json_trans = os.listdir(present_year)
            for file in top_json_trans:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                for i in json_data["data"]["districts"]:
                    Name = i["entityName"]
                    Count = i['metric']['count']
                    Amount = i['metric']['amount']
                    Top_trans_dist["States"].append(state)
                    Top_trans_dist["Years"].append(year)
                    Top_trans_dist["Quarter"].append(int(file.strip('.json')))
                    Top_trans_dist["Districts"].append(Name)
                    Top_trans_dist["Transaction_count"].append(Count)
                    Top_trans_dist["Transaction_amount"].append(Amount)
    return Top_trans_dist

# Function to retrieve top user pincodes data
def top_user_pincodes():
    # Define the path to the top user pincodes data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\top\user\country\india\state"
    top_state_user = os.listdir(path)
    # Initialize a dictionary to store top user pincodes data
    Top_user_pin = {'States': [], 'Years': [], 'Quarter': [], 'Pincodes': [], 'Registered_user': []}
    # Loop through states, years, and JSON files to gather top user pincodes data
    for state in top_state_user:
        present_state = os.path.join(path, state)
        top_year_user = os.listdir(present_state)
        for year in top_year_user:
            present_year = os.path.join(present_state, year)
            top_json_user = os.listdir(present_year)
            for file in top_json_user:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                for i in json_data["data"]["pincodes"]:
                    Name = i['name']
                    Registered_user = i['registeredUsers']
                    Top_user_pin["States"].append(state)
                    Top_user_pin["Years"].append(year)
                    Top_user_pin["Quarter"].append(int(file.strip('.json')))
                    Top_user_pin["Pincodes"].append(Name)
                    Top_user_pin["Registered_user"].append(Registered_user)
    return Top_user_pin

# Function to retrieve top user districts data
def top_user_districts():
    # Define the path to the top user districts data
    path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\pulse\data\top\user\country\india\state"
    top_state_user = os.listdir(path)
    # Initialize a dictionary to store top user districts data
    Top_user_dist = {'States': [], 'Years': [], 'Quarter': [], 'Districts': [], 'Registered_user': []}
    # Loop through states, years, and JSON files to gather top user districts data
    for state in top_state_user:
        present_state = os.path.join(path, state)
        top_year_user = os.listdir(present_state)
        for year in top_year_user:
            present_year = os.path.join(present_state, year)
            top_json_user = os.listdir(present_year)
            for file in top_json_user:
                json_file_path = os.path.join(present_year, file)
                with open(json_file_path, "r") as data:
                    json_data = json.load(data)
                for i in json_data["data"]["districts"]:
                    Name = i['name']
                    Registered_user = i['registeredUsers']
                    Top_user_dist["States"].append(state)
                    Top_user_dist["Years"].append(year)
                    Top_user_dist["Quarter"].append(int(file.strip('.json')))
                    Top_user_dist["Districts"].append(Name)
                    Top_user_dist["Registered_user"].append(Registered_user)
    return Top_user_dist 

# Function to perform data transformation
def data_transformation():
    # Create DataFrames for each data category
    df_aggregated_transaction = pd.DataFrame(aggregated_transaction())  # Aggregated transaction data
    df_aggregated_user = pd.DataFrame(aggregated_user())  # Aggregated user data
    df_map_transaction = pd.DataFrame(map_transaction())  # Map transaction data
    df_map_user = pd.DataFrame(map_user())  # Map user data
    df_top_transaction_pincodes = pd.DataFrame(top_transaction_pincodes())  # Top transaction pincodes data
    df_top_transaction_districts = pd.DataFrame(top_transaction_districts())  # Top transaction districts data
    df_top_user_pincodes = pd.DataFrame(top_user_pincodes())  # Top user pincodes data
    df_top_user_districts = pd.DataFrame(top_user_districts())  # Top user districts data
    # Return the created DataFrames
    return df_aggregated_transaction, df_aggregated_user, df_map_transaction, df_map_user, df_top_transaction_pincodes, df_top_transaction_districts, df_top_user_pincodes, df_top_user_districts

# Function to create a connection to the MySQL database
def create_connection():
    # Establish a connection to the MySQL database
    mysqldb = mysql.connector.connect(
        host="localhost",                  # Specify the MySQL server host (usually the local machine)
        user="root",                       # MySQL username for authentication
        password="123",                    # Password for the MySQL user
        port="3306",                       # Port number (default is 3306)
        database="Phonepe_pulse")          # Name of the MySQL database
    # Create a cursor object for MySQL operations
    mycursor = mysqldb.cursor(buffered=True)
    return mysqldb, mycursor 

# Function to drop existing tables
def drop_tables(mycursor):
    # Drop tables if they exist
    mycursor.execute("DROP TABLE IF EXISTS Aggregated_Transaction, Aggregated_User, Map_Transaction, Map_User, Top_Transaction_Pincodes, Top_Transaction_Districts, Top_User_Pincodes, Top_User_Districts")

# Define the SQL query to create the table if it doesn't exist
def create_tables(mycursor):
    # Table: Aggregated_Transaction
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Aggregated_Transaction (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Transaction_type VARCHAR(50),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE)""")   
    # Table: Aggregated_User
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Aggregated_User (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Brands VARCHAR(50),
        User_count BIGINT,
        User_percentage DOUBLE)""")      
    # Table: Map_Transaction
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Map_Transaction (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Districts VARCHAR(50),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE)""")    
    # Table: Map_User
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Map_User (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Districts VARCHAR(50),
        Registered_user BIGINT,
        App_opens BIGINT)""")
    # Table: Top_Transaction_Pincodes
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_Transaction_Pincodes (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Pincodes INT,
        Transaction_count BIGINT,
        Transaction_amount DOUBLE)""")    
    # Table: Top_Transaction_Districts
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_Transaction_Districts (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Districts VARCHAR(50),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE)""")
    # Table: Top_User_Pincodes
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_User_Pincodes (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Pincodes INT,
        Registered_user BIGINT)""")
    # Table: Top_User_Districts
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_User_Districts (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Districts VARCHAR(50),
        Registered_user BIGINT)""") 

# Function to insert data from DataFrames into corresponding MySQL tables
def insert_values(mycursor, df_aggregated_transaction, df_aggregated_user, df_map_transaction, df_map_user, df_top_transaction_pincodes, df_top_transaction_districts, df_top_user_pincodes, df_top_user_districts):
    # Insert values into Aggregated_Transaction table
    query = "INSERT INTO Aggregated_Transaction(States, Years, Quarter, Transaction_type, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"
    values_aggregated_transaction = df_aggregated_transaction[['States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount']].values.tolist()
    mycursor.executemany(query, values_aggregated_transaction)
    # Insert values into Aggregated_User table
    query = "INSERT INTO Aggregated_User(States, Years, Quarter, Brands, User_count, User_percentage) VALUES (%s, %s, %s, %s, %s, %s)"
    values_aggregated_user = df_aggregated_user[['States', 'Years', 'Quarter', 'Brands', 'User_count', 'User_percentage']].values.tolist()
    mycursor.executemany(query, values_aggregated_user)   
    # Insert values into Map_Transaction table
    query = "INSERT INTO Map_Transaction(States, Years, Quarter, Districts, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"
    values_map_transaction = df_map_transaction[['States', 'Years', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount']].values.tolist()
    mycursor.executemany(query, values_map_transaction)
    # Insert values into Map_User table
    query = "INSERT INTO Map_User(States, Years, Quarter, Districts, Registered_user, App_opens) VALUES (%s, %s, %s, %s, %s, %s)"
    values_map_user = df_map_user[['States', 'Years', 'Quarter', 'Districts', 'Registered_user', 'App_opens']].values.tolist()
    mycursor.executemany(query, values_map_user)
    # Insert values into Top_Transaction_Pincodes table
    query = "INSERT INTO Top_Transaction_Pincodes(States, Years, Quarter, Pincodes, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"
    values_top_transaction_pincodes = df_top_transaction_pincodes[['States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count', 'Transaction_amount']].values.tolist()
    mycursor.executemany(query, values_top_transaction_pincodes)
    # Insert values into Top_Transaction_Districts table
    query = "INSERT INTO Top_Transaction_Districts(States, Years, Quarter, Districts, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"
    values_top_transaction_districts = df_top_transaction_districts[['States', 'Years', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount']].values.tolist()
    mycursor.executemany(query, values_top_transaction_districts)
    # Insert values into Top_User_Pincodes table
    query = "INSERT INTO Top_User_Pincodes(States, Years, Quarter, Pincodes, Registered_user) VALUES (%s, %s, %s, %s, %s)"
    values_top_user_pincodes = df_top_user_pincodes[['States', 'Years', 'Quarter', 'Pincodes', 'Registered_user']].values.tolist()
    mycursor.executemany(query, values_top_user_pincodes)
    # Insert values into Top_User_Districts table
    query = "INSERT INTO Top_User_Districts(States, Years, Quarter, Districts, Registered_user) VALUES (%s, %s, %s, %s,%s)"
    values_top_user_districts = df_top_user_districts[['States', 'Years', 'Quarter','Districts', 'Registered_user']].values.tolist()
    mycursor.executemany(query, values_top_user_districts)

# Function to commit changes and close the MySQL database connection
def close_connection(mysqldb, mycursor):
    mysqldb.commit()
    mycursor.close()
    mysqldb.close()

# Function to perform data insertion into MySQL database
def data_insertion_sql():
    # Create a connection to the MySQL database
    mysqldb, mycursor = create_connection()    
    # Drop existing tables if they exist
    drop_tables(mycursor)    
    # Perform data transformation to obtain DataFrames
    df_aggregated_transaction, df_aggregated_user, df_map_transaction, df_map_user, df_top_transaction_pincodes, df_top_transaction_districts, df_top_user_pincodes, df_top_user_districts = data_transformation()    
    # Create new tables in the MySQL database
    create_tables(mycursor)    
    # Insert values into the created tables
    insert_values(mycursor, df_aggregated_transaction, df_aggregated_user, df_map_transaction, df_map_user, df_top_transaction_pincodes, df_top_transaction_districts, df_top_user_pincodes, df_top_user_districts)    
    # Close the MySQL database connection
    close_connection(mysqldb, mycursor)

#Function to convert count or values to readable format
def convert_amount(value):
    # Convert the value to a string and replace commas if present
    amount_str = str(value).replace(',', '')
    # Convert the string to a float
    amount = float(amount_str)
    # Format the amount based on different ranges
    if amount < 1000:
        # If the amount is less than 1000, return it as an integer
        return str(int(amount))
    elif amount < 100000:
        # If the amount is less than 100000, format it in thousands (K)
        return '{:.2f}K'.format(amount / 1000)
    elif amount < 10000000:
        # If the amount is less than 10000000, format it in lakhs (L)
        return '{:.2f}L'.format(amount / 100000)
    elif amount < 1000000000:
        # If the amount is less than 1000000000, format it in crores (Cr)
        return '{:.2f}Cr'.format(amount / 10000000)
    elif amount < 1000000000000:
        # If the amount is less than 1000000000000, format it in billions (B)
        return '{:.2f}B'.format(amount / 1000000000)
    else:
        # If the amount is greater than or equal to 1000000000000, format it in trillions (T)
        return '{:.2f}T'.format(amount / 1000000000000)  

#Function to load GeoJSON data
def load_geojson_data():
    # URL of the GeoJSON file containing India states data
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"    
    # Send an HTTP GET request to the URL
    response = requests.get(geojson_url, timeout=10)    
    # Load the JSON content from the response
    geo_data = json.loads(response.content)    
    # Extract state names from the GeoJSON data
    geo_states = [i['properties']['ST_NM'] for i in geo_data['features']]   
    # Sort the state names in ascending order
    geo_states.sort(reverse=False)
    # Create a DataFrame with the sorted state names
    df_geo_states = pd.DataFrame({"States": geo_states})    
    return df_geo_states

#Function for mapping states in MySQL with GeoJSON States
def map_states(states_column, reverse=False):
    # Dictionary mapping original states in MySQL with state names from the GeoJSON data
    state_mapping = {'andaman-&-nicobar-islands': 'Andaman & Nicobar', 'andhra-pradesh': 'Andhra Pradesh', 'arunachal-pradesh': 'Arunachal Pradesh',
                     'assam': 'Assam', 'bihar': 'Bihar', 'chandigarh': 'Chandigarh', 'chhattisgarh': 'Chhattisgarh',
                     'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa': 'Goa',
                     'gujarat': 'Gujarat', 'haryana': 'Haryana', 'himachal-pradesh': 'Himachal Pradesh', 'jammu-&-kashmir': 'Jammu & Kashmir',
                     'jharkhand': 'Jharkhand', 'karnataka': 'Karnataka', 'kerala': 'Kerala', 'ladakh': 'Ladakh', 'lakshadweep': 'Lakshadweep',
                     'madhya-pradesh': 'Madhya Pradesh', 'maharashtra': 'Maharashtra', 'manipur': 'Manipur', 'meghalaya': 'Meghalaya',
                     'mizoram': 'Mizoram', 'nagaland': 'Nagaland', 'odisha': 'Odisha', 'puducherry': 'Puducherry', 'punjab': 'Punjab', 
                     'rajasthan': 'Rajasthan', 'sikkim': 'Sikkim', 'tamil-nadu': 'Tamil Nadu', 'telangana': 'Telangana', 'tripura': 'Tripura',
                     'uttar-pradesh': 'Uttar Pradesh', 'uttarakhand': 'Uttarakhand', 'west-bengal': 'West Bengal'}
    if reverse:
        return states_column.map({v: k for k, v in state_mapping.items()})   # Reverse mapping
    else: 
        return states_column.map(state_mapping)  

# Generalised function to fetch data for chropleth plot 
def fetch_aggregated_data(query, value_column, value_column2=None, convert_to_float=False):
    # Establish a connection to the MySQL database
    mysqldb, mycursor = create_connection()
    # Load geographical states data using GeoJSON
    df_geo_states = load_geojson_data()
    # Execute the provided query on the database
    mycursor.execute(query)
    # Define columns for the resulting DataFrame
    if value_column2:
        columns = ['States', value_column, value_column2]
    else:
        columns = ['States', value_column]
    # Create a DataFrame from the fetched data
    data = pd.DataFrame(mycursor.fetchall(), columns=columns)
    # Map state names to their corresponding GeoJSON representations
    data['Geo_States'] = map_states(data['States'])
    # Convert specified columns to float if required
    if convert_to_float:
        data[value_column] = data[value_column].astype(float)
        if value_column2:
            data[value_column2] = data[value_column2].astype(float)
    # Apply custom conversion function to the specified columns
    if value_column2:
        data['Converted_' + value_column2] = data[value_column2].apply(convert_amount)
        data = data[['Geo_States', value_column, value_column2, 'Converted_' + value_column2]]
    else:
        data['Converted_' + value_column] = data[value_column].apply(convert_amount)
        data = data[['Geo_States', value_column, 'Converted_' + value_column]]
    # Close the database connection
    close_connection(mysqldb, mycursor)
    return data

# Function to fetch transaction count data
def fetch_transaction_count(convert_to_float=False):
    query = "SELECT States, SUM(Transaction_count) as Total_Transaction_Count FROM Aggregated_Transaction GROUP BY States;"
    return fetch_aggregated_data(query, 'Total_Transaction_Count', convert_to_float=convert_to_float)
# Function to fetch transaction amount data
def fetch_transaction_amount():
    query = "SELECT States, SUM(Transaction_amount) as Total_Transaction_Amount FROM Aggregated_Transaction GROUP BY States;"
    return fetch_aggregated_data(query, 'Total_Transaction_Amount')
# Function to fetch user count data
def fetch_user_count(convert_to_float=False):
    query = "SELECT States, SUM(User_count) as Total_User_Count FROM Aggregated_User GROUP BY States;"
    return fetch_aggregated_data(query, 'Total_User_Count', convert_to_float=convert_to_float)
# Function to fetch registered user count data
def fetch_registered_user_count():
    query = "SELECT States, Districts, Registered_user FROM Map_User;"
    return fetch_aggregated_data(query, 'Districts', 'Registered_Users_Count') 
# Function to fetch app opens count data
def fetch_app_opens_count():
    query = "SELECT States, Districts, App_opens FROM Map_User;"
    return fetch_aggregated_data(query, 'Districts', 'App_Opens_Count')

# Function to set Mapbox access token
def set_mapbox_access_token(token):
    px.set_mapbox_access_token(token) 

# Set Mapbox access token for geographical visualizations
set_mapbox_access_token("pk.eyJ1IjoicHJpeWFuZ2EwNzAzIiwiYSI6ImNscGUzYWxqcDE0ZngyamxzNnplZmRoNXQifQ.2PF095gqVqidmrdam8F9TA")

# Function to create choropleth map
def create_choropleth_map(data, color_column, converted_column, title, selected_year_quarter):
    formatted_title = f'{title} ({selected_year_quarter})'
    # Create a choropleth map using Plotly Express
    fig = px.choropleth_mapbox(
        data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='Geo_States',
        color=color_column,
        hover_data={color_column: False, converted_column: True},
        color_continuous_scale=px.colors.diverging.Spectral,
        mapbox_style="satellite-streets",
        title=formatted_title,
        center={'lat': 20.5937, 'lon': 78.9629},
        opacity=0.8)
    # Set tick values and labels for color axis
    tick_values = [data[color_column].min(), data[color_column].max()]
    tick_labels = ['{:.2f}'.format(val) for val in tick_values]
    # Update layout settings for the map
    fig.update_layout(mapbox_zoom=2.5, coloraxis_colorbar=dict(
        title=color_column,
        ticks='outside',
        tickvals=tick_values,
        ticktext=tick_labels,
        lenmode='pixels',
        len=280),
        title_x=0.15, title_y=0.99, autosize=False, height=450, width=350, margin={"r": 0, "t": 40, "l": 0, "b": 0})
    # Display the chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Create choropleth map for Transaction Count
def create_transaction_count_choropleth(selected_year_quarter):
    # Fetch transaction count data from the database, converting values to float
    data_transaction_count = fetch_transaction_count(convert_to_float=True)
    # Create choropleth map for transaction count
    return create_choropleth_map(data_transaction_count, 'Total_Transaction_Count', 'Converted_Total_Transaction_Count', 'Transaction Count in India', selected_year_quarter)
# Create choropleth map for Transaction Amount
def create_transaction_amount_choropleth(selected_year_quarter):
    # Fetch transaction amount data from the database
    data_transaction_amount = fetch_transaction_amount()
    # Create choropleth map for transaction amount
    return create_choropleth_map(data_transaction_amount, 'Total_Transaction_Amount', 'Converted_Total_Transaction_Amount', 'Transaction Amount in India', selected_year_quarter)
# Create choropleth map for User Count
def create_user_count_choropleth(selected_year_quarter):
    # Fetch user count data from the database, converting values to float
    data_user_count = fetch_user_count(convert_to_float=True)
    # Create choropleth map for user count
    return create_choropleth_map(data_user_count, 'Total_User_Count', 'Converted_Total_User_Count', 'User Count in India', selected_year_quarter)
# Create choropleth map for Registered User Count
def create_registered_user_count_choropleth(selected_year_quarter):
    # Fetch registered user count data from the database
    data_registered_user_count = fetch_registered_user_count()
    # Create choropleth map for registered user count
    return create_choropleth_map(data_registered_user_count, 'Registered_Users_Count', 'Converted_Registered_Users_Count', 'Registered Users in India', selected_year_quarter)
# Create choropleth map for App Opens Count
def create_app_opens_count_choropleth(selected_year_quarter):
    # Fetch app opens count data from the database
    data_app_opens_count = fetch_app_opens_count()
    # Create choropleth map for app opens count
    return create_choropleth_map(data_app_opens_count, 'App_Opens_Count', 'Converted_App_Opens_Count', 'App Opens in India', selected_year_quarter)

#Function to fetch Transaction type data from the database
def fetch_transaction_type_data(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Transaction_type, SUM(Transaction_amount), SUM(Transaction_count) FROM Aggregated_Transaction WHERE Years=%s AND Quarter=%s GROUP BY Transaction_type;"    
    mycursor.execute(query, (Years, Quarter))    
    data = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Transaction_amount', 'Transaction_count'])    
    data["Converted_Transaction_Amount"] = data["Transaction_amount"].apply(convert_amount)
    data["Converted_Transaction_Count"] = data["Transaction_count"].apply(convert_amount)
    close_connection(mysqldb, mycursor)    
    return data

#Function to fetch user brand data from the database
def fetch_user_brand_count(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Years, Quarter, Brands, SUM(User_count) AS Total_User_Count FROM Aggregated_User WHERE Years=%s AND Quarter=%s GROUP BY Brands;"
    mycursor.execute(query, (Years, Quarter))
    data_user_brand_count = pd.DataFrame(mycursor.fetchall(), columns=['Years', 'Quarter','Brands', 'Total_User_Count'])
    data_user_brand_count["Converted_User_Count"] = data_user_brand_count["Total_User_Count"].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data_user_brand_count

# Function to create bar chart
def create_bar_chart(data, x_column, y_column, converted_column, title, xaxis_title, yaxis_title):
    # Create a bar chart using Plotly Express
    fig = px.bar(data, x=x_column, y=y_column,
                 title=title,
                 text=converted_column,
                 color=x_column, hover_data={y_column: False, converted_column: True})
    # Update layout settings for the chart
    fig.update_layout(xaxis_title=xaxis_title, yaxis_title=yaxis_title,
                      title=dict(text=title, x=0.5, y=0.95, xanchor='center', yanchor='top'), width=1100,
                      margin=dict(l=50, r=50, t=50, b=50))
    # Display the chart using Streamlit
    st.plotly_chart(fig) 
    
# Visualize transaction type count for a selected year quarter
def visualize_transaction_type_count(selected_year_quarter):
    # Fetch aggregated transaction data
    df_aggregated_transaction = fetch_transaction_type_data(selected_year_quarter)
    # Create a bar chart for transaction type count
    create_bar_chart(df_aggregated_transaction, 'Transaction_type', 'Transaction_count', 'Converted_Transaction_Count',
                           f'Transaction Count Comparison ({selected_year_quarter})', 'Transaction Type', 'Transaction Count')
# Visualize transaction type amount for a selected year quarter
def visualize_transaction_type_amount(selected_year_quarter):
    # Fetch aggregated transaction data
    df_aggregated_transaction = fetch_transaction_type_data(selected_year_quarter)
    # Create a bar chart for transaction type amount
    create_bar_chart(df_aggregated_transaction, 'Transaction_type', 'Transaction_amount', 'Converted_Transaction_Amount',
                           f'Transaction Amount Comparison ({selected_year_quarter})', 'Transaction Type', 'Transaction Amount')
# Visualize user brand count for a selected year quarter
def visualize_user_brand_count(selected_year_quarter):
    # Fetch user brand count data
    df_user_brand_count = fetch_user_brand_count(selected_year_quarter)
    # Create a bar chart for user brand count
    create_bar_chart(df_user_brand_count, 'Brands', 'Total_User_Count', 'Converted_User_Count',
                     f'User Count Comparison by Brands ({selected_year_quarter})', 'Brands', 'User Count')

# Generalised function to fetch Districts data for line plot 
def fetch_districts_data(selected_year_quarter, selected_states, table_name, value_column):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4])
    Quarter = selected_year_quarter[6:]
    sql_states = map_states(pd.Series(selected_states), reverse=True).tolist()
    placeholders = ', '.join(['%s' for _ in sql_states])
    query = f"SELECT States, Years, Quarter, Districts, SUM({value_column}) AS Total_{value_column} FROM {table_name} WHERE States IN ({placeholders}) AND Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Districts;"
    mycursor.execute(query, (*sql_states, Years, Quarter))    
    data = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Districts', f'Total_{value_column}'])
    data['Districts'] = data['Districts'].str.capitalize()
    data[f"Converted_Total_{value_column}"] = data[f'Total_{value_column}'].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data

# Function to create line plot
def create_line_plot(selected_year_quarter, data, y_column, converted_column, title):
    # Create line plot using Plotly Express
    fig = px.line(data, x='Districts', y=y_column,
                  title=title, color_discrete_sequence=px.colors.diverging.Spectral,
                  hover_data={y_column: True, converted_column: True})    
    # Update layout settings for the chart
    fig.update_layout(title=dict(text=title, x=0.5, y=0.95, xanchor='center', yanchor='top'), width=1100)    
    # Display the chart using Streamlit
    st.plotly_chart(fig)

# Visualize transaction count trend by districts for selected states and year quarter
def visualize_districts_transaction_count(selected_year_quarter, selected_states):
    # Fetch data for transaction count by districts
    data_districts_transaction_count = fetch_districts_data(selected_year_quarter, selected_states, 'Map_Transaction', 'Transaction_count')
    # Create line plot for transaction count trend
    create_line_plot(selected_year_quarter, data_districts_transaction_count, 'Total_Transaction_count',
                     'Converted_Total_Transaction_count', f'Transaction Count Trend by Districts of {selected_states} in {selected_year_quarter}')
# Visualize transaction amount trend by districts for selected states and year quarter
def visualize_districts_transaction_amount(selected_year_quarter, selected_states):
    # Fetch data for transaction amount by districts
    data_districts_transaction_amount = fetch_districts_data(selected_year_quarter, selected_states, 'Map_Transaction', 'Transaction_amount')
    # Create line plot for transaction amount trend
    create_line_plot(selected_year_quarter, data_districts_transaction_amount, 'Total_Transaction_amount',
                     'Converted_Total_Transaction_amount', f'Transaction Amount Trend by Districts of {selected_states} in {selected_year_quarter}')
# Visualize registered users trend by districts for selected states and year quarter
def visualize_districts_registered_users(selected_year_quarter, selected_states):
    # Fetch data for registered users by districts
    data_districts_map_reg_user = fetch_districts_data(selected_year_quarter, selected_states, 'Map_User', 'Registered_user')
    # Create line plot for registered users trend
    create_line_plot(selected_year_quarter, data_districts_map_reg_user, 'Total_Registered_user',
                     'Converted_Total_Registered_user', f'Registered Users Trend by Districts of {selected_states} in {selected_year_quarter}')
# Visualize app opens trend by districts for selected states and year quarter
def visualize_districts_app_opens(selected_year_quarter, selected_states):
    # Fetch data for app opens by districts
    data_districts_map_app_opens = fetch_districts_data(selected_year_quarter, selected_states, 'Map_User', 'App_opens')
    # Create line plot for app opens trend
    create_line_plot(selected_year_quarter, data_districts_map_app_opens, 'Total_App_opens',
                     'Converted_Total_App_opens', f'App Opens Trend by Districts of {selected_states} in {selected_year_quarter}')

#Function to fetch Top states transaction count data from the database
def fetch_top_states_transaction_count(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, SUM(Transaction_count) AS Total_Transaction_Count FROM Aggregated_Transaction WHERE Years=%s AND Quarter=%s GROUP BY States ORDER BY Total_Transaction_Count DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_states_transaction = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Total_Transaction_Count'])
    data_top_states_transaction["Converted_Transaction_Count"] = data_top_states_transaction["Total_Transaction_Count"].apply(convert_amount)
    data_top_states_transaction["Total_Transaction_Count"] = data_top_states_transaction["Total_Transaction_Count"].astype(float)
    data_top_states_transaction['Geo_States'] = map_states(data_top_states_transaction['States'])
    data_top_states_transaction = data_top_states_transaction[['Geo_States', 'Total_Transaction_Count', 'Converted_Transaction_Count']]
    close_connection(mysqldb, mycursor)
    return data_top_states_transaction

#Function to fetch Top districts transaction count data from the database
def fetch_top_districts_transaction_count(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, Districts, Transaction_count FROM Top_Transaction_Districts WHERE Years=%s AND Quarter=%s ORDER BY Transaction_count DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_districts_transaction = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Districts', 'Transaction_count'])
    data_top_districts_transaction["Converted_Transaction_Count"] = data_top_districts_transaction["Transaction_count"].apply(convert_amount)
    data_top_districts_transaction['Geo_States'] = map_states(data_top_districts_transaction['States'])
    data_top_districts_transaction['Districts'] = data_top_districts_transaction['Districts'].str.capitalize()
    data_top_districts_transaction = data_top_districts_transaction[['Districts', 'Transaction_count', 'Converted_Transaction_Count']]
    close_connection(mysqldb, mycursor)
    return data_top_districts_transaction

#Function to fetch Top states transaction amount data from the database
def fetch_top_states_transaction_amount(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, SUM(Transaction_amount) AS Total_Transaction_Amount FROM Aggregated_Transaction WHERE Years=%s AND Quarter=%s GROUP BY States ORDER BY Total_Transaction_Amount DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_states_transaction = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Total_Transaction_Amount'])
    data_top_states_transaction["Converted_Transaction_Amount"] = data_top_states_transaction["Total_Transaction_Amount"].apply(convert_amount)
    data_top_states_transaction['Geo_States'] = map_states(data_top_states_transaction['States'])
    data_top_states_transaction = data_top_states_transaction[['Geo_States', 'Total_Transaction_Amount', 'Converted_Transaction_Amount']]
    close_connection(mysqldb, mycursor)
    return data_top_states_transaction

#Function to fetch Top districts transaction amount data from the database
def fetch_top_districts_transaction_amount(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, Districts, Transaction_amount FROM Top_Transaction_Districts WHERE Years=%s AND Quarter=%s ORDER BY Transaction_amount DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_districts_transaction = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Districts', 'Transaction_amount'])
    data_top_districts_transaction["Converted_Transaction_Amount"] = data_top_districts_transaction["Transaction_amount"].apply(convert_amount)
    data_top_districts_transaction['Geo_States'] = map_states(data_top_districts_transaction['States'])
    data_top_districts_transaction['Districts'] = data_top_districts_transaction['Districts'].str.capitalize()
    data_top_districts_transaction = data_top_districts_transaction[['Districts', 'Transaction_amount', 'Converted_Transaction_Amount']]
    close_connection(mysqldb, mycursor)
    return data_top_districts_transaction

#Function to fetch Top states user data from the database
def fetch_top_states_user(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, SUM(Registered_User) AS Total_Registered_User FROM Map_User WHERE Years=%s AND Quarter=%s GROUP BY States ORDER BY Total_Registered_User DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_states_user = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Total_Registered_User'])
    data_top_states_user["Total_Registered_User"] = data_top_states_user["Total_Registered_User"].astype(float)
    data_top_states_user['Geo_States'] = map_states(data_top_states_user['States'])
    data_top_states_user["Converted_Registered_User"] = data_top_states_user["Total_Registered_User"].apply(convert_amount)
    data_top_states_user = data_top_states_user[['Geo_States', 'Total_Registered_User', 'Converted_Registered_User']]
    close_connection(mysqldb, mycursor)
    return data_top_states_user          

#Function to fetch Top districts user data from the database
def fetch_top_districts_user(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, Districts, Registered_user FROM Top_User_Districts WHERE Years=%s AND Quarter=%s ORDER BY Registered_user DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_districts_user = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Districts', 'Registered_user'])
    data_top_districts_user['Geo_States'] = map_states(data_top_districts_user['States'])
    data_top_districts_user['Districts'] = data_top_districts_user['Districts'].str.capitalize()
    data_top_districts_user["Converted_Registered_user"] = data_top_districts_user["Registered_user"].apply(convert_amount)
    data_top_districts_user = data_top_districts_user[['Districts', 'Registered_user', 'Converted_Registered_user']]
    close_connection(mysqldb, mycursor)
    return data_top_districts_user

# Function to create a horizontal bar chart
def create_horizontal_bar_chart(data, x_column, y_column, z_column, title, selected_year_quarter):
    # Create horizontal bar chart using Plotly Express
    fig = px.bar(data, x=z_column, y=x_column, orientation='h', text=y_column,
                 title=title,
                 color=z_column, color_continuous_scale=px.colors.diverging.Spectral,
                 category_orders={x_column: data.sort_values(by=z_column, ascending=False)[x_column]},
                 hover_data={z_column: False})  
    # Update layout settings for the chart
    fig.update_layout(xaxis_title=z_column, yaxis_title=x_column,
                      title=dict(text=f'{title} ({selected_year_quarter})', x=0.5, y=0.95, xanchor='center', yanchor='top'),width=1100,
                      margin=dict(l=50, r=50, t=50, b=50))  
    # Add color bar to the chart
    fig.update_layout(coloraxis_colorbar=dict(title=y_column, tickvals=[data[z_column].min(), data[z_column].mean(), data[z_column].max()]))  
    # Display the chart using Streamlit
    st.plotly_chart(fig)

# Visualize top states transaction count
def visualize_top_states_transaction_count(selected_year_quarter):
    # Fetch top data for states transaction count
    data_top_states_transaction_count = fetch_top_states_transaction_count(selected_year_quarter)
    # Create a horizontal bar chart for top states transaction count
    create_horizontal_bar_chart(data_top_states_transaction_count, "Geo_States", "Converted_Transaction_Count", "Total_Transaction_Count", "Top 10 States - Transaction Count", selected_year_quarter)
# Visualize top districts transaction count
def visualize_top_districts_transaction_count(selected_year_quarter):
    # Fetch top data for districts transaction count
    data_top_districts_transaction_count = fetch_top_districts_transaction_count(selected_year_quarter)
    # Create a horizontal bar chart for top districts transaction count
    create_horizontal_bar_chart(data_top_districts_transaction_count, "Districts", "Converted_Transaction_Count", "Transaction_count", "Top 10 Districts - Transaction Count", selected_year_quarter)
# Visualize top states transaction amount
def visualize_top_states_transaction_amount(selected_year_quarter):
    # Fetch top data for states transaction amount
    data_top_states_transaction_amount = fetch_top_states_transaction_amount(selected_year_quarter)
    # Create a horizontal bar chart for top states transaction amount
    create_horizontal_bar_chart(data_top_states_transaction_amount, "Geo_States", "Converted_Transaction_Amount", "Total_Transaction_Amount", "Top 10 States - Transaction Amount", selected_year_quarter)
# Visualize top districts transaction amount
def visualize_top_districts_transaction_amount(selected_year_quarter):
    # Fetch top data for districts transaction amount
    data_top_districts_transaction_amount = fetch_top_districts_transaction_amount(selected_year_quarter)
    # Create a horizontal bar chart for top districts transaction amount
    create_horizontal_bar_chart(data_top_districts_transaction_amount, "Districts", "Converted_Transaction_Amount", "Transaction_amount", "Top 10 Districts - Transaction Amount", selected_year_quarter)
# Visualize top states registered users
def visualize_top_states_user(selected_year_quarter):
    # Fetch top data for states registered users
    data_top_states_user = fetch_top_states_user(selected_year_quarter)
    # Create a horizontal bar chart for top states registered users
    create_horizontal_bar_chart(data_top_states_user, "Geo_States", "Converted_Registered_User", "Total_Registered_User", "Top 10 States - Registered Users", selected_year_quarter)
# Visualize top districts registered users                 
def visualize_top_districts_user(selected_year_quarter):
    # Fetch top data for districts registered users
    data_top_districts_user = fetch_top_districts_user(selected_year_quarter)
    # Create a horizontal bar chart for top districts registered users
    create_horizontal_bar_chart(data_top_districts_user, "Districts", "Converted_Registered_user", "Registered_user", "Top 10 Districts - Registered Users", selected_year_quarter)

#Function to fetch user brands percentage data from the database
def fetch_brands_user_percentage(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Brands, SUM(User_percentage) AS Total_User_Percentage FROM Aggregated_User WHERE Years=%s AND Quarter=%s GROUP BY Brands;"
    mycursor.execute(query, (Years, Quarter)) 
    data_states_user_percentage = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'Total_User_Percentage'])
    data_states_user_percentage["Converted_User_Percentage"] = data_states_user_percentage["Total_User_Percentage"].apply(convert_amount)
    data_states_user_percentage = data_states_user_percentage[['Brands', 'Total_User_Percentage', 'Converted_User_Percentage']]
    close_connection(mysqldb, mycursor)
    return data_states_user_percentage

#Function to fetch Top pincodes transaction count data from the database
def fetch_top_pincodes_transaction_count(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, Pincodes, Transaction_count FROM Top_Transaction_Pincodes WHERE Years=%s AND Quarter=%s ORDER BY Transaction_count DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_pincodes_transaction = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count'])
    data_top_pincodes_transaction["Converted_Transaction_Count"] = data_top_pincodes_transaction["Transaction_count"].apply(convert_amount)
    data_top_pincodes_transaction['Geo_States'] = map_states(data_top_pincodes_transaction['States'])
    data_top_pincodes_transaction['Pincodes'] = data_top_pincodes_transaction['Pincodes'].astype(str).str.replace(',', '')
    data_top_pincodes_transaction = data_top_pincodes_transaction[['Pincodes', 'Transaction_count', 'Converted_Transaction_Count']]
    close_connection(mysqldb, mycursor)
    return data_top_pincodes_transaction

#Function to fetch Top pincodes transaction amount data from the database
def fetch_top_pincodes_transaction_amount(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, Pincodes, Transaction_amount FROM Top_Transaction_Pincodes WHERE Years=%s AND Quarter=%s ORDER BY Transaction_amount DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_pincodes_transaction = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Pincodes', 'Transaction_amount'])
    data_top_pincodes_transaction["Converted_Transaction_Amount"] = data_top_pincodes_transaction["Transaction_amount"].apply(convert_amount)
    data_top_pincodes_transaction['Geo_States'] = map_states(data_top_pincodes_transaction['States'])
    data_top_pincodes_transaction['Pincodes'] = data_top_pincodes_transaction['Pincodes'].astype(str).str.replace(',', '')
    data_top_pincodes_transaction = data_top_pincodes_transaction[['Pincodes', 'Transaction_amount', 'Converted_Transaction_Amount']]
    close_connection(mysqldb, mycursor)
    return data_top_pincodes_transaction

#Function to fetch Top pincodes user data from the database
def fetch_top_pincodes_user(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT States, Years, Quarter, Pincodes, Registered_user FROM Top_User_Pincodes WHERE Years=%s AND Quarter=%s ORDER BY Registered_user DESC LIMIT 10;"
    mycursor.execute(query, (Years, Quarter))
    data_top_pincodes_user = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Years', 'Quarter', 'Pincodes', 'Registered_user'])
    data_top_pincodes_user['Geo_States'] = map_states(data_top_pincodes_user['States'])
    data_top_pincodes_user['Pincodes'] = data_top_pincodes_user['Pincodes'].astype(str).str.replace(',', '')    
    data_top_pincodes_user["Converted_Registered_user"] = data_top_pincodes_user["Registered_user"].apply(convert_amount)
    data_top_pincodes_user = data_top_pincodes_user[['Pincodes', 'Registered_user', 'Converted_Registered_user']]
    close_connection(mysqldb, mycursor)
    return data_top_pincodes_user

# Function to create a donut chart
def create_donut_chart(data, labels_column, values_column, hover_column, title, selected_year_quarter):
    # Create donut chart using Plotly Express
    fig = px.pie(data, names=labels_column, values=values_column, hole=0.4,
                 title=f'{title} ({selected_year_quarter})', color_discrete_sequence=px.colors.qualitative.Dark2,
                 hover_data={hover_column: True})   
    # Update layout settings for the chart
    fig.update_layout(showlegend=True, legend=dict(title=dict(text=labels_column)), width=1100)
    fig.update_layout(title=dict(x=0.5, y=0.9, xanchor='center', yanchor='top'))      
    # Display the chart using Streamlit
    st.plotly_chart(fig)

# Visualize user percentage by brands
def visualize_user_percentage_by_brands(selected_year_quarter):
    # Fetch data for user percentage by brands
    data_brands_user_percentage = fetch_brands_user_percentage(selected_year_quarter)
    # Create a donut chart for user percentage by brands
    create_donut_chart(data_brands_user_percentage,'Brands','Total_User_Percentage','Converted_User_Percentage','User Percentage by Brands',selected_year_quarter)
# Visualize top pincodes transaction count
def visualize_top_pincodes_transaction_count(selected_year_quarter):
    # Fetch top data for pincodes transaction count
    data_top_pincodes_transaction_count = fetch_top_pincodes_transaction_count(selected_year_quarter)
    # Create a donut chart for top pincodes transaction count
    create_donut_chart(data_top_pincodes_transaction_count, "Pincodes", "Transaction_count", "Converted_Transaction_Count", "Top 10 Pincodes - Transaction Count", selected_year_quarter)
# Visualize top pincodes transaction amount
def visualize_top_pincodes_transaction_amount(selected_year_quarter):
    # Fetch top data for pincodes transaction amount
    data_top_pincodes_transaction_amount = fetch_top_pincodes_transaction_amount(selected_year_quarter)
    # Create a donut chart for top pincodes transaction amount
    create_donut_chart(data_top_pincodes_transaction_amount, "Pincodes", "Transaction_amount", "Converted_Transaction_Amount", "Top 10 Pincodes - Transaction Amount", selected_year_quarter)
# Visualize top pincodes registered users
def visualize_top_pincodes_user(selected_year_quarter):
    # Fetch top data for pincodes registered users
    data_top_pincodes_user = fetch_top_pincodes_user(selected_year_quarter)
    # Create a donut chart for top pincodes registered users
    create_donut_chart(data_top_pincodes_user, "Pincodes", "Registered_user", "Converted_Registered_user", "Top 10 Pincodes - Registered Users", selected_year_quarter)

#Function to fetch PhonePe Transactions data from the database
def fetch_all_phonepe_transactions(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Years, Quarter, SUM(Transaction_count) AS Total_Transaction_Count FROM Aggregated_Transaction WHERE Years=%s AND Quarter=%s;"
    mycursor.execute(query, (Years, Quarter))
    data_all_phonepe_transactions = pd.DataFrame(mycursor.fetchall(), columns=['Years', 'Quarter', 'Total_Transaction_Count'])
    data_all_phonepe_transactions["All Phonepe Transactions"] = data_all_phonepe_transactions["Total_Transaction_Count"].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data_all_phonepe_transactions

#Function to fetch Total Payment Value data from the database
def fetch_total_payment_value(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Years, Quarter, SUM(Transaction_amount) AS Total_Transaction_Amount FROM Aggregated_Transaction WHERE Years=%s AND Quarter=%s;"
    mycursor.execute(query, (Years, Quarter))
    data_total_payment_value = pd.DataFrame(mycursor.fetchall(), columns=['Years', 'Quarter', 'Total_Transaction_Amount'])
    data_total_payment_value['Total_Payment_Value'] = data_total_payment_value["Total_Transaction_Amount"].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data_total_payment_value

#Function to fetch Average Transaction Value data from the database
def fetch_avg_transaction_value(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Years, Quarter, AVG(Transaction_amount) AS Transaction_Value FROM Aggregated_Transaction WHERE Years = %s AND Quarter = %s;"
    mycursor.execute(query, (Years, Quarter)) 
    data_avg_transaction_value = pd.DataFrame(mycursor.fetchall(), columns=['Years', 'Quarter', 'Transaction_Value'])
    data_avg_transaction_value['Avg_Transaction_Value'] = data_avg_transaction_value["Transaction_Value"].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data_avg_transaction_value

#Function to fetch Transaction type value data from the database
def fetch_transaction_type_value(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Years, Quarter, Transaction_type, SUM(Transaction_amount) AS Total_Transaction_Amount FROM Aggregated_Transaction WHERE Years=%s AND Quarter=%s GROUP BY Transaction_type;"
    mycursor.execute(query, (Years, Quarter))
    data_transaction_type_value = pd.DataFrame(mycursor.fetchall(), columns=['Years', 'Quarter','Transaction_type', 'Total_Transaction_Amount'])
    data_transaction_type_value["Transactions"] = data_transaction_type_value["Total_Transaction_Amount"].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data_transaction_type_value

#Function to fetch registered users data from the database
def fetch_registered_users(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Years, Quarter, SUM(Registered_user) AS Total_Registered_Users FROM Map_User WHERE Years=%s AND Quarter=%s;"
    mycursor.execute(query, (Years, Quarter))
    data_registered_users = pd.DataFrame(mycursor.fetchall(), columns=['Years', 'Quarter','Total_Registered_Users'])
    data_registered_users["Registered_Users"] = data_registered_users["Total_Registered_Users"].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data_registered_users

#Function to fetch app opens data from the database
def fetch_app_opens(selected_year_quarter):
    mysqldb, mycursor = create_connection()
    df_geo_states = load_geojson_data()
    Years = int(selected_year_quarter[:4]) 
    Quarter = selected_year_quarter[6:]
    query = "SELECT Years, Quarter, SUM(App_opens) AS Total_App_opens FROM Map_User WHERE Years=%s AND Quarter=%s;"
    mycursor.execute(query, (Years, Quarter))
    data_app_opens = pd.DataFrame(mycursor.fetchall(), columns=['Years', 'Quarter','Total_App_opens'])
    data_app_opens["App_opens"] = data_app_opens["Total_App_opens"].apply(convert_amount)
    close_connection(mysqldb, mycursor)
    return data_app_opens

# Function to fetch and download reports data based on selected year and category
def fetch_download_reports_data(selected_year_quarter, category_selection):
    # Establish a connection to the MySQL database
    mysqldb, mycursor = create_connection()  
    # Load geographical data
    df_geo_states = load_geojson_data()    
    # Extract year and quarter from the selected string
    Years = int(selected_year_quarter[:4])
    Quarter = selected_year_quarter[6:]
    
    # Initialize variables
    report_dataframes = {}
    tables_names = []  
    queries = []
    download_button = False

    if category_selection == "Transactions":
        st.write("Note: The download button will generate CSV files for each table according to the selected Year & Quarter.")
        if st.button("Generate Report"):
            # SQL queries for transaction-related data
            queries = ["SELECT States, Years, Quarter, Transaction_type, SUM(Transaction_count) as Total_Transaction_count, SUM(Transaction_amount) as Total_Transaction_amount FROM Aggregated_Transaction WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Transaction_type;",
                       "SELECT States, Years, Quarter, Districts, SUM(Transaction_count) as Total_Transaction_count, SUM(Transaction_amount) as Total_Transaction_amount FROM Map_Transaction WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Districts;",
                       "SELECT States, Years, Quarter, Districts, SUM(Transaction_count) as Total_Transaction_count, SUM(Transaction_amount) as Total_Transaction_amount FROM Top_Transaction_Districts WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Districts;",
                       "SELECT States, Years, Quarter, Pincodes, SUM(Transaction_count) as Total_Transaction_count, SUM(Transaction_amount) as Total_Transaction_amount FROM Top_Transaction_Pincodes WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Pincodes;"]  
            tables_names = ["Aggregated_Transaction", "Map_Transaction", "Top_Transaction_Districts", "Top_Transaction_Pincodes"]
            download_button = True
    elif category_selection == "Users":
        st.write("Note: The download button will generate CSV files for each table according to the selected Year & Quarter.")
        if st.button("Generate Report"):
            # SQL queries for user-related data
            queries = ["SELECT States, Years, Quarter, Brands, SUM(User_count) as Total_User_count, SUM(User_percentage) as Total_User_percentage FROM Aggregated_User WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Brands;",
                       "SELECT States, Years, Quarter, Districts, SUM(Registered_user) as Total_Registered_user, SUM(App_opens) as Total_App_opens FROM Map_User WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Districts;",
                       "SELECT States, Years, Quarter, Districts, SUM(Registered_user) as Total_Registered_user FROM Top_User_Districts WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Districts;",
                       "SELECT States, Years, Quarter, Pincodes, SUM(Registered_user) as Total_Registered_user FROM Top_User_Pincodes WHERE Years=%s AND Quarter=%s GROUP BY States, Years, Quarter, Pincodes;"]            
            tables_names = ["Aggregated_User", "Map_User", "Top_User_Districts", "Top_User_Pincodes"]
            download_button = True
    # Execute SQL queries and save results to CSV files
    for i, (query, table_name) in enumerate(zip(queries, tables_names)):
        mycursor.execute(query, (Years, Quarter))
        column_names = [desc[0] for desc in mycursor.description]
        result_df = pd.DataFrame(mycursor.fetchall(), columns=column_names)
        # Save DataFrame to CSV with the corresponding table name
        result_df.to_csv(f'{table_name} {selected_year_quarter}.csv', index=False)
    # Close the MySQL connection
    close_connection(mysqldb, mycursor)    
    # Display success message if download button is clicked and process done
    if download_button:
        st.success("Download complete! Check your PhonePe folder for the CSV files.")    
    return report_dataframes, tables_names

# Function to display the PhonePe dashboard
def dashboard_creation():
    # Split the layout into two columns
    col1, col2 = st.columns(2) 
    # Column 1: Visualization and selection options
    with col1:
        # Display PhonePe Pulse image
        local_image_path = r"C:\Users\Hp\Desktop\PhonePe_Pulse\PhonePe_Pulse.jpg"
        image = Image.open(local_image_path)
        st.image(image, width=500)
        # Selection options for category, year, and quarter
        st.markdown("<h4>ALL INDIA</h4>", unsafe_allow_html=True)
        st.text("")
        col1_1, col1_2, col1_3 = st.columns(3)
        category_selection = col1_1.selectbox("Select Category", ["Transactions", "Users"])
        selected_year = col1_2.selectbox("Select Year", [2018, 2019, 2020, 2021, 2022, 2023])
        selected_quarter = col1_3.selectbox("Select Quarter", ["Q1", "Q2", "Q3", "Q4"])
        selected_year_quarter = f"{selected_year} {selected_quarter}"  # Combining the selected Year and Quarter
        # Calling the function to download the reports
        fetch_download_reports_data(selected_year_quarter, category_selection)
        # Display visualizations based on selected category and options
        if category_selection == "Transactions":
            # Display info for unavailable data
            st.info("Data for the year and quarter '2023 Q4' is not available yet, as this quarter has not yet been completed.")
            option = st.radio('Select an option', ['Transaction Count', 'Transaction Amount'], horizontal=True)
            if option == 'Transaction Count':
                # Visualizations for Transaction Count
                create_transaction_count_choropleth(selected_year_quarter)
                # Inserting a horizontal rule to create a visual separation in the dashboard
                st.markdown("<hr style='margin-top: 30px; margin-bottom: 30px;'>", unsafe_allow_html=True)
                visualize_transaction_type_count(selected_year_quarter)
                # Additional options for filtering by states
                geo_states_list = load_geojson_data()
                selected_states = st.multiselect("Select States", geo_states_list, default=['Kerala', 'Tamil Nadu'])
                visualize_districts_transaction_count(selected_year_quarter, selected_states)
                # Additional visualizations
                visualize_top_states_transaction_count(selected_year_quarter)
                visualize_top_districts_transaction_count(selected_year_quarter)
                visualize_top_pincodes_transaction_count(selected_year_quarter)
            if option == 'Transaction Amount':
                # Visualizations for Transaction Amount
                create_transaction_amount_choropleth(selected_year_quarter)
                # Inserting a horizontal rule to create a visual separation in the dashboard
                st.markdown("<hr style='margin-top: 30px; margin-bottom: 30px;'>", unsafe_allow_html=True)
                visualize_transaction_type_amount(selected_year_quarter)
                # Additional options for filtering by states
                geo_states_list = load_geojson_data()
                selected_states = st.multiselect("Select States", geo_states_list, default=['Kerala', 'Tamil Nadu'])
                visualize_districts_transaction_amount(selected_year_quarter, selected_states)
                # Additional visualizations
                visualize_top_states_transaction_amount(selected_year_quarter)
                visualize_top_districts_transaction_amount(selected_year_quarter)
                visualize_top_pincodes_transaction_amount(selected_year_quarter)
        if category_selection == "Users":
            # Display info for unavailable data
            st.info("User Count & User Percentage data for the period '2022 Q2' to '2023 Q4' is not available. Additionally, data for the year '2023 Q4' is not available as this quarter has not yet been completed.")
            option = st.radio('Select an option', ['User Count', 'Registered Users', 'App Opens'], horizontal=True)
            if option == 'User Count':
                # Visualizations for User Count
                create_user_count_choropleth(selected_year_quarter)
                # Inserting a horizontal rule to create a visual separation in the dashboard
                st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
                visualize_user_percentage_by_brands(selected_year_quarter)
                visualize_user_brand_count(selected_year_quarter)
            if option == 'Registered Users':
                # Visualizations for Registered Users
                create_registered_user_count_choropleth(selected_year_quarter)
                # Inserting a horizontal rule to create a visual separation in the dashboard
                st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
                # Additional options for filtering by states
                geo_states_list = load_geojson_data()
                selected_states = st.multiselect("Select States", geo_states_list, default=['Kerala', 'Tamil Nadu'])
                visualize_districts_registered_users(selected_year_quarter, selected_states)
                # Additional visualizations
                visualize_top_states_user(selected_year_quarter)
                visualize_top_districts_user(selected_year_quarter)
                visualize_top_pincodes_user(selected_year_quarter)
            if option == 'App Opens':
                # Visualizations for App Opens
                create_app_opens_count_choropleth(selected_year_quarter)
                # Inserting a horizontal rule to create a visual separation in the dashboard
                st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
                # Additional options for filtering by states
                geo_states_list = load_geojson_data()
                selected_states = st.multiselect("Select States", geo_states_list, default=['Kerala', 'Tamil Nadu'])
                visualize_districts_app_opens(selected_year_quarter, selected_states)
    # Column 2: Display additional information and statistics
    with col2:
        if category_selection == "Transactions":
            # Display Transaction information
            st.markdown("<h4 style='text-align: center;'>Transactions</h4>", unsafe_allow_html=True)
            # Display All Phonepe Transactions value
            st.markdown(f"<h5 style='text-align: center;'>All PhonePe transactions (UPI + Cards + Wallets) in {selected_year_quarter}</h5>", unsafe_allow_html=True)
            data_all_phonepe_transactions = fetch_all_phonepe_transactions(selected_year_quarter)
            all_phonepe_transactions = data_all_phonepe_transactions["All Phonepe Transactions"].tolist()
            display = all_phonepe_transactions[0]
            st.write(f"<h5 style='text-align: center;'>{display}</h5>", unsafe_allow_html=True)

            col2_1, col2_2 = st.columns(2)
            with col2_1:
                # Display Total payment value
                st.markdown(f"<h5>Total payment value in {selected_year_quarter}</h5>", unsafe_allow_html=True)
                data_total_payment_value = fetch_total_payment_value(selected_year_quarter)
                total_payment_value = data_total_payment_value["Total_Payment_Value"].tolist()
                display = total_payment_value[0]
                st.write(f"<h5 style='text-align: center;'>₹{display}</h5>", unsafe_allow_html=True)
            with col2_2:
                # Display Avg. transaction value
                st.markdown(f"<h5>Avg. transaction value in {selected_year_quarter}</h5>", unsafe_allow_html=True)
                data_avg_transaction_value = fetch_avg_transaction_value(selected_year_quarter)
                avg_transaction_value = data_avg_transaction_value["Avg_Transaction_Value"].tolist()
                display = avg_transaction_value[0]
                st.write(f"<h5 style='text-align: center;'>₹{display}</h5>", unsafe_allow_html=True)
            # Inserting a horizontal rule to create a visual separation in the dashboard
            st.markdown("<hr style='margin-top: 0; margin-bottom: 0;'>", unsafe_allow_html=True)
            # Display Transaction Type information
            data_transaction_type_value = fetch_transaction_type_value(selected_year_quarter)
            st.markdown(f"<h5>Categories in {selected_year_quarter}</h5>", unsafe_allow_html=True)
            for index, category in enumerate(["Merchant payments", "Peer-to-peer payments", "Recharge & bill payments", "Financial Services", "Others"]):
                display_value = data_transaction_type_value["Transactions"].iloc[index]
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<h5>{category}</h5>", unsafe_allow_html=True)
                with col2:
                    st.write(f"<h5 style='text-align: center;'>₹{display_value}</h5>", unsafe_allow_html=True)
            # Inserting a horizontal rule to create a visual separation in the dashboard
            st.markdown("<hr style='margin-top: 0; margin-bottom: 0;'>", unsafe_allow_html=True)
            # Display Top States, Districts, and Pincodes
            col2_3, col2_4, col2_5 = st.columns(3)
            with col2_3:
                st.markdown("<h5 style='text-align: center;'>States</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: center;'>Top 10 States</h6>", unsafe_allow_html=True)
                if option == 'Transaction Amount':
                    data_top_states_transaction = fetch_top_states_transaction_amount(selected_year_quarter)
                    st.write(data_top_states_transaction["Geo_States"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
                else:
                    data_top_states_transaction = fetch_top_states_transaction_count(selected_year_quarter)
                    st.write(data_top_states_transaction["Geo_States"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
            with col2_4:
                st.markdown("<h5 style='text-align: center;'>Districts</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: center;'>Top 10 Districts</h6>", unsafe_allow_html=True)
                if option == 'Transaction Amount':
                    data_top_districts_transaction = fetch_top_districts_transaction_amount(selected_year_quarter)
                    st.write(data_top_districts_transaction["Districts"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
                else:
                    data_top_districts_transaction = fetch_top_districts_transaction_count(selected_year_quarter)
                    st.write(data_top_districts_transaction["Districts"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
            with col2_5:
                st.markdown("<h5 style='text-align: center;'>Pincodes</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: center;'>Top 10 Pincodes</h6>", unsafe_allow_html=True)
                if option == 'Transaction Amount':
                    data_top_pincodes_transaction = fetch_top_pincodes_transaction_amount(selected_year_quarter)
                    st.write(data_top_pincodes_transaction["Pincodes"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
                else:
                    data_top_pincodes_transaction = fetch_top_pincodes_transaction_count(selected_year_quarter)
                    st.write(data_top_pincodes_transaction["Pincodes"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
        if category_selection == "Users":
            # Display User information
            st.markdown("<h4 style='text-align: center;'>Users</h4>", unsafe_allow_html=True)
            # Display Registered Phonepe Users value
            st.markdown(f"<h5 style='text-align: center;'>Registered Phonepe Users in {selected_year_quarter}</h5>", unsafe_allow_html=True)
            data_registered_users = fetch_registered_users(selected_year_quarter)
            registered_users = data_registered_users["Registered_Users"].tolist()
            display = registered_users[0]
            st.write(f"<h5 style='text-align: center;'>{display}</h5>", unsafe_allow_html=True)
            # Display Phonepe app opens value
            st.markdown(f"<h5 style='text-align: center;'>Phonepe app opens in {selected_year_quarter}</h5>", unsafe_allow_html=True)
            data_app_opens = fetch_app_opens(selected_year_quarter)
            app_opens = data_app_opens["App_opens"].tolist()
            display = app_opens[0]
            st.write(f"<h5 style='text-align: center;'>{display}</h5>", unsafe_allow_html=True)
            st.markdown("<hr style='margin-top: 0; margin-bottom: 0;'>", unsafe_allow_html=True)
            # Display Top States, Districts, and Pincodes for Users
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                st.markdown("<h5 style='text-align: center;'>States</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: center;'>Top 10 States</h6>", unsafe_allow_html=True)
                data_top_states_user = fetch_top_states_user(selected_year_quarter)
                st.write(data_top_states_user["Geo_States"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
            with col2_2:
                st.markdown("<h5 style='text-align: center;'>Districts</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: center;'>Top 10 Districts</h6>", unsafe_allow_html=True)
                data_top_districts_user = fetch_top_districts_user(selected_year_quarter)
                st.write(data_top_districts_user["Districts"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))
            with col2_3:
                st.markdown("<h5 style='text-align: center;'>Pincodes</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: center;'>Top 10 Pincodes</h6>", unsafe_allow_html=True)
                data_top_pincodes_user = fetch_top_pincodes_user(selected_year_quarter)
                st.write(data_top_pincodes_user["Pincodes"].iloc[:10].reset_index(drop=True).rename(lambda x: x + 1))

#Function to display data in transaction summary
def transaction_summary():
    # Transaction Insights Report
    st.markdown("<h4 style='text-align: center;'>Transaction Insights</h4>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 5px; margin-bottom: 5px;'>", unsafe_allow_html=True)
    # Overview and Observations
    st.markdown("<h5>Observations</h5>", unsafe_allow_html=True)
    st.write("After a comprehensive analysis of transaction data from PhonePe Pulse, several key observations have been identified.,")
    st.markdown("""
    - **Dashboard display:** These are the values displayed, All PhonePe Transactions, Total payment value, Average Transaction value and categories of all the transaction types.
    - **All INDIA-Performance:** Implemented Choropleth MapBox for analysis with the highest transaction volume & growth over States.
    - **Top-Performing States:** Highlighted top 10 states with the highest transaction volume & growth, visualized using Horizontal Bar Charts.
    - **Top-Performing Districts & Pincodes:** Highlighted top 10 districts & pincodes with the highest transaction volume & growth, visualized using Horizontal Bar Chart & Donut Chart.
    - **Popular Transaction Types:** Identified the most popular transaction types based on transaction count & amount, visualized using Bar Chart.
    - **District-Wise Trends:** Provided insights into districts based on the transactions with respective to the States input, visualized using Line Chart.
    """)
    st.write("All these analysis were done based on the particular year and quarter choosen from the options to have better understanding over period of time.")
    # Suggestions for Transaction Improvement
    st.markdown("<h5>Transaction Improvement Suggestions</h5>", unsafe_allow_html=True)
    st.write("Based on the observations and in general, here are few strategic suggestions to enhance transaction performance.,")
    st.markdown("""
    - **Promote High-Performing Regions:** Tailor promotions to regional preferences, collaborate with local businesses, etc to maintain the performance stable.
    - **Address Challenges in Low-Performing States:** Provide actionable strategies to overcome challenges in states with lower transaction rates.
    - **Optimize Transaction Types:** Recommend optimizing transaction types, promoting high-performing ones, and improving less popular ones.
    - **District-Wise Strategies:** Tailor promotional activities to districts, considering local factors and preferences.
    - **Improve Transaction Security:** Reinforce security measures, educate users, and build trust in digital transactions.
    - **Explore New Transaction Avenues:** Explore emerging transaction avenues, partnerships, or technologies.
    - **Geo-Specific Promotions:** Design region-specific promotions based on geographical data.
    - **Diversify Transaction Channels:** Encourage users to explore various transaction channels, highlighting their benefits.
    - **Leverage Social Media:** Utilize social media platforms to promote transactions and build a community around digital transactions.
    """)
    # Conclusion
    st.markdown("<h5>Conclusion</h5>", unsafe_allow_html=True)
    st.write("In conclusion, the analysis of transaction data from PhonePe Pulse offers valuable insights into regional variations, transaction type distribution and transaction patterns. The suggested strategies aim to enhance overall transaction performance.")

#Function to display data in users summary
def user_summary():
    # User Insights Report
    st.markdown("<h4 style='text-align: center;'>User Insights</h4>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 5px; margin-bottom: 5px;'>", unsafe_allow_html=True)
    # Overview and Observations
    st.markdown("<h5>Observations</h5>", unsafe_allow_html=True)
    st.write("After a comprehensive analysis of user data from PhonePe Pulse, several key observations have been identified.,")
    st.markdown("""
    - **Dashboard display:** These are the values displayed, Registered users and App opens.
    - **All INDIA-Performance:** Implemented Choropleth MapBox for analysis with the user count and engagement over States.
    - **Top-Performing States:** Highlighted top 10 states with the user count and engagement, visualized using Horizontal Bar Charts.
    - **Top-Performing Districts & Pincodes:** Highlighted top 10 districts & pincodes with the user count and engagement, visualized using Horizontal Bar Chart & Donut Chart.
    - **Popular User Brands:** Identified the most popular smartphone brands based on user registrations, visualized using Bar Chart.
    - **District-Wise User Trends:** Provided insights into districts with the most and least registered users, visualized using Line Chart.
    """)
    st.write("All these analysis were done based on the particular year and quarter choosen from the options to have better understanding over period of time.")
    # Suggestions for User Improvement
    st.markdown("<h5>User Improvement Suggestions</h5>", unsafe_allow_html=True)
    st.write("Based on the observations and in general, here are few strategic suggestions to enhance user engagement.,")
    st.markdown("""
    - **Personalized Recommendations:** Implement personalized recommendations based on user behavior and preferences. Provide users with tailored suggestions for transactions, offers, and app features.
    - **User Engagement Patterns:** Discuss user engagement trends, loyalty, and app opening patterns.
    - **Challenges in Low-Performing Regions:** Discuss challenges faced by states with lower user registrations and app openings, Tailor marketing and engagement campaigns to regions.
    - **Optimize User Brands:** Promote popular smartphone brands through targeted campaigns and partnerships.
    - **Enhance User Engagement:** Develop engagement programs, loyalty initiatives, and strategies to increase app openings.
    - **Diversify User Engagement Channels:** Encourage users to explore various app features and engagement channels.
    - **Interactive Tutorials:** Create interactive tutorials or guides within the app to help users discover and understand various features. Simplify complex functionalities and encourage users to explore through step-by-step guidance.
    - **Feedback Mechanism:** Establish a robust feedback mechanism to gather insights directly from users. Act on user feedback to address concerns, improve existing features, and introduce new functionalities.
    - **Community Forums:** Introduce community forums or discussion boards within the app to foster user interaction. Encourage users to share tips, ask questions, and connect with each other.
    """)
    # Conclusion
    st.markdown("<h5>Conclusion</h5>", unsafe_allow_html=True)
    st.write("In conclusion, the analysis of user data from PhonePe Pulse offers valuable insights into user behavior, brand preferences and engagement patterns. The suggested strategies aim to enhance overall user engagement and satisfaction.")

#Function to display data in about session - Project Overview
def project_overview():
    # Display project overview title
    st.markdown("<h4 style='text-align: center;'>Project Overview</h4>", unsafe_allow_html=True)
    # Display project details
    st.markdown("**Title:** PhonePe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly")
    st.markdown("**Objective:** Develop a user-friendly data visualization tool using Streamlit and Plotly to explore and analyze data from the PhonePe Pulse Github repository.")
    # Display technologies used
    st.markdown("<h4>Technologies Used</h4>", unsafe_allow_html=True)
    st.write("- Github Cloning")
    st.write("- Python")
    st.write("- Pandas")
    st.write("- MySQL")
    st.write("- Streamlit")
    st.write("- Plotly")
    # Display domain
    st.markdown("<h4>Domain</h4>", unsafe_allow_html=True)
    st.write("Fintech")
    # Display problem statement
    st.markdown("<h4>Problem Statement</h4>", unsafe_allow_html=True)
    st.write("The PhonePe Pulse Github repository contains a vast amount of data related to various metrics and statistics. The challenge is to extract, process, and visualize this data to provide valuable insights in a user-friendly manner.")
    # Display approach
    st.markdown("<h4>Approach</h4>", unsafe_allow_html=True)
    st.write("*1. Data Extraction*")
    st.write("- Cloned the Github repository using scripting to fetch data from PhonePe Pulse.")
    st.write("- Stored data in a suitable format.")
    st.write("*2. Data Transformation*")
    st.write("- Utilized Python and Pandas to manipulate and preprocess the data.")
    st.write("- Handled cleaning, missing values, and transform data for analysis.")
    st.write("*3. Database Insertion*")
    st.write("- Connected to a MySQL database using 'mysql-connector-python.'")
    st.write("- Inserted transformed data using SQL commands.")
    st.write("*4. Dashboard Creation*")
    st.write("- Using Streamlit and Plotly in Python to create an interactive and visually appealing dashboard.")
    st.write("- Leverage Plotly's geo map functions for geographical visualizations.")
    st.write("- Implemented multiple dropdown options for users.")
    st.write("*5. Data Retrieval*")
    st.write("- Connected to the MySQL database using 'mysql-connector-python.'")
    st.write("- Fetched data from Pandas dataframe.")
    st.write("- Dynamically updated the dashboard with the latest data.")
    st.write("*6. Deployment*")
    st.write("- Ensure a secure, efficient, and user-friendly solution.")
    st.write("- Thoroughly tested the solution before deploying the dashboard publicly.")
    # Display learning outcomes
    st.markdown("<h4>Learning Outcomes</h4>", unsafe_allow_html=True)
    st.write("1. **Data Extraction and Processing:** Learn to clone Github repository, extract data, and preprocess it using Pandas.")
    st.write("2. **Database Management:** Understand relational database usage (MySQL) for efficient data storage and retrieval.")
    st.write("3. **Visualization and Dashboard Creation:** Gain expertise in creating interactive dashboards using Streamlit and Plotly.")
    st.write("4. **Geo Visualization:** Learn to create and display data on a map using Plotly's geo map functions.")
    st.write("5. **Dynamic Updating:** Implement dashboards that dynamically update based on the latest data.")
    st.write("6. **Project Development and Deployment:** Learn to develop a comprehensive, user-friendly solution—from data extraction to dashboard deployment. Test and deploy securely and efficiently.")
    # Display result
    st.markdown("<h4>Result</h4>", unsafe_allow_html=True)
    st.write("The project delivers a live geo visualization dashboard, offering interactive and visually appealing insights from the PhonePe Pulse Github repository. With a minimum of 10 dropdown options, users can select various facts and figures for display. Data stored in a MySQL database ensures efficient retrieval and dynamic updates on the dashboard.")
    # Display dataset link and source inspiration
    st.markdown("**Dataset Link:** [Data Link](https://github.com/PhonePe/pulse#readme)")
    st.markdown("**Inspired From:** [PhonePe Pulse](https://www.phonepe.com/pulse/)")
    st.markdown("*Note: For access to the dataset and additional information, please follow the provided hyperlinks.*")

#Function to display data in about session - Data Insights
def data_insights():
    # Display welcome message and download links
    st.markdown("<h4 style='text-align: center;'>Welcome to the PhonePe Pulse Application!</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Explore and Visualize data related to PhonePe Transactions, Users & more.</h4>", unsafe_allow_html=True)
    st.write("Download the PhonePe app to experience seamless transactions:")
    st.markdown("[Download PhonePe App](https://play.google.com/store/apps/details?id=com.phonepe.app)")
    st.write("Visit the official website for more information:")
    st.markdown("[PhonePe Official Website](https://www.phonepe.com/)")
    st.markdown("<h4 style='text-align: center;'>PhonePe Pulse Data-Insights</h4>", unsafe_allow_html=True)
    # Display process options
    process = ['1-Key Dimensions', '2-Aggregated Transaction', '3-Aggregated User', '4-Map Transaction', '5-Map User', '6-Top Transaction', '7-Top User']
    selected_process = st.selectbox('Please select the option below:', process, index=0)
    st.write(f'You have selected the option: {selected_process}')
    # Display details based on selected process
    if selected_process == '1-Key Dimensions':
        st.write('- States - All the States in India')
        st.write('- Years -  [2018 to 2023]')
        st.write('- Quarter - Q1 (Jan to Mar), Q2 (Apr to June), Q3 (July to Sep), Q4 (Oct to Dec)')
    if selected_process == '2-Aggregated Transaction':
        st.write('Transaction data includes the following Transaction types:')
        st.write('- Recharge & bill payments')
        st.write('- Peer-to-peer payments')
        st.write('- Merchant payments')
        st.write('- Financial Services')
        st.write('- Others')
    if selected_process == '3-Aggregated User':
        st.write('Users data includes the following Brands:')
        brands_list = ['Apple', 'Asus', 'Coolpad', 'Gionee', 'HMD Global',
                   'Huawei', 'Infinix', 'Lava', 'Lenovo', 'Lyf',
                   'Micromax', 'Motorola', 'OnePlus', 'Oppo', 'Realme',
                   'Samsung', 'Tecno', 'Vivo', 'Xiaomi', 'Others']
        brands_columns = [brands_list[i:i + 5] for i in range(0, len(brands_list), 5)]
        cols = st.columns(4)
        for i, brand_column in enumerate(brands_columns):
            with cols[i]:
                for brand in brand_column:
                    st.write(f":star: {brand}")
    if selected_process == '4-Map Transaction':
        st.write('- Number of transactions mapped at the state and district levels')
        st.write('- Total values of mapped transactions at the state and district levels')
    if selected_process == '5-Map User':
        st.write('- Number of registered users mapped at both state and district levels')
        st.write('- Mapped count of app openings by the registered users at both state and district levels')
    if selected_process == '6-Top Transaction':
        st.write('- Top 10 States with the most transaction')
        st.write('- Top 10 Districts with the most transaction')
        st.write('- Top 10 Pincodes with the most transaction')
    if selected_process == '7-Top User':
        st.write('- Top 10 States with the most registered user')
        st.write('- Top 10 Districts with the most registered user')
        st.write('- Top 10 Pincodes with the most registered user') 

# Function to display information about the application
def display_about():
    # Display application title
    st.markdown("<h2 style='text-align: center;'>PhonePe Pulse Data Visualization and Exploration</h2>", unsafe_allow_html=True)
    # Options for the user to choose
    process = ['Project Overview', 'Data-Insights']
    options = st.selectbox('Please select the option below:', process, index=0)
    st.write(f'You have selected the option: {options}')     
    # Handle selected option
    if options == 'Project Overview':
        project_overview()
    elif options == 'Data-Insights':
        data_insights() 

# Function to display summary information
def display_summary():
    # Display application title
    st.markdown("<h4 style='text-align: center;'>PhonePe Pulse: Summary and Strategic Insights Report</h4>", unsafe_allow_html=True)
    # Options for the user to choose
    process = ['Transactions', 'Users']
    options = st.selectbox('Please select the option below:', process, index=0)
    st.write(f'You have selected the option: {options}')     
    # Handle selected option
    if options == 'Transactions':
        transaction_summary()
    elif options == 'Users':
        user_summary()

# Function to display exit information
def display_exit():
    st.subheader("Exit Application")
    st.markdown("Thank you for using the PhonePe Pulse Data Visualization and Exploration application.")
    st.markdown("If you wish to exit, simply close the browser tab or window.")
    st.markdown("Have a great day!")

# Get user input for page selection
page = st.sidebar.selectbox("Select Page", ["About", "Dashboard", "Summary", "Exit"])

# Main section to display different pages
def main():
    if page == "About":
        display_about()
    elif page == "Dashboard":
        dashboard_creation()
    elif page == "Summary":
        display_summary()
    elif page == "Exit":
        display_exit()

# Call the main function to display the appropriate content based on the selected page
main() 
