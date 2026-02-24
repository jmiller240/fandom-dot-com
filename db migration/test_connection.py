
from connect_postgres import connect_local


## Tests ##

def test_local():
    connection = connect_local()

    cursor = connection.cursor()
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print('Version:', db_version)

    cursor.close()


test_local()