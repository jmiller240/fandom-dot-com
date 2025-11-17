
import sqlalchemy

import pandas as pd


db_host = 'fandomdbinstance.cil0ke6w208h.us-east-1.rds.amazonaws.com'
db_name = 'fandomdb'
db_user = 'fandomdbadmin'
db_pass = 'myteamdb5'


DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
engine = sqlalchemy.create_engine(DATABASE_URL)

# print('Connected to database')

## Insert
for table in ['account', 'league', 'team', 'account_team']:
    if table == 'account': continue
    
    # read file
    print(f'Reading {table}...')
    df = pd.read_csv(f'data/{table}.csv')
    print(df.head())

    # insert
    print(f'Inserting...')
    rows_inserted = df.to_sql(table, engine, schema='fandom_site', index=False, if_exists='append')
    print(f'Data inserted. {rows_inserted} rows')