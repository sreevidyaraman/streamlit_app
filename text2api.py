import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'Title': ['User Story', 'Priority'],
    'SN1': [0, 0, 0],
    'SN2': [0, 0, 0]
})

#    'Title': ['User Story', 'Priority', 'Uploaded', 'Valide', 'Invalid', 'Incomplete', 'Variants', 'Typo', 'Total'],



# Getting user input
input_A = st.number_input('User Story 1', value=0.0)
input_B = st.number_input('User Story 2', value=0.0)

# Update dataframe with user input
df.at[0, 'SN1'] = input_A
df.at[1, 'SN2'] = input_B

# Display the updated dataframe
st.table(df.set_index('Title'))


number = st.slider("Pick a number", 0, 100)
st.write("Values:", number)