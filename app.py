import io
from operator import index

import streamlit as st
import pandas as pd
import duckdb

st.write("""
# SQL SRS 
Spaced Repetition System SQL practice
""")
my_options = ["Joins", "GroupBY","CTE","SubQueries" "Windows Function"]
with st.sidebar:
    option = st.selectbox("What would you like to review",
                          my_options,
                          index= None,
                          placeholder = "Select a thematic to work on ...")
if option in my_options:
    data = {"a":[1, 2, 3], "b":[4, 5, 6]}
    df = pd.DataFrame(data)

    input_query = st.text_area("Veuillez saisir votre requête SQL:")
    if st.button("Valider la requête"):
        result = duckdb.query(query=input_query).df()
        st.dataframe(result)
else:
    st.warning("Please select a correct theme !!")
