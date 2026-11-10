#import all of the dependencies

import csv
import os
import psycopg2

DB_NAME = os.environ.get("AIMSIR_DB_NAME", "aimsir_db")
DB_USER = os.environ.get("AIMSIR_DB_USER", "postgres")
DB_PASSWORD = os.environ.get("AIMSIR_DB_PASSWORD", "postgres_password")
DB_HOST = os.environ.get("AIMSIR_DB_HOST", "localhost")
DB_PORT = os.environ.get("AIMSIR_DB_PORT", "5432")
 
# Paths to the data files (relative to this script)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
csv_file_users = os.path.join(path, "UserDetails.csv")
csv_file_sightings = os.path.join(path, "sightings.csv")
 
# Connect to the database and create a cursor
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                        host=DB_HOST, port=DB_PORT)
cur = conn.cursor()
 
#Clear existing rows as we are repopulating the database with new data
cur.execute("delete from sightings;")
cur.execute("delete from users;")
 
#Users first: sightings.userid refers to users.userid
with open(csv_file_users, newline="") as csvfile:
    dataReader = csv.reader(csvfile, delimiter=",")
    for row in dataReader:
        cur.execute("insert into users (userid, password) values (%s, %s);",
                    (row[0], row[1]))
 
#csv needs a primary key fo rthe sightings table, so this will be created
counter = 1
with open(csv_file_sightings, newline="") as csvfile:
    dataReader = csv.DictReader(csvfile)
    for row in dataReader:
        pk = "S" + str(counter).zfill(4)
        cur.execute(
            "insert into sightings (sighting_id, s_datetime, s_city, s_weather_type, summary, userid) "
            "values (%s, %s, %s, %s, %s, %s);",
            (pk, row["s_datetime"], row["s_city"], row["s_weather_type"],
             row["summary"], row["userid"]))
        counter += 1
 
# Commit, then close the cursor and connection
conn.commit()
 
cur.execute("select count(*) from users;")
print("users rows:", cur.fetchone()[0])
cur.execute("select count(*) from sightings;")
print("sightings rows:", cur.fetchone()[0])
 
cur.close()
conn.close()