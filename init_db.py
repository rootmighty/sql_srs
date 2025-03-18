import io

import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
# -------------------------------------------------------------------
# EXERCISES LIST
# ===================================================================

data = {
    "theme": ["CrossJoins", "CrossJoins"],
    "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["1980-01-01", "1970-01-01"],
}

memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# --------------------------------------------------------------------
# CROSS JOIN EXERCISES
# ====================================================================

CSV_1 = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV_1))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")


CSV_2 = """
food_items,food_price
cookie juice,2.5
chocolatine, 2
muffin, 3
"""

food_items = pd.read_csv(io.StringIO(CSV_2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

sizes = """
size
XS
M
L
XL"""
sizes = pd.read_csv(io.StringIO(sizes))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

trademarks = """
trademark
Nike
Asphalte
Abercrombie
Lewis"""
trademarks = pd.read_csv(io.StringIO(trademarks))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

con.close()
