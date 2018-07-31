#!/usr/bin/python
# -*- coding: utf-8 -*-

# boxlayout.py

import sys
from PyQt4 import QtGui, QtCore
from util import *
import addsignup, addmoney, editmoney


class SignUp(QtGui.QWidget):

    def __init__(self):
        super(SignUp, self).__init__()

        self.initUI()

    def initUI(self):
        frame = QtGui.QFrame(self)
        self.select_infos = read_file("sign_up_info.txt")
        self.stu_list = [i for i,j in self.select_infos]
        self.flag_list = self.stu_list[:1]
        # 表格控件
        self.tablelist = [u''] + self.stu_list + [u'缴费情况'] + [u'缴费金额(元)']
        stuInfo = Sql().select_by_list(self.stu_list)
        self.currentTable = stuInfo
        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setRowCount(len(stuInfo))
        self.tableWidget.setColumnCount(len(self.tablelist))
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 180)
        self.tableWidget.setFixedWidth(1000)
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
            total = get_stu_money(row[0])
            if total == 0.0:
                v = u"未缴费"
            else:
                v = u"已缴费"
            item = QtGui.QTableWidgetItem(v)
            self.tableWidget.setItem(i, col + 2, item)
            v = u"%8.2f" % total
            item = QtGui.QTableWidgetItem(v)
            self.tableWidget.setItem(i, col + 3, item)
            i = i + 1

        #编辑框控件
        self.label = QtGui.QLabel(u"姓名")
        self.label.setFixedWidth(60)
        self.edits = QtGui.QLineEdit()
        self.edits.setFixedWidth(150)
        self.edits.textChanged.connect(self.sels)


        # 按钮控件
        addButton = QtGui.QPushButton(frame)
        addButton.setText(u'新增')
        addButton.setFixedWidth(80)
        QtCore.QObject.connect(addButton, QtCore.SIGNAL("clicked()"), self.adds)
        if query_current_user()[2] == "Guest":
            addButton.setDisabled(True)
        else:
            addButton.setDisabled(False)

        signButton = QtGui.QPushButton(frame)
        signButton.setText(u'缴费')
        signButton.setFixedWidth(80)
        QtCore.QObject.connect(signButton, QtCore.SIGNAL("clicked()"), self.sign_up)
        if query_current_user()[2] == "Guest":
            signButton.setDisabled(True)
        else:
            signButton.setDisabled(False)

        clearButton = QtGui.QPushButton(frame)
        clearButton.setText(u'清空')
        clearButton.setFixedWidth(80)
        clearButton.setFixedHeight(25)
        QtCore.QObject.connect(clearButton, QtCore.SIGNAL("clicked()"), self.clears)

        exportButton = QtGui.QPushButton(frame)
        exportButton.setText(u'导出')
        exportButton.setFixedWidth(80)
        exportButton.setFixedHeight(25)
        QtCore.QObject.connect(exportButton, QtCore.SIGNAL("clicked()"), self.export)
        if query_current_user()[2] != "Admin":
            exportButton.setDisabled(True)
        else:
            exportButton.setDisabled(False)

        #布局vlayout = QtGui.QVBoxLayout()
        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(20)
        grid1.setColumnStretch(200,200)
        grid1.setAlignment(QtCore.Qt.AlignLeft)
        grid1.addWidget(self.label, 1, 0)
        grid1.addWidget(self.edits, 1, 1)

        grid1.addWidget(clearButton, 1, 2)
        grid1.addWidget(exportButton, 1, 4)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(20)
        grid2.setColumnStretch(200, 200)
        grid2.setAlignment(QtCore.Qt.AlignLeft)
        grid2.addWidget(addButton, 1, 1)
        grid2.addWidget(signButton, 1, 2)



        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(10)
        grid3.setAlignment(QtCore.Qt.AlignLeft)
        # grid3.addWidget(self.tableWidget, 3, 0, 5, 0)
        grid3.addWidget(self.tableWidget, 0, 1)
        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(grid1)
        vlayout.addLayout(grid2)
        vlayout.addLayout(grid3)

        self.setLayout(vlayout)

        self.resize(1000, 1000)
        self.setWindowTitle(u'学生报名')
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QtGui.QIcon('icon/png12.png'))

    def sign_up_by_id(self, stu_id):
        money_info = Sql("stu_money_info").select({u"学号": stu_id, u"学期": get_term()})
        if len(money_info) == 0:
            self.editmoney = addmoney.main(self, stu_id)
            self.editmoney.show()
        else:
            self.editmoney = editmoney.main(self, stu_id)
            self.editmoney.show()

    def sign_up(self):
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
        if len(stu_info_list) == 0:
            stu_info_list = self.currentTable
        infos = []
        for stu_info in stu_info_list:
            tmp = list(stu_info[:])
            total = get_stu_money(self.currentTable[0])
            if total == 0.0:
                v1 = u"未缴费"
            else:
                v1 = u"已缴费"
            v2 = u"%8.2f" % total
            tmp.append(v1)
            tmp.append(v2)
            infos.append(tmp)
        status = write_xls(file_name, self.tablelist[1:], infos)
        if status == 1:
            ERROR(u"Export student info to excel failed! user: %s" % unicode(query_current_user()[1]))
            showWarnDialog(self, u"导出Excel失败！")
        else:
            INFO(u"Export student info to excel success!user: %s, file_name: %s, values: %s" % (
            unicode(query_current_user()[1]), unicode(file_name), unicode(infos)))
            showMessageDialog(self, u"导出Excel成功: %s" % file_name )

    def adds(self):
        self.addstudent = addsignup.main(self)
        self.addstudent.show()

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
            total = get_stu_money(row[0])
            if total == 0.0:
                v = u"未缴费"
            else:
                v = u"已缴费"
            item = QtGui.QTableWidgetItem(v)
            self.tableWidget.setItem(i, col + 2, item)
            v = u"%8.2f" % total
            item = QtGui.QTableWidgetItem(v)
            self.tableWidget.setItem(i, col + 3, item)
            i = i + 1

    def sels(self):
        stuInfo = get_stu_infos(self.stu_list, get_text(self.edits))
        self.currentTable = stuInfo
        self.refresh_table(stuInfo)

    def clears(self):
        clear_text(self.edits)
        self.sels()


def main():
    MainWindow_2 = SignUp()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    return MainWindow_2


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainWindow_2 = SignUp()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_2.setPalette(palette)
    MainWindow_2.show()
    sys.exit(app.exec_())