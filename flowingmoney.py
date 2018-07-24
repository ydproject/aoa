#!/usr/bin/python
# -*- coding: utf-8 -*-

# boxlayout.py

import sys
from PyQt4 import QtGui, QtCore
from util import *
import datetime


class FlowingMoney(QtGui.QWidget):

    def __init__(self):
        super(FlowingMoney, self).__init__()

        self.initUI()

    def initUI(self):
        frame = QtGui.QFrame(self)
        self.select_infos = read_file("flow_money_sel.txt")
        self.flag_list = [item for item, item_value in self.select_infos][1:]
        # 表格控件
        self.tablelist = [u''] + self.flag_list
        stuInfo = Sql("flow_money_sel").select_by_list(self.flag_list)
        self.currentTable = stuInfo
        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setRowCount(len(stuInfo))
        self.tableWidget.setColumnCount(len(self.tablelist))
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setHorizontalHeaderLabels(self.tablelist)
        i = 0
        sum = 0
        for row in stuInfo:
            chkBoxItem = QtGui.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 0, chkBoxItem)
            sum = sum + float(row[1])
            for col in range(0, len(row)):
                v = row[col]
                item = QtGui.QTableWidgetItem(v)
                self.tableWidget.setItem(i, col + 1, item)
            i = i + 1

        #编辑框控件
        self.begin_label = QtGui.QLabel(u"开始时间:")
        self.begin_edit = QtGui.QDateTimeEdit(QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime.currentTime()))
        self.end_label = QtGui.QLabel(u"结束时间:")
        self.end_edit = QtGui.QDateTimeEdit(QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime.currentTime()))

        self.sum_info = QtGui.QLabel(u"合计: %8.2f元" % sum)

        # 按钮控件
        selectButton = QtGui.QPushButton(frame)
        selectButton.setText(u'查询')
        QtCore.QObject.connect(selectButton, QtCore.SIGNAL("clicked()"), self.sels)


        clearButton = QtGui.QPushButton(frame)
        clearButton.setText(u'清空')
        QtCore.QObject.connect(clearButton, QtCore.SIGNAL("clicked()"), self.clears)

        #布局vlayout = QtGui.QVBoxLayout()
        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)

        grid1.addWidget(self.begin_label, 0, 0)
        grid1.addWidget(self.begin_edit, 0, 1)
        grid1.addWidget(self.end_label, 0, 2)
        grid1.addWidget(self.end_edit, 0, 3)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(selectButton, 1, 0)
        grid2.addWidget(clearButton, 1, 1)
        grid2.addWidget(self.sum_info, 1, 2)


        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(10)
        grid3.addWidget(self.tableWidget, 3, 0, 5, 0)


        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(grid1)
        vlayout.addLayout(grid2)
        vlayout.addLayout(grid3)


        self.setLayout(vlayout)

        self.resize(500, 1000)
        self.setWindowTitle(u'查询交易流水')
        self.setWindowIcon(QtGui.QIcon('icon/png12.png'))

    def refresh_table(self, stuInfo):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(stuInfo))
        self.tableWidget.setColumnCount(len(self.tablelist))
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setHorizontalHeaderLabels(self.tablelist)
        i = 0
        sum = 0
        for row in stuInfo:
            chkBoxItem = QtGui.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 0, chkBoxItem)
            sum = sum + float(row[1])
            for col in range(0, len(row)):
                v = row[col]
                item = QtGui.QTableWidgetItem(v)
                self.tableWidget.setItem(i, col + 1, item)
            i = i + 1

        self.sum_info.setText(u"合计: %8.2f元" % sum)

    def sels(self, flag=0):
        if flag == 0:
            stuInfo = flow_select_time(self.flag_list, self.begin_edit.text(), self.end_edit.text())
        else:
            stuInfo = flow_select_time(self.flag_list)
        self.currentTable = stuInfo
        self.refresh_table(stuInfo)

    def clears(self):
        self.begin_edit.setDateTime(QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime.currentTime()))
        self.end_edit.setDateTime(QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime.currentTime()))
        self.sels(1)



def main():
    MainWindow_2 = FlowingMoney()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    return MainWindow_2


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainWindow_2 = FlowingMoney()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    MainWindow_2.show()
    sys.exit(app.exec_())