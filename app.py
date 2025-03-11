from operator import index

import streamlit as st
import pandas as pd
import duckdb

st.write("""
# SQL SRS 
Spaced Repetition System SQL practice
""")

option = st.selectbox("What would you like to review",
                      ["Joins", "GroupBY","CTE","SubQueries" "Windows Function"],
                      index= None,
                      placeholder = "Select a thematic to work on ...")
if option:
    data = {"a":[1, 2, 3], "b":[4, 5, 6]}
    df = pd.DataFrame(data)

    input_query = st.text_area("Veuillez saisir votre requête SQL:")
    if st.button("Valider la requête"):
        result = duckdb.query(query=input_query).df()
        st.dataframe(result)