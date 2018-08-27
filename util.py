# -*- coding: utf-8 -*-

import sqlite3
import os
from PyQt4 import QtGui, QtCore
import time, datetime
import Tkinter, tkFileDialog
import traceback
import pandas as pd
from PIL import Image
from log import INFO, ERROR, WARN, DEBUG


NULL_VALUE=u"0,0,0,0,0"
DATA_FORMAT = QtCore.QString("yyyy/MM/dd HH:mm:ss")
DATA_INIT = QtCore.QString("yyyy-MM-dd")


def get_cwd():
    return os.getcwd()


def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# 2.把字符串转成datetime
def string_toDatetime(st):
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")


def get_term():
    data = read_file("stu_term_info.txt")
    term = ""
    if len(data[0][1][0]) != 0:
        term = data[0][1][0]
    if datetime.datetime.now().month in range(2, 6):
        term = str(datetime.datetime.now().year) + "01"
    if datetime.datetime.now().month in range(6, 7):
        term = str(datetime.datetime.now().year) + "02"
    if datetime.datetime.now().month in range(7, 12):
        term = str(datetime.datetime.now().year) + "03"
    if datetime.datetime.now().month in [12, 1]:
        term = str(datetime.datetime.now().year) + "04"
    DEBUG(u"Get term info: %s" % term)
    return term


def query_current_user():
    user_info = Sql("current_user").select({u"学号": "0"})[0]
    return user_info


def init_user():
    DEBUG(u"Init user: Guest")
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
            ERROR(u"Swith user failed. user: %s" % user)
            return 1
        else:
            DEBUG("Swith user: %s" % str(data[0][1]))
            return data[0][1]
    WARN(u"Swith user failed: user or passwd error! user: %s, password: %s" % (user, passwd))
    return 1


def get_user_id():
    t_id = int(time.time())
    DEBUG(u"Get user id: %d" % t_id)
    return t_id


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
        t_id = str(datetime.datetime.now().year) + "0" * (num - len(number)) + number
        DEBUG(u"Get stu id: %s" % t_id)
        return t_id
    except Exception, e:
        t_id = int(time.time())
        ERROR(u"Get stu id failed: %s. Output: %d" % (traceback.format_exc(), t_id))
        return t_id


def str_to_sum(str):
    try:
        sum = reduce(lambda x,y:x+y, map(float, str.split(",")))
        DEBUG(u"Str to sum: %s to %f" % (str, sum))
        return sum
    except Exception,e:
        ERROR(u"Str to sum failed: %s. Output: 0" % traceback.format_exc())
        return 0


def flag_to_str(f_list):
    if len(f_list) == 0:
        DEBUG(u"Flag to str: %s to ''" % str(f_list))
        return ""
    if len(f_list) == 1:
        DEBUG(u"Flag to str: %s to %s" % (str(f_list), f_list[0]))
        return f_list[0]
    str_list = [f_list[0]] * (len(f_list) - 1)
    str = ",".join(str_list)
    DEBUG(u"Flag to str: %s to %s" % (str(f_list), str))
    return str


def read_file(filename):
    file_info = open(os.path.join(get_cwd(), "config", filename))
    infos = []
    for line_info in file_info:
        items = line_info.strip().split(",")
        if len(items) > 0:
            list_info = [i.decode("utf8") for i in items[1:]]
            infos.append((items[0].decode("utf8"), list_info))
    DEBUG(u"Read file %s: %s" % (filename, str(infos)))
    return infos


