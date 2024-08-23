import pymysql
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

default_conn_url = "mysql://live:livecc@localhost:3306/live"
default_port = 3306


class DBConnect(object):
    def __init__(self):
        super(DBConnect, self).__init__()
        db_type, user, password, host, port, db = self.__get_db_config()

        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self.port = default_port
        print(self.host)
    def __get_db_config(self):
        """
        :param self:
        :return:
        """
        # mysql://root:123456@192.168.1.166/liveclass
        data = re.match(r'^(\w+)://(\w+):(\S+)@(\S+):(\w+)/(\S+)$', default_conn_url)
        return data.groups()

    def read_db(self, sql_str):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port)
        cursor = db.cursor()
        doc_list = []
        try:
            cursor.execute(sql_str)
            results = cursor.fetchall()
            for row in results:
                doc_list.append(row)
        except Exception as e:
            logger.error('查询失败 %s %s' % (sql_str, e), exc_info=True)
        # 关闭数据库连接
        db.close()
        logger.info('查询结果 %s' % len(doc_list))
        return doc_list


if __name__ == '__main__':
    sql_str = "select * from live limit 1"

    dbConnect = DBConnect()
    lives = dbConnect.read_db(sql_str)

    print(lives)
    for i in lives:
        print(i[0])
