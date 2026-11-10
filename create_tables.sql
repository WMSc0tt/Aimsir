--Aimsir database: tables, feilds and relationships
-- Run against the aimsir_db database in the postgresql server

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