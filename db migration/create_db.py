
import psycopg2


db_host = 'fandomdbinstance.cil0ke6w208h.us-east-1.rds.amazonaws.com'
db_name = 'fandomdb'
db_user = 'fandomdbadmin'
db_pass = 'myteamdb5'


connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
print('Connected to database')

db_creation_sql = open('create_db.sql', 'r+').read()
queries = [q.strip() for q in db_creation_sql.split(';')]

cursor = connection.cursor()

for q in queries:
    if not q: continue
    
    print(q)
    cursor.execute(q)
    print('Query complete.')

print('All done.')
cursor.close()
connection.commit()