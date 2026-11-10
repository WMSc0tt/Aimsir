#this file is to create the database for Aimsir and for its users and sightings tabe in the PostgreSQL database

import os
import psycopg2

#connection details for the PostgreSQL database
DB_NAME = os.environ.get('AIMSIR_DB_NAME', 'aimsir_db')
DB_USER = os.environ.get('AIMSIR_DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('AIMSIR_DB_PASSWORD', 'postgres_password')
DB_HOST = os.environ.get('AIMSIR_DB_HOST', 'localhost')
DB_PORT = os.environ.get('AIMSIR_DB_PORT', '5432')

#insert the same SQL as the Create_tables.sql file

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    userid varchar(50) PRIMARY KEY NOT NULL,
    password varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS sightings (
    sighting_id varchar(50) PRIMARY KEY NOT NULL,
    s_datetime varchar(50),
    s_city varchar(30),
    s_weather_type varchar(255),
    summary varchar(255),
    userid varchar(50) REFERENCES users(userid)
);
"""
#all sql above is from create_tables.sql

#This is for the creation of the connection to the database to create aimsir_db
conn = psycopg2.connect(database="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
conn.autocommit = True         
cur = conn.cursor()
 
cur.execute("select 1 from pg_database where datname = %s;", (DB_NAME,))
if cur.fetchone() is None:
    cur.execute(f'create database "{DB_NAME}";')
    print(f"Database '{DB_NAME}' created.")
else:
    print(f"Database '{DB_NAME}' already exists.")
 
cur.close()
conn.close()
 
# 2) Connect to aimsir_db and create the tables
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                        host=DB_HOST, port=DB_PORT)
cur = conn.cursor()
cur.execute(CREATE_TABLES_SQL)
conn.commit()
 
cur.execute("select table_name from information_schema.tables where table_schema='public';")
print("Tables in database:", [row[0] for row in cur.fetchall()])
 
cur.close()
conn.close()
