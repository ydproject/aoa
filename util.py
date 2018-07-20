# -*- coding: utf-8 -*-

import sqlite3
import os
from PyQt4 import QtGui, QtCore
import time, datetime
import traceback


def get_term():
    data = read_file("stu_term_info.txt")
    if len(data[0][1][0]) != 0:
        return data[0][1][0]
    if datetime.datetime.now().month in range(2, 6):
        return str(datetime.datetime.now().year) + "01"
    if datetime.datetime.now().month in range(6, 7):
        return str(datetime.datetime.now().year) + "02"
    if datetime.datetime.now().month in range(7, 12):
        return str(datetime.datetime.now().year) + "03"
    if datetime.datetime.now().month in [12, 1]:
        return str(datetime.datetime.now().year) + "04"


def query_current_user():
    return Sql("current_user").select({u"学号": "0"})[0]


def init_user():
    Sql("current_user").delete("0")
    Sql("current_user").add(["0", "Guest", "Guest"])
    return "Guest"


def swith_user(user, passwd):
    data = Sql("auth").select({u"用户": user})
    if len(data) != 0 and data[0][2] == passwd:
        old_list = Sql("current_user").select({u"学号": "0"})[0]
        new_list = ["0", user, data[0][3]]
        status = Sql("current_user").update(old_list, new_list)
        if status == 1:
            return 1
        else:
            return data[0][1]
    return 1


def get_user_id():
    return int(time.time())

def get_stu_id():
    num = 4
    try:
        number = Sql("stu_number_info").select({"id": "0"})
        if len(number) == 0:
            Sql("stu_number_info").add(["1", "0", "0"])
        old_list = list(Sql("stu_number_info").select({"id": "0"})[0])
        number = old_list[2]
        if number == "9999":
            number = "1"
        else:
            number = str(int(number) + 1)
        new_list = old_list[:-1]
        new_list.append(number)
        Sql("stu_number_info").update(old_list, new_list)
        return str(datetime.datetime.now().year) + "0" * (num - len(number)) + number
    except Exception, e:
        print u"get stu_id error!", traceback.format_exc()
        return int(time.time())


def str_to_sum(str):
    try:
        return reduce(lambda x,y:x+y, map(float, str.split(",")))
    except Exception,e:
        print traceback.format_exc()
        return 0

def flag_to_str(f_list):
    if len(f_list) == 0:
        return ""
    if len(f_list) == 1:
        return f_list[0]
    str_list = [f_list[0]] * (len(f_list) - 1)
    return ",".join(str_list)


def read_file(filename):
    file_info = open(os.path.join(os.getcwd(), "config", filename))
    infos = []
    for line_info in file_info:
        items = line_info.strip().split(",")
        if len(items) > 0:
            list_info = [i.decode("utf8") for i in items[1:]]
            infos.append((items[0].decode("utf8"), list_info))
    return infos


def showInputDialog(object, message=""):
    text, ok = QtGui.QInputDialog.getText(object, 'Input Dialog', message)
    if ok:
        return str(text)
    else:
        return ""

def showWarnDialog(object, message=""):
    QtGui.QMessageBox.warning(object, u"警告", message, QtGui.QMessageBox.Cancel)


def showMessageDialog(object, message=""):
    QtGui.QMessageBox.question(object, u"提示", message, QtGui.QMessageBox.Ok)


def showComfirmDialog(object, message=""):
    button=QtGui.QMessageBox.question(object,u"确认",
                                      message,
                                      QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                      QtGui.QMessageBox.Ok)
    if button==QtGui.QMessageBox.Ok:
        return 0
    else:
        return 1


