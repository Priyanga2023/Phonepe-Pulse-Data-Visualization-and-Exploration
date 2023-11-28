# Import necessary Python packages
import os
import git
import json
import pandas as pd
import mysql.connector 
import streamlit as st
import plotly.express as px
import time
import requests

def github_cloning():
    # Clone the repository
    git.Repo.clone_from("https://github.com/PhonePe/pulse.git",'pulse')

# Set Streamlit page configuration
st.set_page_config(page_title="Phonepe", layout="wide")

#aggregated_transaction
def aggregated_transaction():
    path=r"C:\Users\Hp\Desktop\Phonepe\pulse\data\aggregated\transaction\country\india\state"
    agg_state_trans=os.listdir(path)
    
    Agg_trans={'States':[],'Years':[],'Quarter':[],'Transaction_type':[],'Transaction_count':[],'Transaction_amount':[]}
    
    for state in agg_state_trans:
        present_state=os.path.join(path,state)
        agg_year_trans=os.listdir(present_state)
    
        for year in agg_year_trans:
            present_year=os.path.join(present_state,year)
            agg_json_trans=os.listdir(present_year)
    
            for file in agg_json_trans:
                json_file_path=os.path.join(present_year,file)
    
                with open(json_file_path, "r") as data:
                    json_data = json.load(data) 
            
                for i in json_data["data"]["transactionData"]:
                    Name=i["name"]
                    Count=i["paymentInstruments"][0]["count"]
                    Amount=i["paymentInstruments"][0]["amount"]
                    Agg_trans["States"].append(state)
                    Agg_trans["Years"].append(year)
                    Agg_trans["Quarter"].append(int(file.strip('.json'))) 
                    Agg_trans["Transaction_type"].append(Name)
                    Agg_trans["Transaction_count"].append(Count)
                    Agg_trans["Transaction_amount"].append(Amount)

    return Agg_trans

#aggregated_user
def aggregated_user():
    path = r"C:\Users\Hp\Desktop\Phonepe\pulse\data\aggregated\user\country\india\state"
    agg_state_user = os.listdir(path)

    Agg_user = {'States': [], 'Years': [], 'Quarter': [], 'Brands': [], 'User_count': [], 'User_percentage': []}

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

#map_transaction
def map_transaction():
    path=r"C:\Users\Hp\Desktop\Phonepe\pulse\data\map\transaction\hover\country\india\state"
    map_state_trans=os.listdir(path)
    
    Map_trans={'States':[],'Years':[],'Quarter':[],'Districts':[],'Transaction_count':[],'Transaction_amount':[]}
    
    for state in map_state_trans:
        present_state=os.path.join(path,state)
        map_year_trans=os.listdir(present_state)
    
        for year in map_year_trans:
            present_year=os.path.join(present_state,year)
            map_json_trans=os.listdir(present_year)
    
            for file in map_json_trans:
                json_file_path=os.path.join(present_year,file)
    
                with open(json_file_path, "r") as data:
                    json_data=json.load(data) 
                    
                for i in json_data["data"]["hoverDataList"]:
                    Name=i["name"]
                    Count=i["metric"][0]["count"]
                    Amount=i["metric"][0]["amount"]
                    Map_trans["States"].append(state)
                    Map_trans["Years"].append(year)
                    Map_trans["Quarter"].append(int(file.strip('.json'))) 
                    Map_trans["Districts"].append(Name)
                    Map_trans["Transaction_count"].append(Count)
                    Map_trans["Transaction_amount"].append(Amount) 

    return Map_trans

