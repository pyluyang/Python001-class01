# -*- coding: utf-8 -*-

import mysql.connector
import numpy as np
import pandas as pd
from snownlp import SnowNLP
from sqlalchemy import create_engine

MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'ly'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'xxxxxx'

conn = mysql.connector.connect(
    host=MYSQL_HOST, port=MYSQL_PORT,
    user=MYSQL_USER, password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
)
sql = (
    "SELECT id, article_id, goods_type, user_name, user_id, "
    "pub_time, comment_id, comment_info, crawl_time FROM comment"
)


def main():
    df = pd.read_sql(sql, conn)
    df['sentiments'] = df['comment_info'].map(lambda x: SnowNLP(x).sentiments)
    df.replace({np.nan: None})
    engine = create_engine(
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}',
        echo=False
    )
    new_table = 'sentiments'
    df.to_sql(new_table, engine, if_exists='replace')


if __name__ == '__main__':
    main()
