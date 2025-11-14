
import psycopg2


db_host = 'fandomdbinstance.cil0ke6w208h.us-east-1.rds.amazonaws.com'
db_name = 'fandomdb'
db_user = 'fandomdbadmin'
db_pass = 'myteamdb5'

connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
print('Connected to database')

cursor = connection.cursor()
cursor.execute('SELECT version()')
db_version = cursor.fetchone()
print('Version:', db_version)

cursor.close()