def showInputDialog(object, message=""):
    ok = False
    try:
        while not ok:
            text, ok = QtGui.QInputDialog.getText(object, 'Input Dialog', message)
        return str(text)
    except Exception, e:
        ERROR(u"ShowInputDialog failed: %s" % traceback.format_exc())
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
            data.reverse()
        except Exception, e:
            ERROR(u"Select uni,sql: %s failed: %s" % (unicode(sql), traceback.format_exc()))
        self.close()
        DEBUG(u"Select uni,sql: %s output: %s" % (unicode(sql), unicode(data)))
        return data

    def create_table(self):
        try:
            table_info = self.table_info[1:]
            value_list = [u"%s text" % self.table_info[0][0]]
            for label, values in table_info:
                value_list.append(u"%s text" % label)
            value_str = u",".join(value_list)
            sql = u"create table %s(%s);" % (self.table_name, value_str)
            DEBUG(u"Create table Sql: %s" % sql)
            self.cur.execute(sql)
            self.conn.commit()
            DEBUG(u"Create table: %s" % self.table_name)
        except Exception, e:
            ERROR(u"Create table %s failed: %s" % (self.table_name, traceback.format_exc()))

    def check_stu_id_exist(self, stu_id):
        data = self.select({u"学号": stu_id})
        if len(data) == 0:
            res = False
        else:
            res = True
        DEBUG(u"Check stu id exist: %s %s" %(stu_id, str(res)))
        return res

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
            DEBUG(u"Check table update: %s to %s" % (str(value_list), str(table_info)))
        except Exception, e:
            ERROR(u"Check table update failed,alert %s:%s" % (self.table_name, traceback.format_exc()))

    def initDB(self):
        try:
            sql = u"select * from sqlite_master where name='%s'" % self.table_name
            self.cur.execute(sql)
            data = self.cur.fetchall()
            if len(data) == 0:
               self.create_table()
            else:
                self.check_table_update()
            DEBUG(u"InitDB: %s" % self.table_name)
        except Exception, e:
            ERROR(u"InitDB failed: %s" % traceback.format_exc())

    def close(self):
        self.cur.close()
        self.conn.close()
        DEBUG(u"Close DB: %s" % self.table_name)

    def select_by_list(self, label_list=[], sql_dict={}):
        DEBUG(u"Select by lis,label_list: %s, sql_dict: %s" % (unicode(label_list), unicode(sql_dict)))
        data = []
        if len(label_list) == 0:
            label_str = "*"
        else:
            label_str = u",".join(label_list)
        sql = u""
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
            data.reverse()
            DEBUG(u"Select by list,Sql: %s data: %s" % (sql, unicode(data)))
        except Exception, e:
            ERROR(u"Select by list,Sql: %s failed: %s" %(sql, traceback.format_exc()))
        self.close()
        DEBUG(u"Select by lis,return %s" % unicode(data))
        return data

    def select(self, sql_dict={}):
        DEBUG(u"Select,sql_dict: %s" % unicode(sql_dict))
        data = []
        label_list = [i for i, j in self.table_info]
        label_str = u",".join(label_list)
        sql = u""
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
            data.reverse()
            DEBUG(u"Select,Sql: %s data: %s" % (sql, unicode(data)))
        except Exception, e:
            ERROR(u"Select,Sql: %s failed: %s" % (sql, traceback.format_exc()))
        self.close()
        DEBUG(u"Select,return %s" % unicode(data))
        return data

    def add(self, sql_list):
        DEBUG(u"Add,sql_list:%s" % str(sql_list))
        status = 0
        label_list = [i for i, j in self.table_info]
        label_str = u",".join(label_list)
        sql = u""
        try:
            number = u",".join(["'%s'"] * len(sql_list))
            sql = u"insert into %s(%s) values(%s)" % (self.table_name, label_str, number)
            sql = sql % tuple(sql_list)
            self.cur.execute(sql)
            self.conn.commit()
            DEBUG(u"Add,Sql: %s" % sql)
        except Exception, e:
            ERROR(u"Add,Sql: %s failed: %s" % (sql, traceback.format_exc()))
            status = 1
        self.close()
        DEBUG(u"Add,return %s" % str(status))
        return status

    def update_by_stuid(self, stu_id, flag, value):
        DEBUG(u"Update by stuid,stu_id: %s, flag: %s, value: %s" % (unicode(stu_id), unicode(flag), unicode(value)))
        status = 0
        try:
            sql = u"update %s set %s='%s' where 学号='%s'"% (self.table_name, flag, value, stu_id)
            self.cur.execute(sql)
            self.conn.commit()
            DEBUG(u"Update by stuid,Sql: %s" % sql)
        except Exception, e:
            status = 1
            ERROR(u"Update by stuid,Sql: %s failed: %s" % (sql, traceback.format_exc()))
        self.close()
        DEBUG(u"Update by stuide,return %s" % str(status))
        return status

    def update(self, old_list, new_list):
        DEBUG(u"Update,old_list: %s, new_list: %s" % (unicode(old_list), unicode(new_list)))
        status = 0
        if len(old_list) != len(new_list):
            return 1
        if len(old_list) == 0 and len(new_list) == 0:
            return 1
        base_info = read_file("%s.txt" % self.table_name)
        stu_id = old_list[0]
        sql = u""
        try:
            for i in range(0, len(old_list)):
                if old_list[i] != new_list[i]:
                    sql = u"update %s set %s='%s' where 学号='%s'"%\
                          (self.table_name, base_info[i][0], new_list[i], stu_id)
                    self.cur.execute(sql)
                    self.conn.commit()
                    DEBUG(u"Update,Sql: %s" % sql)
                    if i == 0:
                        stu_id = new_list[0]
        except Exception, e:
            ERROR(u"Update,Sql: %s failed: %s" % (sql, traceback.format_exc()))
        self.close()
        DEBUG(u"Update,return %s" % str(status))
        return status

    def delete(self, stu_id):
        DEBUG(u"Delete,stu_id:%s" % unicode(stu_id))
        status = 0
        try:
            sql = u"delete from %s where 学号='%s'" % (self.table_name, stu_id)
            self.cur.execute(sql)
            self.conn.commit()
            DEBUG(u"Delete,Sql: %s" % sql)
        except Exception, e:
            ERROR(u"Delete,Sql: %s failed: %s" % (sql, traceback.format_exc()))
            status = 1
        self.close()
        DEBUG(u"Delete,return %s" % str(status))
        return status


def init_stu_term_info():
    DEBUG(u"Init stu term info.")
    infos = Sql().select()
    for info in infos:
        Sql().update_by_stuid(info[0], u"备注", u"未报到")


def select_addmoney_by_stu(value_list1=[], value_list2=[], dict1={}, dict2={}, begin='1999/01/01 00:00:00', end='2100/12/01 00:00:00'):
    DEBUG(u"Select addmoney by stu,value_list1: %s value_list2: %s dict1: %s dict2: %s begin: %s end: %s" % (
    unicode(value_list1), unicode(value_list2), unicode(dict1), unicode(dict2), begin, end))
    begin = str_to_time(begin)
    end = str_to_time(end)
    Sql("stu_base_info").close()
    Sql("stu_addmoney_info").close()
    sql = Sql()
    if len(value_list1) == 0 and len(value_list2) == 0:
        label_str = "*"
    else:
        value_list1 = [u"stu_base_info." + i for i in value_list1]
        value_list2 = [u"stu_addmoney_info." + i for i in value_list2]
        label_str = u",".join(value_list1 + value_list2)

    sql_info = u"select %s from stu_base_info, stu_addmoney_info where stu_base_info.学号=stu_addmoney_info.学号" % label_str
    if len(dict1) != 0 or len(dict2) != 0:
        select_list = []
        if len(dict1) != 0:
            for i in dict1:
                select_list.append(u"stu_base_info.%s='%s'" % (i, dict1[i]))
        if len(dict2) != 0:
            for i in dict2:
                select_list.append(u"stu_addmoney_info.%s='%s'" % (i, dict2[i]))
        sql_info = sql_info + " and " + " and ".join(select_list)
    infos = sql.select_uni(sql_info)
    res = filter(lambda x:(str_to_time(x[-1]) <= end and str_to_time(x[-1]) >= begin), infos)
    DEBUG(u"Select addmoney by stu,return: %s" % unicode(res))
    return res


