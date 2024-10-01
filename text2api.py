import streamlit as st
import pandas as pd


number = st.slider("Pick a number", 0, 100)
st.write("Values:", number)



df = pd.DataFrame({
    'Title': ['User Story', 'Priority'],
    'SN1': [0, 0, 0],
    'SN2': [0, 0, 0]
})

