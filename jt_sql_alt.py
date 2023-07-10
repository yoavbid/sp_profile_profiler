"""
Alternative implementation for jt_sql.py based on snowflake.connector instead of sqlalchemy.
Both implementation are working. Keeping it here in case the other implementation will break.
"""
import os
import snowflake.connector.pandas_tools

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_conn():
    try:
        with open(os.path.join(__location__, 'snowflake_user_pwd'), 'r') as f:
            user_password = f.read()
        user = user_password.split('\n')[0]
        password = user_password.split('\n')[1]
    except FileNotFoundError:
        user = os.environ['SNOWFLAKE_USER']
        password = os.environ['SNOWFLAKE_PASSWORD']

    conn = snowflake.connector.connect(user=user, password=password,
                                       account='bua07785.us-east-1', database='analytics', schema='public',
                                       warehouse='AGGREGATION_PIPELINE')
    return conn


def execute_query(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    df = cursor.fetch_pandas_all()
    cursor.close()
    return df
