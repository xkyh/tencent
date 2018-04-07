# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class TencentPipeline(object):
    # def __init__(self):
    #     self.filename = open('tencentposition.txt', 'w', encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     text = str(item) + "\n"+ "\n"
    #     self.filename.write(text)
    #     return item
    #
    # def filenameclose(self):
    #     self.filename.close()

    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='tencent',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        cols, values = zip(*item.items())
        sql = 'insert into `%s` (%s) values (%s)' % \
              (item.table,
               ','.join(['`%s`' % k for k in cols]),
               ','.join(['%s'] * len(cols)))
        self.cur.execute(sql, values)
        self.conn.commit()
        print(self.cur._last_executed)
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
