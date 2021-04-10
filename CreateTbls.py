__author__ = 'Valery'

import psycopg2, os
from urllib.parse import urlparse

db_config = urlparse(os.environ['DATABASE_URL'])
with psycopg2.connect(user=db_config.username,
                      password=db_config.password,
                      database=db_config.path[1:],
                      host=db_config.hostname) as conn:
    curs=conn.cursor()
    curs.execute('''
        create table cht (
        cid bigint primary key,
        cname varchar(255)
        );
    ''')

    curs.execute('''
        create table usr (
        uid bigint primary key,
        uuname varchar(255),
        uname varchar(255),
        bd integer,
        bm integer,
        by integer
        );
    ''')

    # curs.execute('''
    #     create table chtusr (
    #     cuid varchar(255) primary key,
    #     cid bigint,
    #     uid bigint
    #     );
    # ''')