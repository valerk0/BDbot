__author__ = 'Valery'

import psycopg2
from confData import confData

conf=confData('dbconfig.ini','DATABASE')
with psycopg2.connect(**conf.params) as conn:
    curs=conn.cursor()
    curs.execute('drop table cht;')

    curs.execute('drop table usr;')

    curs.execute('drop table chtusr;')