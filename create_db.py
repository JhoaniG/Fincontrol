import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='Teojhoanig12*', host='localhost')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('CREATE DATABASE finanzas;')
    print('Database created successfully')
except Exception as e:
    print('Error:', e)
