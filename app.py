# pylint: disable=missing-module-docstring

import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

#solution_df = duckdb.query(query=ANSWER_STR).df()

input_query = st.text_area("Veuillez saisir votre requête SQL:")

my_options = ["CrossJoins", "GroupBy", "CTE", "SubQueries", "Window_Functions"]
with st.sidebar:
    theme = st.selectbox(
        "What would you like to review",
        my_options,
        index=None,
        placeholder="Select a thematic to work on ...",
    )
    st.write(f"You selected: {theme}")
    if theme:
        exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
        st.write(exercise)

#if option in my_options:
#
#    if st.button("Valider la requête"):
#        result = duckdb.query(query=input_query).df()
#        st.dataframe(result)
#
#        if len(result.columns) != len(solution_df.columns):
#            st.write("Error: the number of columns is not the same")
#
#        n_diff_lines = result.shape[0] - solution_df.shape[0]
#        if n_diff_lines != 0:
#            st.write(f"Result has {n_diff_lines} lines differents from the solution")
#
#        try:
#            result = result[solution_df.columns]
#            st.dataframe(result.compare(solution_df))
#        except KeyError as e:
#            st.write("Some columns are missing in the result")
#
#    tab1, tab2 = st.tabs(["Tables", "Solution"])
#
#    with tab1:
#        st.write("Table: beverages")
#        st.dataframe(beverages)
#        st.write("Table: food_items")
#        st.dataframe(food_items)
#        st.write("Expected:")
#        st.dataframe(solution_df)
#    with tab2:
#        st.write(ANSWER_STR)
#
#else:
#    st.warning("Please select a correct theme !!")
