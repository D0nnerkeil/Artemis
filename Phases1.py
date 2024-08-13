import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # Import pyplot submodule
import numpy as np
import seaborn as sns

# Title of the web app
st.title("Phases")

# File uploader to allow users to upload a CSV file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame (optional)
    st.write("Data Preview:")
    st.write(df)

    # Sliders for 'tws' and 'vmg'
    TWS = st.slider("TWS", min_value=8, max_value=20, value=(8, 20))
    vmg = st.slider("VMG%", min_value=0.8, max_value=1.0, value=(0.8, 1.0))
    
    # Dropdown for selecting upwind or downwind
    mode = st.selectbox("Select Mode", options=["UP", "DN"])

    # Filter the DataFrame based on the slider values and mode selection
    filtered_df = df[(df['TWS'] >= TWS[0]) & (df['TWS'] <= TWS[1]) & 
                     (df['VMG%'] >= vmg[0]) & (df['VMG%'] <= vmg[1]) & 
                     (df['mode'] == mode)]

    # Drop down menus for selecting variables
    variables = df.columns.tolist()
    x_var = st.selectbox("Select X variable", variables)
    y_var = st.selectbox("Select Y variable", variables)

    # Ensure that both x_var and y_var are defined before proceeding
    if x_var and y_var:
        # Create the lmplot using seaborn without the hue parameter
        plot = sns.lmplot(data=filtered_df, x=x_var, y=y_var, order=2)

        # Display the plot using Streamlit
        st.pyplot(plot.fig)