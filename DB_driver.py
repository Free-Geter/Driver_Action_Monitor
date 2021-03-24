import pymysql

def connect():
    db = pymysql.connect(host='localhost', user='root', password='200046m..', database='driver_monitor')
    cursor = db.cursor()
    return (db,cursor)

def create():
    db,cursor = connect()
    cursor.execute("DROP TABLE IF EXISTS driving_behavior_record")
    sql = """CREATE TABLE `driving_behavior_record` (
  `date` date NOT NULL,
  `begin_time` varchar(45) NOT NULL,
  `behavior_type` varchar(45) DEFAULT NULL,
  `behavior_possibility` float DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`,`date`,`begin_time`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
    cursor.execute(sql)
    db.close()



def insert(date,begin_time,behavior_type,behavior_possibility,photo):
    db,cursor = connect()
    sql = """INSERT INTO driving_behavior_record
    (date, begin_time, behavior_type, behavior_possibility, photo)
    VALUES ('{0}', '{1}', '{2}', {3}, '{4}');""".format(date,begin_time,behavior_type,behavior_possibility,photo)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def inquire_1(date1):
    db = pymysql.connect(host='localhost', user='root', password='123456', database='b')
    cursor = db.cursor()
    try:
        sql = "SELECT count(*)behavior_type FROM driver WHERE date = '" + date1 + "'"
        cursor.execute(sql)
        results = cursor.fetchall()
        # 1 根据日期查询，前端给日期参数，返回当天总不良驾驶行为次数、各行为所占百分比。
        for row in results:
            behavior_type = row[0]
            print("behavior_type = %s" % (behavior_type))
        sql1 = "select count(*)behavior_type from driver where behavior_type = 'both_hands_leaving_wheel' AND date = '" + date1 + "' "
        cursor.execute(sql1)
        results1 = cursor.fetchall()
        for row in results1:
            behavior_type1 = row[0]
        percent1 = behavior_type1 /behavior_type
        print('双手离开方向盘的百分比:', percent1)
        sql2 = "select count(*)behavior_type from driver where behavior_type = 'no_face_mask' AND date = '" + date1 + "' "
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        for row in results2:
            behavior_type2 = row[0]
        percent2 = behavior_type2 / behavior_type
        print('没戴口罩的百分比:', percent2)
        sql3 = "select count(*)behavior_type from driver where behavior_type = 'not_buckling_up'AND date = '" + date1 + "' "
        cursor.execute(sql3)
        results3 = cursor.fetchall()
        for row in results3:
            behavior_type3 = row[0]
        percent3 = behavior_type3 / behavior_type
        print('没有戴安全帽的百分比:', percent3)
        sql4 = "select count(*)behavior_type from driver where behavior_type = 'smoke' AND date = '" + date1 + "' "
        cursor.execute(sql4)
        results4 = cursor.fetchall()
        for row in results4:
            behavior_type4 = row[0]
        percent4 = behavior_type4 / behavior_type
        print('吸烟的百分比:' ,percent4)
        sql5 = "select count(*)behavior_type from driver where behavior_type = 'cellphone' AND date = '" + date1 + "' "
        cursor.execute(sql5)
        results5 = cursor.fetchall()
        for row in results5:
            behavior_type5 = row[0]
        percent5 = behavior_type5 / behavior_type
        print('使用手机的百分比:', percent5)
        sql6 = "select count(*)behavior_type from driver where behavior_type = 'Fatigue_driving' AND date = '" + date1 + "' "
        cursor.execute(sql6)
        results6 = cursor.fetchall()
        for row in results6:
            behavior_type6 = row[0]
        percent6 = behavior_type6 / behavior_type
        print('疲劳驾驶的百分比:', percent6)
        sql7 = "select count(*)behavior_type from driver where behavior_type = 'yawning' AND date = '" + date1 + "' "
        cursor.execute(sql7)
        results7 = cursor.fetchall()
        for row in results7:
            behavior_type7 = row[0]
        percent7 = behavior_type7 / behavior_type
        print('打呵欠的百分比:', percent7)
        sql8 = "select count(*)behavior_type from driver where behavior_type = 'eyes_closed' AND date = '" + date1 + "' "
        cursor.execute(sql8)
        results8 = cursor.fetchall()
        for row in results8:
            behavior_type8 = row[0]
        percent8 = behavior_type8 / behavior_type
        print('闭眼的百分比:', percent8)
        sql9 = "select count(*)behavior_type from driver where behavior_type = 'head_lowered' AND date = '" + date1 + "' "
        cursor.execute(sql9)
        results9 = cursor.fetchall()
        for row in results9:
            behavior_type9 = row[0]
        percent9 = behavior_type9 / behavior_type
        print('低头的百分比:', percent9)

    except:
        print('Error')
    db.close()


# 2 前端给日期、起始序号参数，返回 从起始序号开始后10条具体行为记录
def inquire_2(date2, number2):
    db = pymysql.connect(host='localhost', user='root', password='123456', database='b')
    cursor = db.cursor()
    sql = "SELECT count(*)behavior_type FROM driver WHERE date = '" + date2 + "' AND "




# create()
# insert()
# inquire_1('2021.03.26')