def select_premoney_by_stu(value_list1=[], value_list2=[], dict1={}, dict2={}):
    DEBUG(u"Select premoney by stu,value_list1: %s value_list2: %s dict1: %s dict2: %s" % (
    unicode(value_list1), unicode(value_list2), unicode(dict1), unicode(dict2)))
    Sql("stu_base_info").close()
    Sql("stu_money_pre").close()
    sql = Sql()
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
                select_list.append(u"stu_money_pre.%s='%s'" % (i, dict2[i]))
        sql_info = sql_info + " and " + " and ".join(select_list)
    res = sql.select_uni(sql_info)
    DEBUG(u"Select premoney by stu,return: %s" % unicode(res))
    return res


def select_money_by_stu(value_list1=[], value_list2=[], dict1={}, dict2={}):
    DEBUG(u"Select money by stu,value_list1: %s value_list2: %s dict1: %s dict2: %s" % (
    unicode(value_list1), unicode(value_list2), unicode(dict1), unicode(dict2)))
    Sql("stu_base_info").close()
    Sql("stu_money_info").close()
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
    res = sql.select_uni(sql_info)
    DEBUG(u"Select money by stu,return: %s" % unicode(res))
    return res


def delete_money(stu_id, stu_term):
    DEBUG(u"Delete money, stu_id: %s stu_term: %s" % (stu_id, stu_term))
    db_name = u"stu_money_info"
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    status = 0
    sql = u""
    try:
        sql = u"delete from %s where 学号='%s' and 学期='%s'" % (db_name, stu_id, stu_term)
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        ERROR(u"Delete money,sql: %s failed: %s" % (sql, traceback.format_exc()))
        status = 1
    cur.close()
    conn.close()
    DEBUG(u"Delete money,return %s" % unicode(status))
    return status


def delete_addmoney(stu_id, stu_term):
    DEBUG(u"Delete addmoney, stu_id: %s stu_term: %s" % (stu_id, stu_term))
    db_name = u"stu_addmoney_info"
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    status = 0
    sql = u""
    try:
        sql = u"delete from %s where 学号='%s' and 学期='%s'" % (db_name, stu_id, stu_term)
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        ERROR(u"Delete addmoney,sql: %s failed: %s" % (sql, traceback.format_exc()))
        status = 1
    cur.close()
    conn.close()
    DEBUG(u"Delete addmoney,return %s" % unicode(status))
    return status


def updata_addmoney(old_list, new_list):
    DEBUG(u"Updata addmoney, old_list: %s new_list: %s" % (unicode(old_list), unicode(new_list)))
    db_name = u"stu_addmoney_info"
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    status = 0
    sql = u""
    try:
        sql = u"update %s set 缴费情况='%s',缴费时间='%s',金额='%s' where 学号='%s' and 学期='%s' and 费用期间='%s' and 种类='%s'" % (
        db_name, new_list[4], new_list[6], new_list[3], old_list[0], old_list[1], old_list[2], old_list[5])
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        ERROR(u"Updata addmoney,,sql: %s failed: %s" % (sql, traceback.format_exc()))
        status = 1
    cur.close()
    conn.close()
    DEBUG(u"Updata addmoney, sql: %s return: %s" % (sql, unicode(status)))
    return status


def get_number():
    number = Sql("number").select_by_list([u"number"],{u"学号":u"0"})[0][0]
    number = int(number) + 1
    Sql("number").update_by_stuid(u"0", u"number", unicode(number))
    return unicode(number)


