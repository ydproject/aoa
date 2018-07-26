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
        self.tableWidget.setColumnWidth(5, 180)
        self.tableWidget.setHorizontalHeaderLabels(self.tablelist)
        i = 0
        sum = 0
        add_sum = 0
        for row in stuInfo:
            chkBoxItem = QtGui.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 0, chkBoxItem)
            sum = sum + float(row[5])
            if float(row[5]) >= 0:
                add_sum = add_sum + float(row[5])
            for col in range(0, len(row)):
                v = row[col]
                item = QtGui.QTableWidgetItem(v)
                self.tableWidget.setItem(i, col + 1, item)
            i = i + 1

        #编辑框控件
        self.label_list = []
        self.value_list = []

        for items, items_value in self.select_infos:
            if str(items_value[0]) == "1":
                label = QtGui.QLabel(items)
                self.label_list.append(label)
                edits = QtGui.QLineEdit()
                self.value_list.append(edits)
            if str(items_value[0]) == "2":
                label = QtGui.QLabel(items)
                self.label_list.append(label)
                edits = QtGui.QComboBox()
                edits.addItem("")
                for item in get_flag_list("flow_money_sel", items):
                    edits.addItem(item)
                self.value_list.append(edits)

        self.startTime = QtCore.QDateTime(QtCore.QDate(1999, 1, 1), QtCore.QTime(0, 0, 0))
        self.begin_label = QtGui.QLabel(u"开始时间:")
        self.begin_edit = QtGui.QDateTimeEdit(self.startTime)
        self.end_label = QtGui.QLabel(u"结束时间:")
        self.end_edit = QtGui.QDateTimeEdit(QtCore.QDateTime(get_tommor_date(), QtCore.QTime(0, 0, 0)))

        self.sum_info = QtGui.QLabel(u"收入：%12.2f，支出：%12.2f， 合计：%12.2f元" % (add_sum, add_sum-sum, sum))

        # 按钮控件
        selectButton = QtGui.QPushButton(frame)
        selectButton.setText(u'查询')
        QtCore.QObject.connect(selectButton, QtCore.SIGNAL("clicked()"), self.sels)


        clearButton = QtGui.QPushButton(frame)
        clearButton.setText(u'清空')
        QtCore.QObject.connect(clearButton, QtCore.SIGNAL("clicked()"), self.clears)

        exportButton = QtGui.QPushButton(frame)
        exportButton.setText(u'导出')
        QtCore.QObject.connect(exportButton, QtCore.SIGNAL("clicked()"), self.export)
        if query_current_user()[2] != "Admin":
            exportButton.setDisabled(True)
        else:
            exportButton.setDisabled(False)

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

        x = x + 1
        grid1.addWidget(self.begin_label, x, 0)
        grid1.addWidget(self.begin_edit, x, 1)
        x = x + 1
        grid1.addWidget(self.end_label, x, 0)
        grid1.addWidget(self.end_edit, x, 1)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(selectButton, 1, 0)
        grid2.addWidget(clearButton, 1, 1)
        grid2.addWidget(exportButton, 1, 2)
        grid2.addWidget(self.sum_info, 1, 3)


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

    def export(self):
        file_name = save_file()
        if file_name == "":
            return
        stu_info_list = []
        i = 0
        while i < len(self.currentTable):
            if self.tableWidget.item(i, 0).checkState() == QtCore.Qt.Checked:
                stu_info_list.append(self.currentTable[i])
            i = i + 1
        if len(stu_info_list) != 0:
            status = write_xls(file_name, self.flag_list, stu_info_list)
        else:
            status = write_xls(file_name, self.flag_list, self.currentTable)
        if status == 0:
            showWarnDialog(self, u"导出Excel失败！")
        else:
            showMessageDialog(self, u"导出Excel成功: %s" % file_name )

    def refresh_table(self, stuInfo):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(stuInfo))
        self.tableWidget.setColumnCount(len(self.tablelist))
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(5, 180)
        self.tableWidget.setHorizontalHeaderLabels(self.tablelist)
        i = 0
        sum = 0
        add_sum = 0
        for row in stuInfo:
            chkBoxItem = QtGui.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 0, chkBoxItem)
            sum = sum + float(row[5])
            if float(row[5]) >= 0:
                add_sum = add_sum + float(row[5])
            for col in range(0, len(row)):
                v = row[col]
                item = QtGui.QTableWidgetItem(v)
                self.tableWidget.setItem(i, col + 1, item)
            i = i + 1

        self.sum_info.setText(u"收入：%12.2f，支出：%12.2f， 合计：%12.2f元" % (add_sum, add_sum-sum, sum))

    def sels(self, flag=0):
        i = 0
        sel_dict = {}
        while i < len(self.label_list):
            if len(get_text(self.value_list[i])) != 0:
                sel_dict[self.label_list[i].text()] = get_text(self.value_list[i])
            i = i + 1
        if flag == 0:
            stuInfo = flow_select_time(self.flag_list, sel_dict, self.begin_edit.text(), self.end_edit.text())
        else:
            stuInfo = flow_select_time(self.flag_list)
        self.currentTable = stuInfo
        self.refresh_table(stuInfo)

    def clears(self):
        for value in self.value_list:
            clear_text(value)
        self.begin_edit.setDateTime(self.startTime)
        self.end_edit.setDateTime(QtCore.QDateTime(get_tommor_date(), QtCore.QTime(0, 0, 0)))
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