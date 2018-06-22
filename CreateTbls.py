__author__ = 'Valery'

import psycopg2
from DBconfData import DBconf

with psycopg2.connect(**DBconf.db_params) as conn:
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
        uname varchar(255),
        bd integer,
        bm integer,
        by integer
        );
    ''')
    curs.execute('''
        create table chtusr (
        cuid varchar(255) primary key,
        cid bigint,
        uid bigint
        );
    ''')