#map_user
def map_user():
    path=r"C:\Users\Hp\Desktop\Phonepe\pulse\data\map\user\hover\country\india\state"
    map_state_user=os.listdir(path)
    
    Map_user={'States':[],'Years':[],'Quarter':[],"Districts":[],"Registered_user":[],"App_opens":[]}
    
    for state in map_state_user:
        present_state=os.path.join(path,state)
        map_year_user=os.listdir(present_state)
    
        for year in map_year_user:
            present_year=os.path.join(present_state,year)
            map_json_user=os.listdir(present_year)
    
            for file in map_json_user:
                json_file_path=os.path.join(present_year,file)
                
                with open(json_file_path, "r") as data:
                    json_data=json.load(data) 
                    
                    for district,data in json_data["data"]["hoverData"].items():
                        Name=district
                        Registered_user=data["registeredUsers"]
                        App_opens=data["appOpens"]
                        Map_user["States"].append(state)
                        Map_user["Years"].append(year)
                        Map_user["Quarter"].append(int(file.strip('.json'))) 
                        Map_user["Districts"].append(Name)
                        Map_user["Registered_user"].append(Registered_user)
                        Map_user["App_opens"].append(App_opens) 

    return Map_user

#top_transaction_pincodes
def top_transaction_pincodes():
    path=r"C:\Users\Hp\Desktop\Phonepe\pulse\data\top\transaction\country\india\state"
    top_state_trans=os.listdir(path)
    
    Top_trans_pin={'States':[],'Years':[],'Quarter':[],'Pincodes':[],'Transaction_count':[],'Transaction_amount':[]}
    
    for state in top_state_trans:
        present_state=os.path.join(path,state)
        top_year_trans=os.listdir(present_state)
    
        for year in top_year_trans:
            present_year=os.path.join(present_state,year)
            top_json_trans=os.listdir(present_year)
    
            for file in top_json_trans:
                json_file_path=os.path.join(present_year,file)
    
                with open(json_file_path, "r") as data:
                    json_data=json.load(data) 
                    
                for i in json_data["data"]["pincodes"]:
                    Name=i["entityName"]
                    Count=i['metric']['count']
                    Amount=i['metric']['amount']
                    Top_trans_pin["States"].append(state)
                    Top_trans_pin["Years"].append(year)
                    Top_trans_pin["Quarter"].append(int(file.strip('.json'))) 
                    Top_trans_pin["Pincodes"].append(Name)
                    Top_trans_pin["Transaction_count"].append(Count)
                    Top_trans_pin["Transaction_amount"].append(Amount) 

    return Top_trans_pin

#top_transaction_districts
def top_transaction_districts():
    path=r"C:\Users\Hp\Desktop\Phonepe\pulse\data\top\transaction\country\india\state"
    top_state_trans=os.listdir(path)
    
    Top_trans_dist={'States':[],'Years':[],'Quarter':[],'Districts':[],'Transaction_count':[],'Transaction_amount':[]}
    
    for state in top_state_trans:
        present_state=os.path.join(path,state)
        top_year_trans=os.listdir(present_state)
    
        for year in top_year_trans:
            present_year=os.path.join(present_state,year)
            top_json_trans=os.listdir(present_year)
    
            for file in top_json_trans:
                json_file_path=os.path.join(present_year,file)
    
                with open(json_file_path, "r") as data:
                    json_data=json.load(data) 
                    
                for i in json_data["data"]["districts"]:
                    Name=i["entityName"]
                    Count=i['metric']['count']
                    Amount=i['metric']['amount']
                    Top_trans_dist["States"].append(state)
                    Top_trans_dist["Years"].append(year)
                    Top_trans_dist["Quarter"].append(int(file.strip('.json'))) 
                    Top_trans_dist["Districts"].append(Name)
                    Top_trans_dist["Transaction_count"].append(Count)
                    Top_trans_dist["Transaction_amount"].append(Amount) 

    return Top_trans_dist

