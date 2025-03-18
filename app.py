# pylint: disable=missing-module-docstring

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
    input_query = st.text_area("Veuillez saisir votre requête SQL:")
    button_validation = st.button("Valider la requête")

    exercise_name = exercise.loc[
        0, "exercise_name"
    ]  # Récupérer première ligne de la colonne qui nous intéresse
    with open(f"answers/{exercise_name}.sql", "r") as f:
        ANSWER_STR = f.read()
    solution_df = con.execute(ANSWER_STR).df()

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
            # Votre Résultat
            st.write("Your Result:")
            result = con.execute(input_query).df()
            st.dataframe(result)

            if len(result.columns) != len(solution_df.columns):
                st.write("Error: the number of columns is not the same")

            n_diff_lines = result.shape[0] - solution_df.shape[0]
            if n_diff_lines != 0:
                st.write(
                    f"Result has {n_diff_lines} lines differents from the solution"
                )

            try:
                result = result[solution_df.columns]
                st.dataframe(result.compare(solution_df))
            except KeyError as e:
                st.write("Some columns are missing in the result")

        except AttributeError as e:
            st.warning("Please enter a valid SQL query !!")

        # Résultat Attendu
        st.write("Expected Result:")
        st.dataframe(solution_df)

else:
    st.warning("Please select a correct theme !!")
