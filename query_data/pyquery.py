from sqlalchemy import create_engine, text
import pandas as pd

# Format: postgresql://user:password@host:port/dbname
# db is used as host since the database is in another container
engine = create_engine("postgresql://postgres:example@db:5432/raw_data")

df = pd.read_sql("SELECT * FROM routes LIMIT 50", engine)

print(df.head())