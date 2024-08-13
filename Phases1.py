import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # Import pyplot submodule
import seaborn as sns
import mysql.connector
from sqlalchemy import create_engine

# Title of the web app
st.title("Phases")

# Option to select data source: CSV or Database
data_source = st.selectbox("Select Data Source", ["Upload CSV", "Connect to Database"])

# Load data from CSV
if data_source == "Upload CSV":
    # File uploader to allow users to upload a CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

# Load data from Database
elif data_source == "Connect to Database":
    # Database connection details
    MYSQL_HOST = "sailing-performance.artemisracing.com"
    MYSQL_PORT = 3306
    MYSQL_USR = "admin"
    MYSQL_PWD = "Vh&bxj07oiFNFP;Jg+BZ"
    MYSQL_SCHEMA = "ac40"

    try:
        # Create a connection to the database
        engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USR}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_SCHEMA}")
        
        # Query to fetch data
        query = "SELECT * FROM ac40.stats_phases;"
        
        # Read the data into a DataFrame
        st.session_state[df] = pd.read_sql(query, engine)
        
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

if 'df' in locals():
    # Convert the 'dateTimeUtc' column to datetime format
    df = st.session_state[df].copy()
    df['dateTimeUtc'] = pd.to_datetime(df['dateTimeUtc'])

    # Display the DataFrame (optional)
    st.write("Data Preview:")
    st.write(df)

    # Get a list of unique dates for multiselect
    unique_dates = df['dateTimeUtc'].dt.date.unique()
    unique_dates.sort()  # Sort dates for better user experience

    # Multi-select widget for selecting multiple dates
    selected_dates = st.multiselect("Select dates", options=unique_dates, default=unique_dates)

    # Filtering DataFrame based on selected dates
    if selected_dates:
        filtered_df = df[df['dateTimeUtc'].dt.date.isin(selected_dates)]
    else:
        filtered_df = df

    # Sliders for 'tws' and 'vmg'
    TWS = st.slider("TWS", min_value=8, max_value=20, value=(8, 20))
    vmg = st.slider("VMG%", min_value=0.8, max_value=1.5, value=(0.8, 1.5))
    
    # Dropdown for selecting upwind or downwind
    mode = st.selectbox("Select Mode", options=["UP", "DN"])

    # Filter the DataFrame based on the slider values and mode selection
    filtered_df = filtered_df[(filtered_df['TWS'] >= TWS[0]) & (filtered_df['TWS'] <= TWS[1]) & 
                             (filtered_df['VMG%'] >= vmg[0]) & (filtered_df['VMG%'] <= vmg[1]) & 
                             (filtered_df['mode'] == mode)]

    # Drop down menus for selecting variables
    variables = filtered_df.columns.tolist()
    x_var = st.selectbox("Select X variable", variables)
    y_var = st.selectbox("Select Y variable", variables)

    # Drop down for the interpolation
    order = int(st.selectbox("Select interpolation", options=["1","2","3","4","5","6"], index=1))

    # Ensure that both x_var and y_var are defined before proceeding
    if x_var and y_var:
        # Create the lmplot using seaborn without the hue parameter
        plot = sns.lmplot(data=filtered_df, x=x_var, y=y_var, order=order)

        # Display the plot using Streamlit
        st.pyplot(plot.fig)
