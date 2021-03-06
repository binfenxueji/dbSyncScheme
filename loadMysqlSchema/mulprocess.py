import pymysql

import time

import multiprocessing as mp
# by 光城
def job(q):
    res = 0
    for i in range(1000000):
        res += i + i**2 + i**3
    q.put(res) # queue




class MyPyMysql:
    def __init__(self, host, port, username, password, db, charset='utf8'):
        self.host = host  # mysql主机地址
        self.port = port  # mysql端口
        self.username = username  # mysql远程连接用户名
        self.password = password  # mysql远程连接密码
        self.db = db  # mysql使用的数据库名
        self.charset = charset  # mysql使用的字符编码,默认为utf8
        self.pymysql_connect()  # __init__初始化之后，执行的函数

    def pymysql_connect(self):
        # pymysql连接mysql数据库
        # 需要的参数host,port,user,password,db,charset
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.username,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset
                                    )
        # 连接mysql后执行的函数
        # self.run()
        self.multicore()

    def run(self,start,end,m):
        # 创建游标
        self.cur = self.conn.cursor()

        # 定义sql语句,插入数据id,name,gender,email
        sql = "insert into sqlbase(carflag, touchevent, opstatus,gpstime,gpslongitude,gpslatitude,gpsspeed,gpsorientation,gpsstatus) values(%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%s'),%s,%s,%s,%s,%s)"

        # 定义总插入行数为一个空列表
        print("================================="+m+"==================================")
        for i in range(start,end+1):
            data_list = []
            count = 0
            with open('/home/light/mysql/gps/gps_'+str(i)+'.txt', 'r') as fp:
                for line in fp:
                    line = line.split(',')
                    # print(line)
                    carflag, touchevent, opstatus, gpstime, gpslongitude, gpslatitude, gpsspeed, gpsorientation, gpsstatu = line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8].strip()

                    gpstime = gpstime[:4]+'-'+gpstime[4:6]+'-'+gpstime[6:8]+' '+gpstime[8:10]+':'+gpstime[10:12]+':'+gpstime[12:14]
                    tup = (carflag, touchevent, opstatus, gpstime, gpslongitude, gpslatitude, gpsspeed, gpsorientation, gpsstatu)
                    data_list.append(tup)
                    count += 1
                    if count and count%20000==0:
                        # 执行多行插入，executemany(sql语句,数据(需一个元组类型))
                        self.cur.executemany(sql, data_list)
                        # 提交数据,必须提交，不然数据不会保存
                        self.conn.commit()
                        data_list = []
                        print("提交了：" + str(count) + "条数据")

            if data_list:
                # 执行多行插入，executemany(sql语句,数据(需一个元组类型))
                self.cur.executemany(sql, data_list)
                # 提交数据,必须提交，不然数据不会保存
                self.conn.commit()
                print("提交了：" + str(count) + "条数据")
        # self.cur.close()  # 关闭游标
        # self.conn.close()  # 关闭pymysql连接

    def multicore(self):
        file_list = [1,2324,4648,6972,9298]
        m1 = mp.Process(target=self.run, args=(file_list[0],file_list[1],'m1',))
        m2 = mp.Process(target=self.run, args=(file_list[1]+1,file_list[2],'m2',))
        m3 = mp.Process(target=self.run, args=(file_list[2]+1,file_list[3],'m3',))
        m4 = mp.Process(target=self.run, args=(file_list[3]+1,file_list[4],'m4',))
        m1.start()
        m2.start()
        m3.start()
        m4.start()
        m1.join()
        m2.join()
        m3.join()
        m4.join()


if __name__ == '__main__':
    start_time = time.time()  # 计算程序开始时间
    st = MyPyMysql('127.0.0.1', 3306, 'root', 'xxxx', 'loaddb')  # 实例化类，传入必要参数
    print('程序耗时{:.2f}'.format(time.time() - start_time))  # 计算程序总耗时
