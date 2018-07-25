#!/usr/bin/python
# -*- coding: utf-8 -*-

# boxlayout.py

import sys
from PyQt4 import QtGui, QtCore
from util import *
import addmoney, editbymoney, editmoney


class SelMoney(QtGui.QWidget):

    def __init__(self):
        super(SelMoney, self).__init__()

        self.initUI()

    def initUI(self):
        frame = QtGui.QFrame(self)
        self.select_infos = read_file("stu_selmoney_info.txt")
        self.flag_list = [item for item, item_value in self.select_infos]
        self.money_infos = read_file("stu_money_info.txt")
        self.money_list = [item for item, item_value in self.money_infos]
        # 表格控件
        self.tablelist = [u''] + self.flag_list + self.money_list[1:]
        stuInfo = Sql().select_by_list(self.flag_list, {})
        self.currentTable = stuInfo
        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setRowCount(len(stuInfo))
        self.tableWidget.setColumnCount(len(self.tablelist))
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setHorizontalHeaderLabels(self.tablelist)
        i = 0
        for row in stuInfo:
            chkBoxItem = QtGui.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 0, chkBoxItem)
            for col in range(0, len(row)):
                v = row[col]
                item = QtGui.QTableWidgetItem(v)
                self.tableWidget.setItem(i, col + 1, item)

            money_info = Sql("stu_money_info").select_by_list(self.money_list[1:], {u"学号": row[0], u"学期": get_term()})
            if len(money_info) != 0:
                for j in range(0, len(money_info[0])):
                    vj = money_info[0][j]
                    item = QtGui.QTableWidgetItem(vj)
                    self.tableWidget.setItem(i, col + j + 2, item)
            i = i + 1

        #编辑框控件
        self.label_list = []
        self.value_list = []
        for items, items_value in self.select_infos:
            label = QtGui.QLabel(items)
            self.label_list.append(label)
            if str(items_value[0]) == "1":
                edits = QtGui.QLineEdit()
            else:
                edits = QtGui.QComboBox()
                edits.addItem("")
                for item in get_flag_list("stu_base_info", items):
                    edits.addItem(item)
            self.value_list.append(edits)

        # 按钮控件
        selectButton = QtGui.QPushButton(frame)
        selectButton.setText(u'查询')
        QtCore.QObject.connect(selectButton, QtCore.SIGNAL("clicked()"), self.sels)

        editButton = QtGui.QPushButton(frame)
        editButton.setText(u'编辑')
        QtCore.QObject.connect(editButton, QtCore.SIGNAL("clicked()"), self.edit_money)
        if query_current_user()[2] != "Admin":
            editButton.setDisabled(True)
        else:
            editButton.setDisabled(False)

        modifyButton = QtGui.QPushButton(frame)
        modifyButton.setText(u'缴费')
        QtCore.QObject.connect(modifyButton, QtCore.SIGNAL("clicked()"), self.edits)
        if query_current_user()[2] == "Guest":
            modifyButton.setDisabled(True)
        else:
            modifyButton.setDisabled(False)

        deleteButton = QtGui.QPushButton(frame)
        deleteButton.setText(u'删除')
        QtCore.QObject.connect(deleteButton, QtCore.SIGNAL("clicked()"), self.dels)
        if query_current_user()[2] != "Admin":
            deleteButton.setDisabled(True)
        else:
            deleteButton.setDisabled(False)

        clearButton = QtGui.QPushButton(frame)
        clearButton.setText(u'清空')
        QtCore.QObject.connect(clearButton, QtCore.SIGNAL("clicked()"), self.clears)

        #布局vlayout = QtGui.QVBoxLayout()
        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)

        i = 0
        x = 1
        y = 0
        while i < len(self.label_list):
            grid1.addWidget(self.label_list[i], x, y)
            grid1.addWidget(self.value_list[i], x, y + 1)
            i = i + 1
            if i % 4 == 0:
                x = x + 1
                y = 0
            else:
                y = y + 2

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(selectButton, 1, 0)
        grid2.addWidget(clearButton, 1, 1)
        grid2.addWidget(modifyButton, 1, 2)
        grid2.addWidget(deleteButton, 1, 3)
        grid2.addWidget(editButton, 1, 4)


        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(10)
        grid3.addWidget(self.tableWidget, 3, 0, 5, 0)

        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(grid1)
        vlayout.addLayout(grid2)
        vlayout.addLayout(grid3)

        self.setLayout(vlayout)

        self.resize(1100, 1000)
        self.setWindowTitle(u'缴费信息')
        self.setWindowIcon(QtGui.QIcon('icon/png12.png'))

    def refresh_table(self, stuInfo):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(stuInfo))
        self.tableWidget.setColumnCount(len(self.tablelist))
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setHorizontalHeaderLabels(self.tablelist)
        i = 0
        for row in stuInfo:
            chkBoxItem = QtGui.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 0, chkBoxItem)
            for col in range(0, len(row)):
                v = row[col]
                item = QtGui.QTableWidgetItem(v)
                self.tableWidget.setItem(i, col + 1, item)
            money_info = Sql("stu_money_info").select_by_list(self.money_list[1:], {u"学号":row[0], u"学期": get_term()})
            if len(money_info) != 0:
                for j in range(0, len(money_info[0])):
                    vj = money_info[0][j]
                    item = QtGui.QTableWidgetItem(vj)
                    self.tableWidget.setItem(i, col + j + 2, item)
            i = i + 1

    def sels(self):
        i = 0
        sel_dict = {}
        while i < len(self.label_list):
            if len(get_text(self.value_list[i])) != 0:
                sel_dict[self.label_list[i].text()] = get_text(self.value_list[i])
            i = i + 1

        stuInfo = Sql().select_by_list(self.flag_list, sel_dict)
        self.currentTable = stuInfo
        self.refresh_table(stuInfo)

    def edit_money(self):
        i = 0
        stu_info_list = []
        while i < len(self.currentTable):
            if self.tableWidget.item(i, 0).checkState() == QtCore.Qt.Checked:
                stu_info_list.append(self.currentTable[i])
            i = i + 1
        if len(stu_info_list) == 0:
            return 0
        if len(stu_info_list) > 1:
            showWarnDialog(self, u"只能选择一条记录！")
            return 1
        money_info = Sql("stu_money_info").select({u"学号": stu_info_list[0][0], u"学期": get_term()})
        if len(money_info) == 0:
            self.editmoney = addmoney.main(self, stu_info_list[0][0])
            self.editmoney.show()
        else:
            self.editmoney = editbymoney.main(self, stu_info_list[0][0])
            self.editmoney.show()

    def edits(self):
        i = 0
        stu_info_list = []
        while i < len(self.currentTable):
            if self.tableWidget.item(i, 0).checkState() == QtCore.Qt.Checked:
                stu_info_list.append(self.currentTable[i])
            i = i + 1
        if len(stu_info_list) == 0:
            return 0
        if len(stu_info_list) > 1:
            showWarnDialog(self, u"只能选择一条记录！")
            return 1
        money_info = Sql("stu_money_info").select({u"学号": stu_info_list[0][0], u"学期": get_term()})
        if len(money_info) == 0:
            self.editmoney = addmoney.main(self, stu_info_list[0][0])
            self.editmoney.show()
        else:
            self.editmoney = editmoney.main(self, stu_info_list[0][0])
            self.editmoney.show()

    def clears(self):
        for value in self.value_list:
            clear_text(value)
        self.sels()

    def dels(self):
        i = 0
        stu_id_list = []
        stu_id_list1 = []
        ask_ok = showComfirmDialog(self, u"是否删除学生缴费信息？")
        if ask_ok == 1:
            return 1
        while i < len(self.currentTable):
            if self.tableWidget.item(i, 0).checkState() == QtCore.Qt.Checked:
                stu_id = self.currentTable[i][0]
                stu_term = get_term()
                status = Sql("stu_money_info").delete(stu_id)
                if status == 1:
                    stu_id_list.append(stu_id)
                status1 = delete_addmoney(stu_id, stu_term)
                if status1 == 1:
                    stu_id_list1.append((stu_id, stu_term))
            i = i + 1
        if len(stu_id_list) == 0 and len(stu_id_list1) == 0:
            showMessageDialog(self, u"删除学生缴费信息成功！")
        else:
            msg = u"""删除学生缴费信息失败！
INFO:
    stu_money_info:%s
    stu_addmoney_info:%s""" % (str(stu_id_list), str(stu_id_list1))
            showWarnDialog(self, msg)

        self.sels()
        return 0


def main():
    MainWindow_2 = SelMoney()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    return MainWindow_2


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainWindow_2 = SelMoney()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    MainWindow_2.show()
    sys.exit(app.exec_())