import sqlite3

conn = sqlite3.connect("healthdata.sqlite")

cursor = conn.cursor()

sql_qry = """ create table healthdata (
    id integer primary key,
    name text not null,
    app_name text not null,
    steps integer,
    oxygen text,
    calories text,
    distance text
)"""

# sql_qry = """ create table healthimage (
#     id integer primary key,
#     image text
# )"""

cursor.execute(sql_qry)