#top_user_pincodes
def top_user_pincodes():
    path=r"C:\Users\Hp\Desktop\Phonepe\pulse\data\top\user\country\india\state"
    top_state_user=os.listdir(path)
    
    Top_user_pin={'States':[],'Years':[],'Quarter':[],'Pincodes':[],'Registered_user':[]}
    
    for state in top_state_user:
        present_state=os.path.join(path,state)
        top_year_user=os.listdir(present_state)
    
        for year in top_year_user:
            present_year=os.path.join(present_state,year)
            top_json_user=os.listdir(present_year)
    
            for file in top_json_user:
                json_file_path=os.path.join(present_year,file)
                
                with open(json_file_path, "r") as data:
                    json_data=json.load(data) 
                
                for i in json_data["data"]["pincodes"]:
                        Name=i['name']
                        Registered_user=i['registeredUsers']
                        Top_user_pin["States"].append(state)
                        Top_user_pin["Years"].append(year)
                        Top_user_pin["Quarter"].append(int(file.strip('.json'))) 
                        Top_user_pin["Pincodes"].append(Name)
                        Top_user_pin["Registered_user"].append(Registered_user) 

    return Top_user_pin

#top_user_districts
def top_user_districts():
    path=r"C:\Users\Hp\Desktop\Phonepe\pulse\data\top\user\country\india\state"
    top_state_user=os.listdir(path)
    
    Top_user_dist={'States':[],'Years':[],'Quarter':[],'Districts':[],'Registered_user':[]}
    
    for state in top_state_user:
        present_state=os.path.join(path,state)
        top_year_user=os.listdir(present_state)
    
        for year in top_year_user:
            present_year=os.path.join(present_state,year)
            top_json_user=os.listdir(present_year)
    
            for file in top_json_user:
                json_file_path=os.path.join(present_year,file)
                
                with open(json_file_path, "r") as data:
                    json_data=json.load(data) 
                
                for i in json_data["data"]["districts"]:
                        Name=i['name']
                        Registered_user=i['registeredUsers']
                        Top_user_dist["States"].append(state)
                        Top_user_dist["Years"].append(year)
                        Top_user_dist["Quarter"].append(int(file.strip('.json'))) 
                        Top_user_dist["Districts"].append(Name)
                        Top_user_dist["Registered_user"].append(Registered_user) 

    return Top_user_dist

# Function to perform data transformation
def data_transformation():
    # Perform data extraction
    Agg_trans = aggregated_transaction()
    Agg_user = aggregated_user()
    Map_trans = map_transaction()
    Map_user = map_user()
    Top_trans_pincodes = top_transaction_pincodes()
    Top_trans_districts = top_transaction_districts()
    Top_user_pincodes = top_user_pincodes()
    Top_user_districts = top_user_districts()

    # Create DataFrames
    df_aggregated_transaction = pd.DataFrame(Agg_trans)
    df_aggregated_user = pd.DataFrame(Agg_user)
    df_map_transaction = pd.DataFrame(Map_trans)
    df_map_user = pd.DataFrame(Map_user)
    df_top_transaction_pincodes = pd.DataFrame(Top_trans_pincodes)
    df_top_transaction_districts = pd.DataFrame(Top_trans_districts)
    df_top_user_pincodes = pd.DataFrame(Top_user_pincodes)
    df_top_user_districts = pd.DataFrame(Top_user_districts)

    return df_aggregated_transaction, df_aggregated_user,df_map_transaction, df_map_user,df_top_transaction_pincodes, df_top_transaction_districts,df_top_user_pincodes, df_top_user_districts

# Function to create a connection to the MySQL database
def create_connection():
    mysqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        port="3306",
        database="Phonepe_pulse")
    
    # Create a cursor object for MySQL operations
    mycursor = mysqldb.cursor(buffered=True)

    return mysqldb, mycursor

