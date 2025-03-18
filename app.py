# pylint: disable=missing-module-docstring

from datetime import timedelta, date, datetime

import duckdb
import streamlit as st
import ast
import os
import logging

# Vérifions que la donnée existe
if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("No data folder found! Creating data folder ...")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    logging.error("No duckdb database file found! Creating the database file ...")
    exec(
        open("init_db.py").read()
    )  # C'est un truc de hackeur mais on le fait car subprocess ne marche pas bien avec streamlit
    # subprocess.run(["python", "init_db.py"])
    logging.info("Data initialized")



def check_users_solution(user_query: str):
    """
    Check the users solution with the solution given in the exercise by:
    1: check the number of columns
    2: check the number of lines
    3: check the content of the columns

    :param user_query:
    :return:
    """
    # Votre Résultat
    st.write("Your Result:")
    result = con.execute(user_query).df()
    st.dataframe(result)
    if len(result.columns) != len(solution_df.columns):
        st.sidebar.write(":red[Error:] the number of columns is not the same")
    n_diff_lines = result.shape[0] - solution_df.shape[0]
    if n_diff_lines != 0:
        st.sidebar.write(
            f"Result has :red[{n_diff_lines}] lines differents from the solution"
        )
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).empty:
            st.sidebar.success(":green[Congratulations, you have a correct result]")
            st.balloons()
        else:
            st.sidebar.write(":red[Error:] the content of the columns is not the same")

    except KeyError as e:
        st.sidebar.write(":red[Some columns are missing in the result]")


st.title("SQL SRS Applications - Exercises")
st.write(
    "Welcome to the SQL SRS Applicatiosn - Exercises. Please select a thematic to work on."
)
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

#Lister uniquement les thématiques disponibles

availabble_theme_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
my_options = availabble_theme_df['theme'].unique()

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review",
        my_options,
        index=None,
        placeholder="Select a thematic to work on ...",
    )
    st.write(f"You selected: {theme}")
    if theme:
        exercise = (
            con.execute(
                f"SELECT theme, exercise_name, tables, last_reviewed FROM memory_state WHERE theme = '{theme}' ORDER BY last_reviewed ASC"
            )
            .df()
            .reset_index(drop=True)
        )  # On pouvait faire df().sort_values("last_reviewed")
        st.write(exercise)


if theme in my_options:
    input_query = st.text_area("Please enter your SQL query here :")
    button_validation = st.button("Validate your query")

    exercise_name = exercise.loc[
        0, "exercise_name"
    ]  # Récupérer première ligne de la colonne qui nous intéresse
    with open(f"answers/{exercise_name}.sql", "r") as f:
        ANSWER_STR = f.read()
    solution_df = con.execute(ANSWER_STR).df()

    for n_days in [2, 7, 21]:
        if st.button(f"Review again in {n_days} days"):
            next_review = date.today() + timedelta(days=n_days)
            st.write(f"Next review: {next_review}")
            con.execute(
                f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
            )
            st.rerun()

    if st.button("Reset"):
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '1970-01-01' WHERE theme = '{theme}'"
        )
        st.rerun() #Permet de rerun tout le code dès le début pour au en live afficher les changements dans les tables.

    tab1, tab2 = st.tabs(["Tables", "Solution"])

    with tab1:
        #    exercise_tables = ast.literal_eval(exercise.loc[0, 'tables'])
        exercise_tables = exercise.loc[0, "tables"]
        st.write(f"Tables: {exercise_tables}")
        for table in exercise_tables:
            st.write(f"Table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)
    with tab2:
        st.text(ANSWER_STR)

    # Resultats
    if button_validation:
        try:
            check_users_solution(input_query)
        except AttributeError as e:
            st.warning("Please enter a valid SQL query !!")

        # Résultat Attendu
        st.write("Expected Result:")
        st.dataframe(solution_df)

else:
    st.warning("Please select a correct theme !!")
