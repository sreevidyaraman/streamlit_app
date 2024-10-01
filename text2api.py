import streamlit as st
import pandas as pd

number = st.slider("Pick a number", 0, 100)
st.write("Values:", number)
