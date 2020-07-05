# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class MaoyanMoviesPipeline:
    def process_item(self, item, spider):
        film_name = item['film_name']
        film_types = item['film_types']
        plan_date = item['plan_date']
        # output = f'|{film_name}|\t|{film_types}|\t|{plan_date}|\n\n'
        # print('-----',output)
        # with open('./maoyan.csv', 'a+', encoding='utf-8') as article:
        #     article.write(output)
        # return item
        data = (film_name,film_types,plan_date)
        #insert into mysql
        try:
            insertsql = 'insert into movie_list (film_name,film_types,plan_date) values (%s,%s,%s)'
            dbconn = Mysqldb()
            dbconn.run(insertsql,data)

        except Exception as e:
            print(e)

        return item

class Mysqldb:

    def  __init__(self):
        db_config = {
            'host': 'xxx',
            'port': 'xxx',
            'user': 'xxx',
            'password': 'xxx',
            'db': 'xx'
            }
            
        self.conn = pymysql.connect(**db_config)


    def get_cursor(self):
        return self.conn.cursor()
 
    def query(self,sql):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                 print(row)
                 return row

            self.conn.commit()
        except Exception as e:
            print('unexcept happened at the query sql',str(e))
            self.conn.rollback()
        #close connection
        #self.conn.close()

    def run(self,sql,data):
        # 游标建立的时候就开启了一个隐形的事物
        cursor = self.get_cursor()
        try:
            cursor.execute(sql,data)   
            self.conn.commit()
        except Exception as e:
            print('unexcept happened at the execute sql',str(e))
            self.conn.rollback()