def drop_tables(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS Aggregated_Transaction, Aggregated_User, Map_Transaction, Map_User, Top_Transaction_Pincodes, Top_Transaction_Districts, Top_User_Pincodes, Top_User_Districts")
           
# Define the SQL query to create the table if it doesn't exist
def create_tables(mycursor):
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Aggregated_Transaction (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Transaction_type VARCHAR(50),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE
    )
    """)
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Aggregated_User (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Brands VARCHAR(50),
        User_count BIGINT,
        User_percentage DOUBLE
    )
    """)   
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Map_Transaction (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Districts VARCHAR(50),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE
    )
    """)
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Map_User (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Districts VARCHAR(50),
        Registered_user BIGINT,
        App_opens BIGINT
    )
    """)
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Top_Transaction_Pincodes (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Pincodes INT,
        Transaction_count BIGINT,
        Transaction_amount DOUBLE
    )
    """)
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Top_Transaction_Districts (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Districts VARCHAR(50),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE
    )
    """)
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Top_User_Pincodes (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Pincodes INT,
        Registered_user BIGINT
    )
    """)
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Top_User_Districts (
        States VARCHAR(50),
        Years INT,
        Quarter TINYINT CHECK (Quarter >= 1 AND Quarter <= 4),
        Registered_user BIGINT
    )
    """) 

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
    query = "INSERT INTO Top_User_Districts(States, Years, Quarter, Registered_user) VALUES (%s, %s, %s, %s)"
    values_top_user_districts = df_top_user_districts[['States', 'Years', 'Quarter', 'Registered_user']].values.tolist()
    mycursor.executemany(query, values_top_user_districts)

def close_connection(mysqldb, mycursor):
    # Commit changes and close the connection
    mysqldb.commit()
    mycursor.close()
    mysqldb.close()

def data_insertion_sql():
    # Create a connection
    mysqldb, mycursor = create_connection()
    # Drop tables
    drop_tables(mycursor)
    # Perform data transformation
    df_aggregated_transaction, df_aggregated_user, df_map_transaction, df_map_user, df_top_transaction_pincodes, df_top_transaction_districts, df_top_user_pincodes, df_top_user_districts = data_transformation()
    # Create tables
    create_tables(mycursor)
    # Insert values
    insert_values(mycursor, df_aggregated_transaction, df_aggregated_user, df_map_transaction, df_map_user, df_top_transaction_pincodes, df_top_transaction_districts, df_top_user_pincodes, df_top_user_districts)
    # Close the connection
    close_connection(mysqldb, mycursor)

def convert_amount(value):
    # Convert the value to a string and replace commas if present
    amount_str = str(value).replace(',', '')

    # Convert the string to a float and format it
    amount = float(amount_str)

    if amount < 1000:
        return str(int(amount))
    elif amount < 100000:
        return '{:.2f}K'.format(amount / 1000)
    elif amount < 10000000:
        return '{:.2f}L'.format(amount / 100000)
    elif amount < 1000000000:
        return '{:.2f}Cr'.format(amount / 10000000)
    elif amount < 1000000000000:
        return '{:.2f}B'.format(amount / 1000000000)
    else:
        return '{:.2f}T'.format(amount / 1000000000000)

def execute_query(query, params=None):
    mysqldb, mycursor = create_connection()
    mycursor.execute(query, params)
    result = mycursor.fetchall()
    close_connection(mysqldb, mycursor)
    return result

def fetch_data_and_convert(query, column_names):
    result = execute_query(query)
    data = pd.DataFrame(result, columns=column_names)
    return data

def load_geojson_data():
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(geojson_url)
    geo_data = json.loads(response.content)
    geo_states = [i['properties']['ST_NM'] for i in geo_data['features']]
    geo_states.sort(reverse=False)
    df_geo_states = pd.DataFrame({"States": geo_states})
    
    return df_geo_states

def aggregated_transaction_amount_by_states():
        query = """SELECT States, sum(Transaction_amount) as 'Total Transaction Amount'
               FROM Aggregated_Transaction
               GROUP BY States
               ORDER BY States ASC;"""
        column_names = ['States', 'Total Transaction Amount']
        data = fetch_data_and_convert(query, column_names)
        data['States'] = df_geo_states['States']
        data = data.sort_values(by='Total Transaction Amount', ascending=False)
        data['Converted Values'] = data['Total Transaction Amount'].apply(convert_amount)

        return data

