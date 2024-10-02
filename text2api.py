import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

number = st.slider("Pick a number", 0, 100)
st.write("Values:", number)

# Sample data to display in the table
data = {
    'Name': ['John', 'Jane', 'Doe'],
    'Age': [28, 34, 45],
    'Occupation': ['Engineer', 'Doctor', 'Artist']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Configure the editable grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)  # Make all columns editable
gb.configure_column("Age", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], editable=True)

# Final Grid options
grid_options = gb.build()

# Create the editable table
st.write("### Editable User Input Table")
response = AgGrid(
    df,
    gridOptions=grid_options,
    editable=True,  # Enable cell editing
    fit_columns_on_grid_load=True,
    theme="streamlit",  # Add a Streamlit theme to the grid
)

# Display the updated data
st.write("### Updated Data:")
st.write(response['data'])  # Display updated data after user input


# Blue banner with white text using HTML and CSS
st.markdown("""
    <style>
    .blue-banner {
        background-color: #1E90FF;  /* DodgerBlue color */
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        font-family: Arial, sans-serif;
    }
    .blue-banner h1 {
        color: white;
        font-size: 24px;
        margin: 0;
    }
    </style>
    
    <div class="blue-banner">
        <h1>Welcome to My Streamlit App</h1>
    </div>
""", unsafe_allow_html=True)
