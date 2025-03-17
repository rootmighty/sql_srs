import io

import streamlit as st
import pandas as pd
import duckdb


csv1 = '''
beverage,price
orange juice,1.99
coffee,2.99
tea,1.99
water,0.99
'''

beverages = pd.read_csv(io.StringIO(csv1))

csv2 = '''
food_items, food_price
cookies, 1.99
pizza, 2.99
pasta, 1.99
salad, 1.99
sandwiches, 1.99
sushi, 2.99
steak, 2.99
meat, 2.99
vegetables, 1.99'''

food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.query(query=answer).df()

input_query = st.text_area(label="Veuillez saisir votre requête SQL:", key="user_input")
if st.button("Valider la requête"):
    result = duckdb.query(query=input_query).df()
    st.dataframe(result)
tab1, tab2 = st.tabs(["Tables","Solution"])

with tab1:
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution)
with tab2:
    st.write(answer)

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