def stu_addpre_print(stu_id, money):
    stu_name = Sql().select_by_list([u"姓名"],{u"学号": stu_id})
    if len(stu_name) == 0:
        stu_name = stu_id
    else:
        stu_name = stu_name[0][0]
    if money > 0:
        flag = u"收预收费"
        beizhu = u"收费"
    else:
        flag = u"退预收费"
        beizhu = u"退费"

    money = str(round(money, 2))
    head_html = u"""
<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf8" />
    <head>
        <title>成都市双流区阳光幼儿园</title>
    </head>
"""
    day_time = datetime.datetime.today()
    body_html = u"""
    <h1 align="center">成都市双流区阳光幼儿园预收费</h1>
    <body>
      <table>
        <tr>
          <th width="50%" align="left">学生姓名：name</th>
          <th width="10%" align="left"> year 年</th>
          <th width="10%" align="left"> month 月</th>
          <th width="10%" align="left"> day 日</th>
          <th width="20%" align="left">NO: number </th>
        </tr>
      </table>
      <table border="1" cellspacing="1" cellpadding="0">
        <tr>
          <th rowspan=2 width="45%"><font size="4">摘要</font></th>
          <th rowspan=2 width="5%"><font size="4">单位</font></th>
          <th rowspan=2 width="5%"><font size="4">数量</font></th>
          <th rowspan=2 width="10%"><font size="4">单价</font></th>
          <th colspan=8 width="30%"><font size="4">金额</font></th>
          <th rowspan=2 width="5%"><font size="4">备注</font></th>
        </tr>
        <tr>
          <th>十</th>
          <th>万</th>
          <th>千</th>
          <th>百</th>
          <th>十</th>
          <th>元</th>
          <th>角</th>
          <th>分</th>
        </tr>
"""
    number = get_number()
    body_html = body_html.replace(u"year", str(day_time.year)).replace(u"month", str(day_time.month)).replace(u"day", str(
        day_time.day)).replace(u"number", number).replace(u"name", stu_name)

    row_html = u""

    row_html_tmp = u"""
       <tr>
          <td name="zhaiyao" height="100">%s</td>
          <td name="danwei" height="100"></td>
          <td name="shuliang" height="100"></td>
          <td name="danjia" height="100">%s</td>
          <td name="shiwan" height="100">%s</td>
          <td name="wan" height="100">%s</td>
          <td name="qian" height="100">%s</td>
          <td name="bai" height="100">%s</td>
          <td name="shi" height="100">%s</td>
          <td name="yuan" height="100">%s</td>
          <td name="jiao" height="100">%s</td>
          <td name="fei" height="100">%s</td>
          <td name="beizhu" height="100">%s</td>
        </tr>
"""
    out_put_list = out_put_money_list(float(money))
    out_put_list = [flag, money] + out_put_list + [beizhu]
    row_html = row_html + row_html_tmp % tuple(out_put_list)
    for j in range(0, 14):
        row_html = row_html + row_html_tmp % (u' ', u' ', u' ', u' ', u' ', u' ', u' ', u' ',u' ',u' ',u' ')
    row_html_tmp = u"""
        <tr>
          <td colspan=4>合计(人民币)：%s 拾 %s 万 %s 仟 %s 佰 %s 拾 %s 元 %s 角 %s 分</td>
          <td name="shiwan">%s</td>
          <td name="wan">%s</td>
          <td name="qian">%s</td>
          <td name="bai">%s</td>
          <td name="shi">%s</td>
          <td name="yuan">%s</td>
          <td name="jiao">%s</td>
          <td name="fei">%s</td>
          <td name="beizhu"><font size="4">%s</font></td>
        </tr>
"""
    money_list = out_put_money_list(float(money))
    money_list_ch = out_put_money_list_ch(money_list)
    row_html = row_html + row_html_tmp % tuple(money_list_ch + money_list + [beizhu])
    row_html_tmp = u"""
      </table>
      <table>
        <tr>
          <th width="30%" align="left">填票人：name</th>
          <th width="30%" align="left">收款人：name</th>
          <th width="40%" align="left">单位名称(盖章):</th>
        </tr>
      </table>
    </body>
"""
    row_html = row_html + row_html_tmp.replace(u"name", query_current_user()[1])
    blank_line = u"""
    <br />
    <br />
    <br />
    <hr />
    <br />
    <br />
    <br />
"""
    body_html = body_html + row_html
    end_html = u"""
</html>
"""
    result_html = head_html + body_html + blank_line + body_html + end_html
    write_file(number, result_html)
    return result_html


def stu_addflowing_print(num):
    flowing_info = Sql("flow_money_sel").select_by_list([u"学号", u"金额", u"备注"],{u"num": num})[0]
    stu_id = flowing_info[0]
    stu_name = Sql().select_by_list([u"姓名"],{u"学号": stu_id})
    if len(stu_name) == 0:
        stu_name = stu_id
    else:
        stu_name = stu_name[0][0]
    money = flowing_info[1]
    flag = flowing_info[2]
    head_html = u"""
<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf8" />
    <head>
        <title>成都市双流区阳光幼儿园</title>
    </head>
"""
    day_time = datetime.datetime.today()
    body_html = u"""
    <h1 align="center">成都市双流区阳光幼儿园退费票据</h1>
    <body>
      <table>
        <tr>
          <th width="50%" align="left">学生姓名：name</th>
          <th width="10%" align="left"> year 年</th>
          <th width="10%" align="left"> month 月</th>
          <th width="10%" align="left"> day 日</th>
          <th width="20%" align="left">NO: number </th>
        </tr>
      </table>
      <table border="1" cellspacing="1" cellpadding="0">
        <tr>
          <th rowspan=2 width="45%"><font size="4">摘要</font></th>
          <th rowspan=2 width="5%"><font size="4">单位</font></th>
          <th rowspan=2 width="5%"><font size="4">数量</font></th>
          <th rowspan=2 width="10%"><font size="4">单价</font></th>
          <th colspan=8 width="30%"><font size="4">金额</font></th>
          <th rowspan=2 width="5%"><font size="4">备注</font></th>
        </tr>
        <tr>
          <th>十</th>
          <th>万</th>
          <th>千</th>
          <th>百</th>
          <th>十</th>
          <th>元</th>
          <th>角</th>
          <th>分</th>
        </tr>
"""
    number = get_number()
    body_html = body_html.replace(u"year", str(day_time.year)).replace(u"month", str(day_time.month)).replace(u"day", str(
        day_time.day)).replace(u"number", number).replace(u"name", stu_name)

    row_html = u""

    row_html_tmp = u"""
       <tr>
          <td name="zhaiyao" height="100">%s</td>
          <td name="danwei" height="100"></td>
          <td name="shuliang" height="100"></td>
          <td name="danjia" height="100">%s</td>
          <td name="shiwan" height="100">%s</td>
          <td name="wan" height="100">%s</td>
          <td name="qian" height="100">%s</td>
          <td name="bai" height="100">%s</td>
          <td name="shi" height="100">%s</td>
          <td name="yuan" height="100">%s</td>
          <td name="jiao" height="100">%s</td>
          <td name="fei" height="100">%s</td>
          <td name="beizhu" height="100">%s</td>
        </tr>
"""
    out_put_list = out_put_money_list(float(money))
    out_put_list = [flag, money] + out_put_list + [u"退费"]
    row_html = row_html + row_html_tmp % tuple(out_put_list)
    for j in range(0, 14):
        row_html = row_html + row_html_tmp % (u' ', u' ', u' ', u' ', u' ', u' ', u' ', u' ',u' ',u' ',u' ')
    row_html_tmp = u"""
        <tr>
          <td colspan=4>合计(人民币)：%s 拾 %s 万 %s 仟 %s 佰 %s 拾 %s 元 %s 角 %s 分</td>
          <td name="shiwan">%s</td>
          <td name="wan">%s</td>
          <td name="qian">%s</td>
          <td name="bai">%s</td>
          <td name="shi">%s</td>
          <td name="yuan">%s</td>
          <td name="jiao">%s</td>
          <td name="fei">%s</td>
          <td name="beizhu"><font size="4">%s</font></td>
        </tr>
"""
    money_list = out_put_money_list(float(money))
    beizhu = u"退费"
    money_list_ch = out_put_money_list_ch(money_list)
    row_html = row_html + row_html_tmp % tuple(money_list_ch + money_list + [beizhu])
    row_html_tmp = u"""
      </table>
      <table>
        <tr>
          <th width="30%" align="left">填票人：name</th>
          <th width="30%" align="left">收款人：name</th>
          <th width="40%" align="left">单位名称(盖章):</th>
        </tr>
      </table>
    </body>
"""
    row_html = row_html + row_html_tmp.replace(u"name", query_current_user()[1])
    blank_line = u"""
    <br />
    <br />
    <br />
    <hr />
    <br />
    <br />
    <br />
"""
    body_html = body_html + row_html
    end_html = u"""
</html>
"""
    result_html = head_html + body_html + blank_line + body_html + end_html
    write_file(number, result_html)
    return result_html


