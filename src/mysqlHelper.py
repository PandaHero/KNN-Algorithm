import pymysql


class MysqlHelper:
    '''
    python操作mysql增删查改的封装
    '''

    def __init__(self, host, user, password, database, port=3306, charset="utf8"):
        '''
        :param host:ip地址
        :param user:用户
        :param password:密码
        :param database:数据库名称
        :param port:端口号
        :param charset:编码格式
        '''
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset

    def connect(self):
        '''
        获取连接对象和执行对象
        :return:
        '''
        # 获取连接对象
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                    port=self.port, charset=self.charset)
        # 获取执行对象
        self.cur = self.conn.cursor()

    def fetchone(self, sql, params=None):
        '''
        根据sql和参数获取一行数据
        :param sql: sql语句
        :param params: sql语句对象的参数元祖，默认值为None
        :return: 查询一行数据
        '''
        dataOne = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataOne = self.cur.fetchone()
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return dataOne

    def fetchall(self, sql, params=None):
        '''
        根据sql和参数获取所有数据
        :param sql:sql语句
        :param params:sql语句对象的参数列表
        :return:返回值查询的所有数据
        '''
        dataAll = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataAll = self.cur.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return dataAll

    def __item(self, sql, params=None):
        '''
        执行增删改操作
        :param sql: sql语句
        :param params: sql语句对象的参数列表
        :return: 返回操作
        '''
        count = 0
        try:
            count = self.cur.execute(sql, params)
            self.conn.commit()
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return count

    def insert(self, sql, params=None):
        '''
        执行新增
        :param sql:sql语句
        :param params: sql语句对象的参数列表
        :return: 返回值
        '''
        return self.__item(sql, params)

    def delete(self, sql, params=None):
        '''
        执行删除操作
        :param sql:sql语句
        :param params: sql语句对象参数对象
        :return: 返回值
        '''
        return self.__item(sql, params)

    def select(self, sql, params=None):
        '''
        执行查找操作
        :param sql:
        :param params:
        :return:
        '''
        return self.__item(sql, params)

    def update(self, sql, params=None):
        '''
        执行修改操作
        :param sql:
        :param params:
        :return:
        '''
        return self.__item(sql, params)

    def close(self):
        '''
        关闭执行对象和连接对象
        :return:
        '''
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()


if __name__ == '__main__':
    # 初始化数据库对象
    mysqlhelper = MysqlHelper("localhost", "root", "root", "my_db")
    # 连接
    mysqlhelper.connect()
    sql_1 = "select * from per_info "
    data = mysqlhelper.fetchall(sql_1)
    mysqlhelper.connect()
    sql_2 = "update per_info set first_name=%s where my_id=111"
    params = ["jack"]
    mysqlhelper.update(sql_2, params)
