# Test Branch

This branch is used for generic development and should not be used to add specific features but rather to test the implementation of existing ones.

# Testing SQL Queries

1. Start with building the project running `docker-compose build` in a terminal instance in the root directory of the project.
2. Execute the ipython client service by running `docker-compose run --rm ipython`. This will open an interactive python interpreter that can be connected to the SQL Database.
3. Run the following commands in the window to fetch different queries from the database:

```python
# import the necessary libraries to connect to the PostgreSQL Engine
import psycopg2
# Initiate connection to the database, notice that here it is called "db" because it is run in a different container
# and so the name of the service (as specified in the docker-compose file) must be specified here as the host to work properly
# The port is also specified in the docker-compose file
conn = psycopg2.connect(dbname="raw_data", user="postgres", password="example", host="db", port=5432)
# Allows Python code to execute PostgreSQL command in a database session. Cursors are created by the connection.cursor() method
# they are bound to the connection for the entire lifetime and all the commands are executed in the context of the database session wrapped by the connection.
cur = conn.cursor()
# Execute a database operation (query or command).
cur.execute("SELECT * FROM trips LIMIT 5;")
# Fetch all (remaining) rows of a query result, returning them as a list of tuples. An empty list is returned if there is no more record to fetch.
print(cur.fetchall())
```
