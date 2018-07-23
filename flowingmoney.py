#!/usr/bin/python
# -*- coding: utf-8 -*-

# boxlayout.py

import sys
from PyQt4 import QtGui, QtCore
from util import *


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
        self.begin_label = QtGui.QLabel(u"开始时间:")
        self.begin_edit = QtGui.QLineEdit()
        self.end_label = QtGui.QLabel(u"结束时间:")
        self.end_edit = QtGui.QLineEdit()

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


        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(10)
        grid3.addWidget(self.tableWidget, 3, 0, 5, 0)

        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(grid1)
        vlayout.addLayout(grid2)
        vlayout.addLayout(grid3)

        self.setLayout(vlayout)

        self.resize(1000, 1000)
        self.setWindowTitle(u'查询交易流水')
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
        sel_dict = {}
        while i < len(self.label_list):
            if len(self.value_list[i].text()) != 0:
                sel_dict[self.label_list
                [i].text()] = self.value_list[i].text()
            i = i + 1

        stuInfo = Sql("flow_money_sel").select(self.flag_list, sel_dict)
        self.currentTable = stuInfo
        self.refresh_table(stuInfo)

    def clears(self):
        for value in self.value_list:
            if not isinstance(value, QtGui.QComboBox):
                value.clear()
        self.sels()



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