def stu_addmoney_print(old_values=[], values=[], premoney=0):
    stu_id = values[0]
    stu_name = Sql().select_by_list([u"姓名"],{u"学号": stu_id})
    if len(stu_name) == 0:
        stu_name = stu_id
    else:
        stu_name = stu_name[0][0]
    head_html = u"""
<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf8" />
    <head>
        <title>成都市双流区阳光幼儿园</title>
    </head>
"""
    day_time = datetime.datetime.today()
    body_html = u"""
    <h1 align="center">成都市双流区阳光幼儿园收据</h1>
    <body>
      <table>
        <tr>
          <th width="50%" align="left">学生姓名：name</th>
          <th width="10%" align="left"> year 年</th>
          <th width="10%" align="left"> month 月</th>
          <th width="10%" align="left"> day 日</th>
          <th width="20%" align="left">NO: number </th>
        </tr>
      </table>
      <table border="1" cellspacing="1" cellpadding="0">
        <tr>
          <th rowspan=2 width="45%"><font size="4">摘要</font></th>
          <th rowspan=2 width="5%"><font size="4">单位</font></th>
          <th rowspan=2 width="5%"><font size="4">数量</font></th>
          <th rowspan=2 width="10%"><font size="4">单价</font></th>
          <th colspan=8 width="30%"><font size="4">金额</font></th>
          <th rowspan=2 width="5%"><font size="4">备注</font></th>
        </tr>
        <tr>
          <th>十</th>
          <th>万</th>
          <th>千</th>
          <th>百</th>
          <th>十</th>
          <th>元</th>
          <th>角</th>
          <th>分</th>
        </tr>
"""
    number = get_number()
    body_html = body_html.replace(u"year", str(day_time.year)).replace(u"month", str(day_time.month)).replace(u"day", str(
        day_time.day)).replace(u"number", number).replace(u"name", stu_name)

    row_html = u""

    row_html_tmp = u"""
       <tr>
          <td name="zhaiyao" height="100">%s</td>
          <td name="danwei" height="100"></td>
          <td name="shuliang" height="100"></td>
          <td name="danjia" height="100">%s</td>
          <td name="shiwan" height="100">%s</td>
          <td name="wan" height="100">%s</td>
          <td name="qian" height="100">%s</td>
          <td name="bai" height="100">%s</td>
          <td name="shi" height="100">%s</td>
          <td name="yuan" height="100">%s</td>
          <td name="jiao" height="100">%s</td>
          <td name="fei" height="100">%s</td>
          <td name="beizhu" height="100">%s</td>
        </tr>
"""
    status = 0
    #values [(u'20180001', u'201803', u'1200', u'100,100,100', u'60,60,60', u'1200', u'1300')]
    flags = read_file("stu_money_info.txt")
    if len(values) < 2:
        return 0
    i = -1
    num = 15
    sum = 0
    for flag, value in flags:
        i = i + 1
        if value[0] == u"":
            continue
        if len(old_values) == 0:
            sum = sum + str_to_sum(values[i])
            out_put_list = out_put_result(values[i])
        else:
            sum = sum + str_to_sum(values[i]) - str_to_sum(old_values[i])
            out_put_list = out_put_result(values[i], old_values[i])
        if out_put_list == 0:
            continue
        out_put_list = [flag + "(" + out_put_list[0] + ")"] + out_put_list[1:]
        row_html = row_html + row_html_tmp % tuple(out_put_list)
    if premoney != 0:
        pre_list = [u"抵扣预收费用", str(-premoney)] + out_put_money_list(premoney) + [u"抵扣"]
        row_html = row_html + row_html_tmp % tuple(pre_list)
        i = i + 1
    for j in range(0, num - i):
        row_html = row_html + row_html_tmp % (u' ', u' ', u' ', u' ', u' ', u' ', u' ', u' ',u' ',u' ',u' ')
    row_html_tmp = u"""
        <tr>
          <td colspan=4>合计(人民币)：%s 拾 %s 万 %s 仟 %s 佰 %s 拾 %s 元 %s 角 %s 分</td>
          <td name="shiwan">%s</td>
          <td name="wan">%s</td>
          <td name="qian">%s</td>
          <td name="bai">%s</td>
          <td name="shi">%s</td>
          <td name="yuan">%s</td>
          <td name="jiao">%s</td>
          <td name="fei">%s</td>
          <td name="beizhu"><font size="4">%s</font></td>
        </tr>
"""
    sum = sum - premoney
    money_list = out_put_money_list(sum)
    if sum >= 0:
        beizhu = u"缴费"
    else:
        beizhu = u"退费"
    money_list_ch = out_put_money_list_ch(money_list)
    row_html = row_html + row_html_tmp % tuple(money_list_ch + money_list + [beizhu])
    row_html_tmp = u"""
      </table>
      <table>
        <tr>
          <th width="30%" align="left">填票人：name</th>
          <th width="30%" align="left">收款人：name</th>
          <th width="40%" align="left">单位名称(盖章):</th>
        </tr>
      </table>
    </body>
"""
    row_html = row_html + row_html_tmp.replace(u"name", query_current_user()[1])
    blank_line = u"""
    <br />
    <br />
    <br />
    <hr />
    <br />
    <br />
    <br />
"""
    body_html = body_html + row_html
    end_html = u"""
</html>
"""
    result_html = head_html + body_html + blank_line + body_html + end_html
    write_file(number, result_html)
    return result_html


