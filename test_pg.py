import psycopg2
try:
    psycopg2.connect(dbname='finanzas', user='postgres', password='Teojhoanig12*', host='localhost')
except Exception as e:
    print('Error:', type(e), e.args)