def chropleth_map_trans_amount():
    load_geojson_data()
    call_func = aggregated_transaction_amount_by_states()
    df = pd.DataFrame(call_func)  
    
    px.set_mapbox_access_token("pk.eyJ1IjoicHJpeWFuZ2EwNzAzIiwiYSI6ImNscGUzYWxqcDE0ZngyamxzNnplZmRoNXQifQ.2PF095gqVqidmrdam8F9TA")
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    fig = px.choropleth_mapbox(
    df,
    geojson=geojson_url,
    featureidkey='properties.ST_NM',
    locations='States',
    color='Total Transaction Amount',
    hover_data=['Total Transaction Amount'],  
    mapbox_style='mapbox://styles/mapbox/satellite-streets-v11',
    title="Aggregated Transaction Amount across States",
    center={'lat': 20.5937, 'lon': 78.9629},
    zoom=4,
    opacity=0.9,
    color_continuous_scale="tealrose")
    fig.update_layout(coloraxis_colorbar=dict(title='Total Transaction Amount'))
    st.plotly_chart(fig, use_container_width=True)

def phonepe_analysis():
    st.subheader("Phonepe Pulse Dashboard")
    process = ['States', 'Years', 'Quater','Districts', 'Transaction Types', 'User Brands', 'Top 10 Analysis']
    options = st.selectbox('Please select the option below:', process,index=0)
    if options == 'States':
        st.write(f'You have selected the option: {options}')
    
        tab1, tab2 = st.tabs(['Transaction', 'User'])
        with tab1:
            chropleth_map_trans_amount()
        with tab2:
            st.write("")

def project_overview():
    st.subheader("Project Overview")

    st.markdown("**Title:** Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly")
    st.markdown("**Objective:** Develop a user-friendly data visualization tool using Streamlit and Plotly to explore and analyze data from the Phonepe Pulse Github repository.")

    st.subheader("Technologies Used")
    st.write("- Github Cloning")
    st.write("- Python")
    st.write("- Pandas")
    st.write("- MySQL")
    st.write("- Streamlit")
    st.write("- Plotly")

    st.subheader("Domain")
    st.write("Fintech")

    st.subheader("Problem Statement")
    st.write("The Phonepe Pulse Github repository contains a vast amount of data related to various metrics and statistics. The challenge is to extract, process, and visualize this data to provide valuable insights in a user-friendly manner.")

    st.subheader("Approach")

    st.write("*1. Data Extraction*")
    st.write("- Cloned the Github repository using scripting to fetch data from Phonepe Pulse.")
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

    st.subheader("Results")
    st.write("The project delivers a live geo visualization dashboard, offering interactive and visually appealing insights from the Phonepe Pulse Github repository. With a minimum of 10 dropdown options, users can select various facts and figures for display. Data stored in a MySQL database ensures efficient retrieval and dynamic updates on the dashboard.")

    st.markdown("**Dataset Link:** [Data Link](https://github.com/PhonePe/pulse#readme)")
    st.markdown("**Inspired From:** [PhonePe Pulse](https://www.phonepe.com/pulse/)")

    st.subheader("Learning Outcomes")
    st.write("1. **Data Extraction and Processing:** Learn to clone Github repository, extract data, and preprocess it using Pandas.")
    st.write("2. **Database Management:** Understand relational database usage (MySQL) for efficient data storage and retrieval.")
    st.write("3. **Visualization and Dashboard Creation:** Gain expertise in creating interactive dashboards using Streamlit and Plotly.")
    st.write("4. **Geo Visualization:** Learn to create and display data on a map using Plotly's geo map functions.")
    st.write("5. **Dynamic Updating:** Implement dashboards that dynamically update based on the latest data.")
    st.write("6. **Project Development and Deployment:** Learn to develop a comprehensive, user-friendly solution—from data extraction to dashboard deployment. Test and deploy securely and efficiently.")

    st.markdown("*Note: For access to the dataset and additional information, please follow the provided hyperlinks.*")