def write_file(filename, content):
    import codecs
    try:
        f = codecs.open(os.path.join(get_cwd(),"backup","%s.html" % str(filename)), "w", "utf-8")
        f.write(content)
        f.close()
    except Exception,e:
        ERROR(traceback.format_exc())


def print_html(html):
    printer = QtGui.QPrinter()
    textDocument = QtGui.QTextDocument()
    textDocument.setHtml(html)
    textDocument.print_(printer)


def out_put_money_list_ch(result):
    flag_dict = {u"1": u"壹", u"2":u"贰", u"3":u"叁", u"4":u"肆", u"5":u"伍", u"6":u"陆", u"7":u"柒", u"8":u"捌", u"9":u"玖",u"0":u"零",u"￥":u"零"}
    result = [flag_dict[i] for i in result]
    return result


def out_put_term(str, old_str=NULL_VALUE):
    term_info = read_file("money_term.txt")[0][1]
    term_info = [i for i in term_info]
    infos = str.split(",")
    old_infos = old_str.split(",")
    if len(infos) == 1:
        if old_str == NULL_VALUE:
            old_str = u"0"
        if float(str) > float(old_str):
            term_info = [u"缴费"]
            return ",".join(term_info)
        else:
            term_info = [u"退费"]
            return ",".join(term_info)
    i = 0
    tmp = []
    for info in infos:
        if float(old_infos[i]) > float(infos[i]):
            tmp.append(u"退" + term_info[i])
        if float(old_infos[i]) < float(infos[i]):
            tmp.append(u"缴"+ term_info[i])
        i = i + 1
    return ",".join(tmp)


def out_put_result(new_str="0", old_str="0"):
    if "," in new_str:
        old_str = NULL_VALUE
    money = str_to_sum(new_str) - str_to_sum(old_str)
    if new_str == old_str:
        return 0
    f_beizhu = u" "
    if money > 0:
        f_beizhu = u"缴费"
    if money < 0:
        f_beizhu = u"退费"
    return [out_put_term(new_str, old_str), str(round(money, 2))] + out_put_money_list(money) + [f_beizhu]


def out_put_money_list(money):
    num_i = 6
    num_f = 2
    list_value = []
    money = abs(money)
    money = round(money, num_f)
    money_int = int(money)
    money_float = int((money - money_int) * (10 ** num_f))
    for i in range(1, num_f + 1):
        tmp = money_float % 10
        money_float = money_float / 10
        list_value.append(tmp)
    for i in range(1, num_i + 1):
        tmp = money_int % 10
        money_int = money_int / 10
        list_value.append(tmp)
    list_value.reverse()
    result = []
    flag = 0
    for i in range(0, len(list_value)):
        if i < (len(list_value) - 1) and list_value[i + 1] != 0 and flag == 0:
            flag = 1
            result.append(u"￥")
        elif i == (len(list_value) - 1) and list_value[i] == 0 and flag == 0:
            flag = 1
            result.append(u"￥")
        else:
            result.append(str(list_value[i]))
    return result


def stu_addmoney_add(values=[]):
    DEBUG(u"Stu addmoney add, values: %s" % unicode(values))
    db_name = "stu_addmoney_info"
    #values [(u'20180001', u'201803', u'1200', u'100,100,100', u'60,60,60', u'1200', u'1300')]
    flags = read_file("stu_money_info.txt")
    if len(values) < 2:
        return 0
    stu_id = values[0]
    stu_term = values[1]
    i = 2
    status = 0
    for items in values[2:]:
        flag = flags[i][0]
        f_values = flags[i][1]
        if len(f_values) == 1:
            old_list = Sql(db_name).select({u"学号": stu_id, u"学期": stu_term, u"种类": flag})
            if items != u"0":
                f_status = u"已缴费"
                if len(old_list) != 0 and old_list[0][4] == u"已缴费":
                    create_time = old_list[0][-1]
                else:
                    create_time = time_to_str(time.time())
            else:
                f_status = u"未缴费"
                create_time = u"2000/01/01 00:00:00"
            new_list = [stu_id, stu_term, u"All", f_values[0], f_status, flag, create_time]
            if len(old_list) != 0:
                old_list = old_list[0]
                status = updata_addmoney(old_list, new_list)
            else:
                status = Sql(db_name).add(new_list)
        else:
            j = 1
            for item in items.split(u","):
                f_value_flag = f_values[j]
                old_list = Sql(db_name).select({u"学号": stu_id, u"学期": stu_term, u"种类": flag, u"费用期间": f_value_flag})
                if item != u"0":
                    f_status = u"已缴费"
                    if len(old_list) != 0 and old_list[0][4] == u"已缴费":
                        create_time = old_list[0][-1]
                    else:
                        create_time = time_to_str(time.time())
                else:
                    f_status = u"未缴费"
                    create_time = u"2000/01/01 00:00:00"
                new_list = [stu_id, stu_term, f_value_flag, f_values[0], f_status, flag, create_time]
                if len(old_list) != 0:
                    old_list = old_list[0]
                    status = updata_addmoney(old_list, new_list)
                else:
                    status = Sql(db_name).add(new_list)
                j = j + 1
        i = i + 1
    DEBUG(u"Stu addmoney add, return %s" % unicode(status))
    return status


