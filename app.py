# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

CSV_1 = """
beverage,price
orange juice,1.99
coffee,2.99
tea,1.99
"""

beverages = pd.read_csv(io.StringIO(CSV_1))

CSV_2 = """
food_items,food_price
cookies, 1.99
pizza, 2.99
pasta, 1.99
"""

food_items = pd.read_csv(io.StringIO(CSV_2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.query(query=ANSWER_STR).df()

input_query = st.text_area("Veuillez saisir votre requête SQL:")

my_options = ["Joins", "GroupBY", "CTE", "SubQueries", "Windows Function"]
with st.sidebar:
    option = st.selectbox(
        "What would you like to review",
        my_options,
        index=None,
        placeholder="Select a thematic to work on ...",
    )
if option in my_options:

    if st.button("Valider la requête"):
        result = duckdb.query(query=input_query).df()
        st.dataframe(result)

        if len(result.columns) != len(solution_df.columns):
            st.write("Error: the number of columns is not the same")

        n_diff_lines = result.shape[0] - solution_df.shape[0]
        if n_diff_lines != 0:
            st.write(f"Result has {n_diff_lines} lines differents from the solution")

        try:
            result = result[solution_df.columns]
            st.dataframe(result.compare(solution_df))
        except KeyError as e:
            st.write("Some columns are missing in the result")

    tab1, tab2 = st.tabs(["Tables", "Solution"])

    with tab1:
        st.write("Table: beverages")
        st.dataframe(beverages)
        st.write("Table: food_items")
        st.dataframe(food_items)
        st.write("Expected:")
        st.dataframe(solution_df)
    with tab2:
        st.write(ANSWER_STR)

else:
    st.warning("Please select a correct theme !!")
