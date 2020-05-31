__author__ = 'Valery'

import psycopg2, os
from urllib.parse import urlparse

db_config = urlparse(os.environ['DATABASE_URL'])
with psycopg2.connect(user=db_config.username,
                      password=db_config.password,
                      database=db_config.path[1:],
                      host=db_config.hostname) as conn:
    curs=conn.cursor()
    curs.execute('drop table cht;')

    curs.execute('drop table usr;')

    curs.execute('drop table chtusr;')