def add_flowing(object, value="0", stu_id=u"", info=u""):
    INFO(u"Add flowing, value: %s, stu_id: %s, info: %s" % (unicode(value), unicode(stu_id), unicode(info)))
    msg = u""
    if float(value) < 0:
        msg = showInputDialog(object, u"请记录退费原因：")
    flow_flag_list = [i for i, j in read_file("flow_money_sel.txt")]
    stuInfo = Sql("flow_money_sel").select_by_list()
    num = str(len(stuInfo) + 1)
    data_info = Sql().select_by_list(flow_flag_list[1:5], {u"学号": stu_id})[0]
    values = [num] + list(data_info) + [time_to_str(time.time()), value, info, msg]
    status = Sql("flow_money_sel").add(values)
    if status == 1:
        res = -1
    else:
        res = num
    DEBUG(u"Add flowing, return %s" % unicode(res))
    return res


def flow_select_time(flag_list=[], value_dict={}, begin='1999/01/01 00:00:00', end='2100/12/01 00:00:00'):
    DEBUG(u"Flow select time,flag_list: %s,value_dict: %s,begin: %s,end: %s" % (
    unicode(flag_list), unicode(value_dict), unicode(begin), unicode(end)))
    if flag_list == []:
        return 0
    begin = str_to_time(begin)
    end = str_to_time(end)
    infos = Sql("flow_money_sel").select_by_list(flag_list, value_dict)
    res = filter(lambda x:(str_to_time(x[4]) <= end and str_to_time(x[4]) >= begin), infos)
    DEBUG(u"Flow select time,return: %s" % unicode(res))
    return res


def time_to_str(l_time):
    res = u""
    try:
        res = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(l_time))
    except Exception, e:
        ERROR(u"Time to str, failed: %s" % traceback.format_exc())
    DEBUG(u"Time to str, l_time: %s, return: %s" %(unicode(l_time), unicode(res)))
    return res


def str_to_time(str):
    res = 0
    try:
        res = time.mktime(time.strptime(str, '%Y/%m/%d %H:%M:%S'))
    except Exception, e:
        ERROR(u"Str to time, failed: %s" % traceback.format_exc())
    DEBUG(u"Str to time, str: %s, return: %s" % (unicode(str), unicode(res)))
    return res


def get_tommor_date():
    res = QtCore.QDate(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day + 1)
    DEBUG(u"Get tommor date,return: %s" % unicode(res))
    return res


def get_current_year():
    res = QtCore.QDate(datetime.datetime.now().year, 1, 1)
    DEBUG(u"Get tommor date,return: %s" % unicode(res))
    return res


def get_text(object):
    res = unicode(object)
    if isinstance(object, QtGui.QDateEdit):
        res = unicode(object.text())
    if isinstance(object, QtGui.QLineEdit):
        res = unicode(object.text())
    if isinstance(object, QtGui.QComboBox):
        res = unicode(object.currentText())
    DEBUG(u"Get text,object: %s, return: %s" % (unicode(object), unicode(res)))
    return res


def clear_text(object):
    if isinstance(object, QtGui.QDateEdit):
        if object.isEnabled():
            object.setDate(QtCore.QDate(datetime.datetime.now().year - 3, 1, 1))
        else:
            object.setDate(QtCore.QDate.currentDate())
    if isinstance(object, QtGui.QLineEdit):
        object.clear()
    if isinstance(object, QtGui.QComboBox):
        object.setCurrentIndex(0)
    DEBUG(u"Clear text,object: %s" % unicode(object))


def get_flag_list(db_name, flag):
    DEBUG(u"Get flag list,db_name: %s, flag: %s" % (unicode(db_name), unicode(flag)))
    infos = Sql(db_name).select_by_list([flag])
    infos = map(lambda x:x[0], infos)
    infos = list(set(infos))
    infos.sort()
    DEBUG(u"Get flag list,return: %s" % unicode(infos))
    return infos


def choose_dirname():
    root = Tkinter.Tk()
    root.withdraw()
    options = {}
    options['initialdir'] = os.path.join(get_cwd(), "download")
    dir_name = tkFileDialog.askdirectory(**options)
    DEBUG(u"Choose dirname,return: %s" % unicode(dir_name))
    return dir_name


def choose_filepath():
    root = Tkinter.Tk()
    root.withdraw()
    options = {}
    options['defaultextension'] = '.xls'
    options['initialdir'] = os.path.join(get_cwd(), "download")
    options['filetypes'] = [('Excel files', '*.xls'), ('all files', '.*')]
    filepath = tkFileDialog.askopenfilename(**options)
    DEBUG(u"Choose filepath,return: %s" % unicode(filepath))
    return filepath


def save_file():
    root = Tkinter.Tk()
    root.withdraw()
    options = {}
    options['defaultextension'] = '.xls'
    options['initialdir'] = os.path.join(get_cwd(), "download")
    options['initialfile'] = '%d.xls' % int(time.time())
    options['filetypes'] = [('all files', '.*'), ('Excel files', '*.xls')]
    filepath = tkFileDialog.asksaveasfilename(**options)
    DEBUG(u"Save file,return: %s" % unicode(filepath))
    return filepath