def data_insights():
    st.subheader("Welcome to the PhonePe Pulse Application!")
    st.subheader("Explore and Visualize data related to PhonePe Transactions, Users & more.")
    st.write("Download the PhonePe app to experience seamless transactions:")
    st.markdown("[Download PhonePe App](https://play.google.com/store/apps/details?id=com.phonepe.app)")

    st.write("Visit the official website for more information:")
    st.markdown("[PhonePe Official Website](https://www.phonepe.com/)")

    st.subheader("PhonePe Pulse Data-Insights") 

    process = ['','1-Key Dimensions','2-Aggregated Transaction','3-Aggregated User','4-Map Transaction','5-Map User','6-Top Transaction','7-Top User']
    selected_process = st.selectbox('Please select the option below:',process,index=0)
    if selected_process == '':
        st.write("")
    else:
        st.write(f'You have selected the option: {selected_process}')

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

def display_about():
    st.header("Phonepe Pulse Data Visualization and Exploration")
    process=['','Project Overview','Data-Insights']
    options=st.selectbox('Please select the option below:', process,index=0)
    if options == '':
        st.write("")
    else:
        st.write(f'You have selected the option: {options}')
    if options == 'Project Overview':
        project_overview()
    if options == 'Data-Insights':
        data_insights()

# Function to display information about the project
def dashboard_creation():
    st.header("Phonepe Pulse Data Visualization and Exploration")
    process = ['','1-Data Extraction','2-Data Migration','3-Data Analysis & Visualization']
    selected_process = st.selectbox('Please select the option below:',process,index=0)
    if selected_process == '':
        st.write("")
    else:
        st.write(f'You have selected the option: {selected_process}')
    if selected_process == "1-Data Extraction":
        folder_name = "pulse" 
        if os.path.isdir(folder_name):
            time.sleep(4) 
            st.success('Phonepe Pulse data successfully cloned from the Git repository')
        else:
            git_cloning() 
            st.success('Phonepe Pulse data successfully cloned from the Git repository')

    if selected_process == "2-Data Migration":
        st.info("Migrating Phonepe Pulse data to MySQL Database 'Phonepe_pulse'")
        migrate_button = st.button("Migrate data")
        if migrate_button:
            # List of table names to check for existence
            table_names = ['Aggregated_Transaction', 'Aggregated_User', 'Map_Transaction', 'Map_User', 'Top_Transaction_Pincodes', 'Top_Transaction_Districts', 'Top_User_Pincodes', 'Top_User_Districts']
        
            # Check if any of the tables exist
            table_exists_query = "SHOW TABLES LIKE %s"
            data_inserted = False
        
            for table_name in table_names:
                table_exists = execute_query(table_exists_query, (table_name,))
                if not table_exists:
                    data_insertion_sql()
                    data_inserted = True
                
            if data_inserted:
                st.success('Phonepe Pulse data successfully migrated to the SQL Database')
            else:
                time.sleep(4)
                st.success('Phonepe Pulse data already exists in the SQL Database')

    if selected_process == "3-Data Analysis & Visualization":
        phonepe_analysis()

def display_exit():
    st.subheader("Exit Application")
    st.markdown("Thank you for using the Phonepe Pulse Data Visualization and Exploration application.")
    st.markdown("If you wish to exit, simply close the browser tab or window.")
    st.markdown("Have a great day!")

# Get user input for page selection
page = st.sidebar.selectbox("Select Page", ["About", "Dashboard", "Exit"])

# Main section to display different pages
def main():
    if page == "About":
        display_about()
    elif page == "Dashboard":
        dashboard_creation()
    elif page == "Exit":
        display_exit()

# Call the main function to display the appropriate content based on the selected page
main()    