class Sql():

    def __init__(self, table_name="stu_base_info"):
        self.conn = sqlite3.connect('example.db')
        self.cur = self.conn.cursor()
        self.table_name = table_name
        self.table_info = read_file(self.table_name + ".txt")
        self.initDB()

    def select_uni(self, sql):
        data = []
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
        except Exception, e:
            print traceback.format_exc()
        self.close()
        return data

    def create_table(self):
        try:
            table_info = self.table_info[1:]
            value_list = [u"%s text" % self.table_info[0][0]]
            for label, values in table_info:
                value_list.append(u"%s text" % label)
            value_str = ",".join(value_list)
            sql = u"create table %s(%s);" % (self.table_name, value_str)
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print u"create table %s failed!" % self.table_name, traceback.format_exc()

    def check_stu_id_exist(self, stu_id):
        data = self.select({u"学号": stu_id})
        if len(data) == 0:
            return False
        return True

    def check_table_update(self):
        try:
            table_info = self.table_info
            sql = u"select * from {};".format(self.table_name)
            self.cur.execute(sql)
            value_list = [item[0].decode("utf8") for item in self.cur.description]
            for label, values in table_info:
                if label not in value_list:
                    sql = u"alter table %s add column %s text;" % (self.table_name, label)
                    self.cur.execute(sql)
                    self.conn.commit()
        except Exception, e:
            print u"alert table %s failed!" % self.table_name, traceback.format_exc()

    def initDB(self):
        try:
            sql = u"select * from sqlite_master where name='%s'" % self.table_name
            self.cur.execute(sql)
            data = self.cur.fetchall()
            if len(data) == 0:
               self.create_table()
            else:
                self.check_table_update()
        except Exception, e:
            print u"data db is error!", traceback.format_exc()

    def close(self):
        self.cur.close()
        self.conn.close()

    def select_by_list(self, label_list=[], sql_dict={}):
        data = []
        if len(label_list) == 0:
            label_str = "*"
        else:
            label_str = u",".join(label_list)
        try:
            sql = u"select %s from " % label_str + self.table_name + u" where %s;"
            if len(sql_dict) == 0:
                sql = "select %s from %s;" % (label_str, self.table_name)
            else:
                select_list = [u"%s='%s'"%(i, sql_dict[i]) for i in sql_dict]
                select_info = u" and ".join(select_list)
                sql = sql % select_info
            self.cur.execute(sql)
            data = self.cur.fetchall()
        except Exception, e:
            print traceback.format_exc()
        self.close()
        return data

    def select(self, sql_dict={}):
        data = []
        label_list = [i for i, j in self.table_info]
        label_str = u",".join(label_list)
        try:
            sql = u"select %s from " % label_str + self.table_name + u" where %s;"
            if len(sql_dict) == 0:
                sql = "select %s from %s;" % (label_str, self.table_name)
            else:
                select_list = [u"%s='%s'"%(i, sql_dict[i]) for i in sql_dict]
                select_info = u" and ".join(select_list)
                sql = sql % select_info
            self.cur.execute(sql)
            data = self.cur.fetchall()
        except Exception, e:
            print traceback.format_exc()
        self.close()
        return data

    def add(self, sql_list):
        status = 0
        label_list = [i for i, j in self.table_info]
        label_str = u",".join(label_list)
        try:
            number = u",".join(["'%s'"] * len(sql_list))
            sql = u"insert into %s(%s) values(%s)" % (self.table_name, label_str, number)
            sql = sql % tuple(sql_list)
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print traceback.format_exc()
            status = 1
        self.close()
        return status

    def update(self, old_list, new_list):
        status = 0
        if len(old_list) != len(new_list):
            return 1
        if len(old_list) == 0 and len(new_list) == 0:
            return 1
        base_info = read_file("%s.txt" % self.table_name)
        stu_id = old_list[0]
        try:
            for i in range(0, len(old_list)):
                if old_list[i] != new_list[i]:
                    sql = u"update %s set %s='%s' where 学号='%s'"%\
                          (self.table_name, base_info[i][0], new_list[i], stu_id)
                    self.cur.execute(sql)
                    self.conn.commit()
                    if i == 0:
                        stu_id = new_list[0]
        except Exception, e:
            # print str(e)
            print traceback.format_exc()
            status = 1
        self.close()
        return status

    def delete(self, stu_id):
        status = 0
        try:
            sql = u"delete from %s where 学号='%s'" % (self.table_name, stu_id)
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print traceback.format_exc()
            status = 1
        self.close()
        return status


def select_premoney_by_stu(value_list1=[], value_list2=[], dict1={}, dict2={}):
    sql = Sql(u"stu_base_info")
    sql = Sql(u"stu_money_pre")
    sql = Sql()
    print value_list1, value_list2, dict1, dict2
    if len(value_list1) == 0 and len(value_list2) == 0:
        label_str = "*"
    else:
        value_list1 = [u"stu_base_info." + i for i in value_list1]
        value_list2 = [u"stu_money_pre." + i for i in value_list2]
        label_str = u",".join(value_list1 + value_list2)

    sql_info = u"select %s from stu_base_info, stu_money_pre where stu_base_info.学号=stu_money_pre.学号" % label_str
    if len(dict1) != 0 or len(dict2) != 0:
        select_list = []
        if len(dict1) != 0:
            for i in dict1:
                select_list.append(u"stu_base_info.%s='%s'" % (i, dict1[i]))
        if len(dict2) != 0:
            for i in dict2:
                if dict2[i] == u'-1':
                    select_list.append(u"stu_money_pre.%s!='0'" % i)
                elif dict2[i] == u'0':
                    select_list.append(u"stu_money_pre.%s='0'" % i)
                else:
                    select_list.append(u"stu_money_pre.%s='%s'" % (i, dict2[i]))
        sql_info = sql_info + " and " + " and ".join(select_list)
    return sql.select_uni(sql_info)


def select_money_by_stu(value_list1=[], value_list2=[], dict1={}, dict2={}):
    sql = Sql(u"stu_base_info")
    sql = Sql(u"stu_money_info")
    sql = Sql()
    if len(value_list1) == 0 and len(value_list2) == 0:
        label_str = "*"
    else:
        value_list1 = [u"stu_base_info." + i for i in value_list1]
        value_list2 = [u"stu_money_info." + i for i in value_list2]
        label_str = u",".join(value_list1 + value_list2)

    sql_info = u"select %s from stu_base_info, stu_money_info where stu_base_info.学号=stu_money_info.学号" % label_str
    if len(dict1) != 0 or len(dict2) != 0:
        select_list = []
        if len(dict1) != 0:
            for i in dict1:
                select_list.append(u"stu_base_info.%s='%s'" % (i, dict1[i]))
        money_infos = read_file("stu_money_info.txt")
        money_infos = {i:flag_to_str(j) for i, j in money_infos}
        if len(dict2) != 0:
            for i in dict2:
                if dict2[i] == u'-1':
                    select_list.append(u"stu_money_info.%s='%s'" % (i, money_infos[i]))
                elif dict2[i] == u'0':
                    select_list.append(u"stu_money_info.%s!='%s'" % (i, money_infos[i]))
                else:
                    select_list.append(u"stu_money_info.%s='%s'" % (i, dict2[i]))
        sql_info = sql_info + " and " + " and ".join(select_list)
    return sql.select_uni(sql_info)


if __name__ == '__main__':
    # showInputDialog()
    # test = Sql("stu_money_info")
    # # sql = "alter table stu_money_info add column name text;"
    # sql = "select * from {};".format("stu_money_info")
    # test.cur.execute(sql)
    # print test.cur.description
    # # test.conn.commit()
    # test.close()
    print select_money_by_stu(value_list1=[u"学号"], value_list2=[u"生活费"], dict1={u"学号": u"20180007"}, dict2={u"生活费": "0"})