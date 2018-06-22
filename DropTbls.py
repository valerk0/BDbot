__author__ = 'Valery'

import psycopg2
from DBconfData import DBconf

with psycopg2.connect(**DBconf.db_params) as conn:
    curs=conn.cursor()
    curs.execute(drop table cht;)

    curs.execute(drop table usr;)

    curs.execute(drop table chtusr;)