def write_xls(file_name, flag_list, infos):
    status = 0
    DEBUG(u"Write xls,file_name: %s, flag_list: %s, infos: %s" % (unicode(file_name), unicode(flag_list), unicode(infos)))
    try:
        df = pd.DataFrame(data=infos, columns=flag_list)
        df.to_excel(file_name, index=False)
    except Exception, e:
        status = 1
        ERROR(u"Write xls,failed: %s" % traceback.format_exc())
    DEBUG(u"Write xls,return: %s" % unicode(status))
    return status


def class_map(class_name):
    class_map_info = {i:j[0] for i,j in read_file("class_map.txt")}
    if class_map_info.has_key(class_name):
        return class_map_info[class_name]
    return u""


def address_map(address_info):
    address_map_info = read_file_dict("address_map.txt")
    for i in range(len(address_info), 0, -1):
        for j in range(i-1, -1, -1):
            if address_map_info.has_key(address_info[j:i]):
                return address_map_info[address_info[j:i]]
    return u""


def read_file_dict(file_name):
    return {i:j[0] for i,j in read_file(file_name)}


def str_to_date(str):
    res = 0
    try:
        res = time.mktime(time.strptime(str, '%Y/%m/%d'))
    except Exception, e:
        ERROR(u"Str to time, failed: %s" % traceback.format_exc())
    DEBUG(u"Str to time, str: %s, return: %s" % (unicode(str), unicode(res)))
    return res


def get_age(date_str):
    try:
        result = str(int((time.time() - str_to_date(date_str)) / (3600 * 24 * 360)))
    except Exception, e:
        result = "0"
    return result


def write_xls_by_sort(file_name, flag_list, infos, sort_list):
    status = 0
    DEBUG(u"Write xls,file_name: %s, flag_list: %s, infos: %s" % (unicode(file_name), unicode(flag_list), unicode(infos)))
    try:
        df = pd.DataFrame(data=infos, columns=flag_list)
        df[u"年龄"] = df[u"出生年月"].map(get_age)
        df_result = df[sort_list]
        df_result.to_excel(file_name, index=False)
    except Exception, e:
        status = 1
        ERROR(u"Write xls,failed: %s" % traceback.format_exc())
    DEBUG(u"Write xls,return: %s" % unicode(status))
    return status


def read_xls(file_name):
    DEBUG(u"Read xls,file_name: %s" % unicode(file_name))
    res = []
    try:
        df = pd.read_excel(file_name,sheet_name=0)
        df[u"联系电话"] = df[u"联系电话"].map(float_to_int_str)
        df[u"年龄"] = df[u"年龄"].map(float_to_int_str)
        res = df.values.tolist()
    except Exception, e:
        ERROR(u"Read xls,failed: %s" % traceback.format_exc())
    DEBUG(u"Read xls,return: %s" % unicode(res))
    return res


def clear_df_list(x):
    y = unicode(x)
    if y == u"nan":
        return u""
    else:
        return y


def float_to_int_str(x):
    y = unicode(x)
    if y == u"nan":
        return u""
    try:
        result = str(int(x))
    except Exception, e:
        result = str(x)
    return result


def update_stu(new_lists):
    DEBUG(u"Update stu,new_lists: %s" % unicode(new_lists))
    error_list = []
    for new_list in new_lists:
        new_list = map(clear_df_list, new_list)
        old_list = Sql().select({u"学号":new_list[0]})
        if len(old_list) == 0:
            status = Sql().add(new_list)
        else:
            status = Sql().update(old_list[0], new_list)
        if status == 1:
            error_list.append(new_list[0])
    DEBUG(u"Update stu,return: %s" % unicode(error_list))
    return error_list


def get_pic_size(file_name):
    w = 500
    h = 500
    try:
        im = Image.open(file_name)
        w, h = im.size
    except Exception, e:
        ERROR(u"Get pic size,file_name: %s can not read: %s" %(file_name, traceback.format_exc()))
    DEBUG(u"Get pic size,file_name: %s success! return %d %d" % (file_name, w, h))
    return w, h


def get_stu_money(stu_id):
    money_info = Sql("stu_money_info").select({u"学号": stu_id})
    if len(money_info) == 0:
        total = 0.0
    else:
        money_info = money_info[0]
    total = sum(map(str_to_sum, money_info[2:]))
    DEBUG(u"Get stu money,stu_id: %s success! return %8.2f" % (stu_id, total))
    return total


def get_stu_infos(flag_list=[], stu_name=u""):
    infos = Sql().select_by_list(flag_list)
    infos = filter(lambda x: stu_name in x[1], infos)
    return infos


if __name__ == '__main__':
    # showInputDialog()
    # test = Sql("stu_money_info")
    # # sql = "alter table stu_money_info add column name text;"
    # sql = "select * from {};".format("stu_money_info")
    # test.cur.execute(sql)
    # print test.cur.description
    # # test.conn.commit()
    # test.close()
    # print select_addmoney_by_stu(value_list1=[u"学号"], value_list2=[u"生活费"], dict1={u"学号": u"20180007"}, dict2={u"生活费": "0"})
    # get_flag_list("stu_addmoney_info", u"班级")
    # print choose_dirname()
    # tkFileDialog.asksaveasfilename(**self.file_opt)
    # print read_xls(os.path.join(os.getcwd(), "download", "test.xls"))
    # print choose_filepath()
    # # print showInputDialog()
    # im = Image.open("icon/start.png")  # 返回一个Image对象
    # print im.size
    # print('宽：%d,高：%d' % (im.size[0], im.size[1]))
    # test = Sql("stu_money_info")
    # get_stu_infos([u"学号",u"姓名",u"联系电话",u"身份证件号码"], u"f")
    # print init_stu_term_info()
    # test = stu_addmoney_print([u'20180001', u'201803', u'1200', u'100,100,0', u'60,60,0', u'1200', u'1300'], [u'20180001', u'201803', u'1200', u'100,100,100', u'60,60,60', u'1200', u'1300'])
    # print_html(test)
    print get_age("1987/07/02")
