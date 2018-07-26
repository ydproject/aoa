# -*- coding: utf-8 -*-

import sqlite3
import os
from PyQt4 import QtGui, QtCore
import time, datetime
import Tkinter, tkFileDialog
import traceback
import pandas as pd
from log import INFO, ERROR, WARN


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
    INFO("Get term info: %s" % term)
    return term


def query_current_user():
    user_info = Sql("current_user").select({u"学号": "0"})[0]
    INFO("Query current user: %s" % str(user_info))
    return user_info


def init_user():
    INFO("Init user: Guest")
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
            ERROR("Swith user failed.")
            return 1
        else:
            INFO("Swith user: %s" % str(data[0][1]))
            return data[0][1]
    WARN("Swith user failed: user or passwd error!")
    return 1


def get_user_id():
    t_id = int(time.time())
    INFO("Get user id: %d" % t_id)
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
        INFO("Get stu id: %s" % t_id)
        return t_id
    except Exception, e:
        t_id = int(time.time())
        ERROR("Get stu id failed: %s. Output: %d" % (traceback.format_exc(), t_id))
        return t_id


def str_to_sum(str):
    try:
        sum = reduce(lambda x,y:x+y, map(float, str.split(",")))
        INFO("Str to sum: %f" % sum)
        return sum
    except Exception,e:
        ERROR("Str to sum failed: %s. Output: 0" % traceback.format_exc())
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


def select_addmoney_by_stu(value_list1=[], value_list2=[], dict1={}, dict2={}, begin='1999/01/01 00:00:00', end='2100/12/01 00:00:00'):
    begin = str_to_time(begin)
    end = str_to_time(end)
    sql = Sql(u"stu_base_info")
    sql = Sql(u"stu_addmoney_info")
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
    return filter(lambda x:(str_to_time(x[-1]) <= end and str_to_time(x[-1]) >= begin), infos)


def select_premoney_by_stu(value_list1=[], value_list2=[], dict1={}, dict2={}):
    sql = Sql(u"stu_base_info")
    sql = Sql(u"stu_money_pre")
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


def delete_addmoney(stu_id, stu_term):
    db_name = u"stu_addmoney_info"
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    status = 0
    try:
        sql = u"delete from %s where 学号='%s' and 学期='%s'" % (db_name, stu_id, stu_term)
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        print traceback.format_exc()
        status = 1
    cur.close()
    conn.close()
    return status


def updata_addmoney(old_list, new_list):
    db_name = u"stu_addmoney_info"
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    status = 0
    try:
        sql = u"update %s set 缴费情况='%s',缴费时间='%s',金额='%s' where 学号='%s' and 学期='%s' and 费用期间='%s' and 种类='%s'" % (db_name, new_list[4],new_list[6],new_list[3],old_list[0], old_list[1], old_list[2], old_list[5])
        cur.execute(sql)
        conn.commit()
    except Exception, e:
        print traceback.format_exc()
        status = 1
    cur.close()
    conn.close()
    return status


def stu_addmoney_add(values=[]):
    db_name = u"stu_addmoney_info"
    #values [(u'20180001', u'201803', u'1200', u'100,100,100', u'60,60,60', u'1200', u'1300')]
    flags = read_file("stu_money_info.txt")
    if len(values) < 2:
        return 0
    stu_id = values[0]
    stu_term = values[1]
    i = 2
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
                f_status = u"未交费"
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
                    f_status = u"未交费"
                    create_time = u"2000/01/01 00:00:00"
                new_list = [stu_id, stu_term, f_value_flag, f_values[0], f_status, flag, create_time]
                if len(old_list) != 0:
                    old_list = old_list[0]
                    status = updata_addmoney(old_list, new_list)
                else:
                    status = Sql(db_name).add(new_list)
                j = j + 1
        i = i + 1

    return status


def add_flowing(value="0", stu_id=u"", info=u""):
    flow_flag_list = [i for i, j in read_file("flow_money_sel.txt")]
    print flow_flag_list
    stuInfo = Sql("flow_money_sel").select_by_list()
    num = str(len(stuInfo) + 1)
    data_info = Sql().select_by_list(flow_flag_list[1:5], {u"学号": stu_id})[0]
    values = [num] + list(data_info) + [time_to_str(time.time()), value, info]
    print values
    status = Sql("flow_money_sel").add(values)
    if status == 1:
        return -1
    return num


def flow_select_time(flag_list=[], value_dict={}, begin='1999/01/01 00:00:00', end='2100/12/01 00:00:00'):
    if flag_list == []:
        return 0
    begin = str_to_time(begin)
    end = str_to_time(end)
    infos = Sql("flow_money_sel").select_by_list(flag_list, value_dict)
    return filter(lambda x:(str_to_time(x[4]) <= end and str_to_time(x[4]) >= begin), infos)

def time_to_str(l_time):
    return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(l_time))


def str_to_time(str):
    return time.mktime(time.strptime(str, '%Y/%m/%d %H:%M:%S'))


def get_tommor_date():
    return QtCore.QDate(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day + 1)


def get_text(object):
    if isinstance(object, QtGui.QDateEdit):
        return unicode(object.text())
    if isinstance(object, QtGui.QLineEdit):
        return unicode(object.text())
    if isinstance(object, QtGui.QComboBox):
        return unicode(object.currentText())
    return unicode(object)


def clear_text(object):
    if isinstance(object, QtGui.QDateEdit):
        if object.isEnabled():
            object.setDate(QtCore.QDate(1999, 1, 1))
        else:
            object.setDate(QtCore.QDate.currentDate())
    if isinstance(object, QtGui.QLineEdit):
        object.clear()
    if isinstance(object, QtGui.QComboBox):
        object.setCurrentIndex(0)

def get_flag_list(db_name, flag):
    infos = Sql(db_name).select_by_list([flag])
    infos = map(lambda x:x[0], infos)
    infos = list(set(infos))
    infos.sort()
    return infos


def choose_dirname():
    root = Tkinter.Tk()
    root.withdraw()
    options = {}
    options['initialdir'] = os.path.join(os.getcwd(), u"download")
    dir_name = tkFileDialog.askdirectory(**options)
    return dir_name


def choose_filepath():
    root = Tkinter.Tk()
    root.withdraw()
    options = {}
    options['defaultextension'] = '.xls'
    options['initialdir'] = os.path.join(os.getcwd(), u"download")
    options['filetypes'] = [('Excel files', '*.xls'), ('all files', '.*')]
    filepath = tkFileDialog.askopenfilename(**options)
    return filepath


def save_file():
    root = Tkinter.Tk()
    root.withdraw()
    options = {}
    options['defaultextension'] = '.xls'
    options['initialdir'] = os.path.join(os.getcwd(), u"download")
    options['initialfile'] = '%d.xls' % int(time.time())
    options['filetypes'] = [('all files', '.*'), ('Excel files', '*.xls')]
    filepath = tkFileDialog.asksaveasfilename(**options)
    return filepath


def write_xls(file_name, flag_list, infos):
    try:
        df = pd.DataFrame(data=infos, columns=flag_list)
        df.to_excel(file_name, index=False)
        return 1
    except Exception, e:
        print traceback.format_exc()
        return 0


def read_xls(file_name):
    try:
        df = pd.read_excel(file_name,sheet_name=0)
        return df.values.tolist()
    except Exception, e:
        print traceback.format_exc()
        return []


def clear_df_list(x):
    y = unicode(x)
    if y == u"nan":
        return u""
    else:
        return y


def update_stu(new_lists):
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
    return error_list


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
    print get_tommor_date()