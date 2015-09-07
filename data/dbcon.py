__author__ = 'exley'

import sqlalchemy as sa
import pandas as pd
import MySQLdb as mdb

def make_db_connection(database, user='xread', password=None, host='127.0.0.1', conn_type='SA'):
    """
    :param database: Database to which you want to connect.
    :param user: MySQL Username
    :param password: If no password, default to username
    :param host: Address of SQL Server
    :param conn_type: 'SA' for sqlalchemy; 'MS' for MySQLdb
    :return: Database Engine. Not connected.
    """
    if password is None:
        password = user
    if conn_type.upper() == 'SA':
        con_str = 'mysql://' + user + ':' + password + '@' + host + '/' + database
        db_con = sa.create_engine(con_str, isolation_level='READ UNCOMMITTED')
    elif conn_type.upper() == 'MYSQL':
        db_con = mdb.connect(host=host, user=user, passwd=password)
    else:
        return None
    return db_con


def get_data(con, sql, ret_type='df'):
    if ret_type.lower() == 'df':
        return pd.read_sql_query(sql, con)
    elif ret_type.lower() == 'list':
        return [r for r in con.execute(sql)]
    elif ret_type.lower() == 'item':
        tmp = con.execute(sql).fetchone()
        if tmp is None:
            return None
        else:
            return tmp[0]
    elif ret_type.lower() == 'object':
        return con.execute(sql)
