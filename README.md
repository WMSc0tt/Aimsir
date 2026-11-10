# Aimsir

Aimsir is a local Irish weather reporting web application built with Python and Flask.
Users can sign in and report weather sightings (Heavy Rain, Storm, Fog, High Winds),
which are stored in a PostgreSQL database.

## Tech stack
Python 3.11, Flask 3.0.0, Flask-SQLAlchemy, Flask-WTF, PostgreSQL 16, Docker, GitHub Actions.
Full versions are in `tech_spec.yaml` and `requirements.txt`.

## Test account
Once the data is loaded, sign in (or report a sighting) with any user from `data/UserDetails.csv`, for example:

| Username | Password |
| `aisling_brennan69` | `vXVF!C3ZejP4` |
| `cathal_moore66` | `ptEgptSf#PS%` |

These are dummy development accounts only.

## Setup
1. Create and activate a virtual environment, then run `pip install -r requirements.txt`
2. (Optional) set `AIMSIR_DB_PASSWORD` to your PostgreSQL password
3. Create the database and tables: `python initialise_db.py`
4. Load the data: `python populate_db.py`
5. Run the app: `python aimsir.py` and open http://127.0.0.1:5000

## Database
- `users` (userid, password): 50 rows
- `sightings` (sighting_id, s_datetime, s_city, s_weather_type, summary, userid): 500 rows

The SQL is in `create_tables.sql`. The data in `data/UserDetails.csv` and `data/sightings.csv`
is synthetic and was generated with Claude (Anthropic). The prompt used is recorded in `GenAI_prompt.txt`.
The passwords are dummy development values.

## Branches
- `main`: initial website (Home and About Us pages)
- `feature-login`: login checked against the `users` table
- `feature-report-sighting`: report form saves a new row in the `sightings` table
