#!/usr/bin/python
# -*- coding: utf-8 -*-

# boxlayout.py

import sys
from PyQt4 import QtGui, QtCore
from util import *


class PreAddMoney(QtGui.QWidget):

    def __init__(self):
        super(PreAddMoney, self).__init__()

        self.initUI()

    def initUI(self):
        frame = QtGui.QFrame(self)
        self.select_infos = read_file("stu_selmoney_info.txt")
        self.flag_list = [item for item, item_value in self.select_infos]
        self.money_infos = read_file("stu_money_pre.txt")
        self.money_list = [item for item, item_value in self.money_infos]
        # 表格控件
        self.tablelist = [u''] + self.flag_list + self.money_list[1:]
        stuInfo = select_money_by_stu(self.flag_list, self.money_list[1:])
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
            i = i + 1

        #编辑框控件
        self.label_list_stu = []
        self.value_list_stu = []
        self.label_list_money = []
        self.value_list_money = []
        for items, items_value in self.select_infos:
            label = QtGui.QLabel(items)
            self.label_list_stu.append(label)
            edits = QtGui.QLineEdit()
            self.value_list_stu.append(edits)

        for items, items_value in self.money_infos[1:]:
            label = QtGui.QLabel(items)
            self.label_list_money.append(label)
            edits = QtGui.QLineEdit()
            self.value_list_money.append(edits)

        # 按钮控件
        selectButton = QtGui.QPushButton(frame)
        selectButton.setText(u'查询')
        QtCore.QObject.connect(selectButton, QtCore.SIGNAL("clicked()"), self.sels)

        addButton = QtGui.QPushButton(frame)
        addButton.setText(u'新增')
        QtCore.QObject.connect(addButton, QtCore.SIGNAL("clicked()"), self.adds)

        modifyButton = QtGui.QPushButton(frame)
        modifyButton.setText(u'编辑')
        QtCore.QObject.connect(modifyButton, QtCore.SIGNAL("clicked()"), self.edits)
        if query_current_user()[2] != "Admin":
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
        while i < len(self.label_list_stu):
            grid1.addWidget(self.label_list_stu[i], x, y)
            grid1.addWidget(self.value_list_stu[i], x, y + 1)
            i = i + 1
            if i % 4 == 0:
                x = x + 1
                y = 0
            else:
                y = y + 2

        i = 0
        x = x + 1
        while i < len(self.label_list_money):
            grid1.addWidget(self.label_list_money[i], x, y)
            grid1.addWidget(self.value_list_money[i], x, y + 1)
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
        grid2.addWidget(addButton, 1, 2)
        grid2.addWidget(modifyButton, 1, 3)
        grid2.addWidget(deleteButton, 1, 4)


        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(10)
        grid3.addWidget(self.tableWidget, 3, 0, 5, 0)

        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(grid1)
        vlayout.addLayout(grid2)
        vlayout.addLayout(grid3)

        self.setLayout(vlayout)

        self.resize(1200, 1000)
        self.setWindowTitle(u'查询缴费信息')
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
            i = i + 1

    def sels(self):
        i = 0
        dict1 = {}
        while i < len(self.label_list_stu):
            if len(self.value_list_stu[i].text()) != 0:
                dict1[unicode(self.label_list_stu[i].text())] = unicode(self.value_list_stu[i].text())
            i = i + 1
        dict2 = {}
        i = 0
        while i < len(self.label_list_money):
            if len(self.value_list_money[i].text()) != 0:
                dict2[unicode(self.label_list_money[i].text())] = unicode(self.value_list_money[i].text())
            i = i + 1
        stuInfo = select_money_by_stu(self.flag_list, self.money_list[1:], dict1, dict2)
        self.currentTable = stuInfo
        self.refresh_table(stuInfo)


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
            self.editmoney = editpremoney.main(self, stu_info_list[0][0])
            self.editmoney.show()

    def adds(self):
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
        self.editmoney = addpremoney.main(self, stu_info_list[0][0])
        self.editmoney.show()

    def clears(self):
        for value in self.value_list_stu:
            if not isinstance(value, QtGui.QComboBox):
                value.clear()
        for value in self.value_list_money:
            if not isinstance(value, QtGui.QComboBox):
                value.clear()
        self.sels()

    def dels(self):
        i = 0
        stu_id_list = []
        ask_ok = showComfirmDialog(self, u"是否删除学生信息？")
        if ask_ok == 1:
            return 1
        while i < len(self.currentTable):
            if self.tableWidget.item(i, 0).checkState() == QtCore.Qt.Checked:
                stu_id = self.currentTable[i][0]
                status = Sql("stu_money_info").delete(stu_id)
                if status == 1:
                    stu_id_list.append(stu_id)
            i = i + 1
        if len(stu_id_list) == 0:
            showMessageDialog(self, u"删除学生信息成功！")
        else:
            showWarnDialog(self, u"删除学生信息(%s)失败！" % ",".join(stu_id_list))

        self.sels()
        return 0


def main():
    MainWindow_2 = PreAddMoney()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    return MainWindow_2


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainWindow_2 = PreAddMoney()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    MainWindow_2.show()
    sys.exit(app.exec_())