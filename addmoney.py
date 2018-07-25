# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from util import *
import traceback


class AddMoney(QtGui.QWidget):

    def __init__(self, object=None, stu_id=""):
        super(AddMoney, self).__init__()
        self.faWindow = object
        frame = QtGui.QFrame(self)
        self.stu_id = stu_id

        #编辑控件
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.student_info = read_file("stu_money_info.txt")
        self.label_list = []
        self.value_list = []
        self.money_list = []
        for item_info, item_value in self.student_info:
            if item_value[0] == "":
                continue
            label = QtGui.QLabel(item_info)
            self.label_list.append(label)
            if len(item_value) == 0 or len(item_value[0]) == 0:
                money = 0
            else:
                try:
                    money = int(item_value[0])
                except Exception, e:
                    print traceback.format_exc()
                    money = 0
            self.money_list.append(money)
            if len(item_value) <= 1:
                chkBoxItem = QtGui.QCheckBox(u"全部")
                chkBoxItem.setCheckState(QtCore.Qt.Checked)
                self.value_list.append(chkBoxItem)
            else:
                chkBoxItem_list = []
                for item in item_value[1:]:
                    chkBoxItem = QtGui.QCheckBox(item)
                    chkBoxItem.setCheckState(QtCore.Qt.Checked)
                    chkBoxItem_list.append(chkBoxItem)
                self.value_list.append(chkBoxItem_list)

        pushButton_1 = QtGui.QPushButton(frame)
        pushButton_1.setGeometry(QtCore.QRect(120, 360, 71, 31))
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        pushButton_1.setFont(font2)
        pushButton_1.setText(u'确定添加')
        pushButton_2 = QtGui.QPushButton(frame)
        pushButton_2.setGeometry(QtCore.QRect(390, 360, 75, 31))
        # pushButton_2.setFont(font2)
        pushButton_2.setText(u'清空信息')
        QtCore.QObject.connect(pushButton_1, QtCore.SIGNAL("clicked()"), self.confirm)
        QtCore.QObject.connect(pushButton_2, QtCore.SIGNAL("clicked()"), self.clears)

        #布局
        vlayout = QtGui.QVBoxLayout()
        vlayout.setAlignment(QtCore.Qt.AlignTop)
        grid1 = QtGui.QGridLayout()
        grid1.setAlignment(QtCore.Qt.AlignBottom)
        grid1.setSpacing(20)
        number = 12
        x = 1
        label0 = QtGui.QLabel(u"学号")
        self.lineEdit0 = QtGui.QLineEdit()
        if self.stu_id != "":
            self.lineEdit0.setText(self.stu_id)
            self.lineEdit0.setDisabled(True)
        grid1.addWidget(label0, x, 0)
        grid1.addWidget(self.lineEdit0, x, 1, 1, 2)
        for index in range(2, number):
            label = QtGui.QLabel(" ")
            grid1.addWidget(label, x, index)

        x = 2
        label1 = QtGui.QLabel(u"学期")
        self.lineEdit1 = QtGui.QLineEdit()
        self.lineEdit1.setText(get_term())
        self.lineEdit1.setDisabled(True)
        grid1.addWidget(label1, x, 0)
        grid1.addWidget(self.lineEdit1, x, 1, 1, 2)
        for index in range(2, number):
            label = QtGui.QLabel(" ")
            grid1.addWidget(label, x, index)

        i = 0
        for label in self.label_list:
            x = x + 1
            grid1.addWidget(label, x, 0)
            y = 1
            if isinstance(self.value_list[i], list):
                for value in self.value_list[i]:
                    grid1.addWidget(value, x, y)
                    y = y + 1
            else:
                grid1.addWidget(self.value_list[i], x, y)
            for index in range(y+1, number):
                label = QtGui.QLabel(" ")
                grid1.addWidget(label, x, index)
            i = i + 1

        vlayout.addLayout(grid1)
        vlayout.setSpacing(40)

        grid2 = QtGui.QGridLayout()
        grid2.setAlignment(QtCore.Qt.AlignLeft)
        grid2.setSpacing(80)
        grid2.addWidget(pushButton_1, 1, 1)
        grid2.addWidget(pushButton_2, 1, 3)

        vlayout.addLayout(grid2)

        self.setLayout(vlayout)
        self.setWindowTitle(u'缴费信息')
        self.resize(335, 549)
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'icon', 'png_3.png')))

    def clears(self):
        if self.stu_id == "":
            self.lineEdit0.clear()
        for value in self.value_list:
            if not isinstance(value, list):
                value.setCheckState(QtCore.Qt.Unchecked)
            else:
                for item in value:
                    item.setCheckState(QtCore.Qt.Unchecked)

    def confirm(self):
        if not Sql().check_stu_id_exist(self.lineEdit0.text()):
            showWarnDialog(self, u"学号不存在！")
            return 1
        values = [self.lineEdit0.text(), self.lineEdit1.text()]
        for i in range(0, len(self.label_list)):
            if not isinstance(self.value_list[i], list):
                if self.value_list[i].checkState() == QtCore.Qt.Checked:
                    value = str(self.money_list[i])
                else:
                    value = "0"
            else:
                value = []
                for item in self.value_list[i]:
                    if item.checkState() == QtCore.Qt.Checked:
                        value.append(str(self.money_list[i]))
                    else:
                        value.append("0")
                value = ",".join(value)
            values.append(value)
        total = sum(map(str_to_sum, values[2:]))
        pre_info = Sql("stu_money_pre").select({u"学号": self.lineEdit0.text()})
        if len(pre_info) == 0:
            premoney = 0.0
        else:
            premoney = float(pre_info[0][1])
            ask_info = showComfirmDialog(self, u"是否抵扣预收款？ %8.2f" % premoney)
            if ask_info == 1:
                premoney = 0.0
            else:
                pre_before = unicode(premoney)
                pre_end = u"0.0"
                if total >= premoney:
                    pre_status = Sql("stu_money_pre").update([self.lineEdit0.text(), unicode(premoney)], [self.lineEdit0.text(), pre_end])
                else:
                    pre_end = unicode(premoney - total)
                    pre_status = Sql("stu_money_pre").update([self.lineEdit0.text(), unicode(premoney)], [self.lineEdit0.text(), pre_end])
                    premoney = total
                if pre_status != 0:
                    pre_end = unicode(premoney)
                    premoney = 0.0
                    showWarnDialog(self, u"抵扣预收费失败！")

        ask_info = showComfirmDialog(self, u"合计：%8.2f 元，抵扣预收费：%8.2f 元，需缴纳：%8.2f 元，确认缴费？" % (total, premoney, total - premoney))
        if ask_info == 1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            return 1
        total = total - premoney
        if total >= 0:
            f_str = u"缴费"
        else:
            f_str = u"退费"
        num = add_flowing(u"%8.2f" % total, self.lineEdit0.text(), f_str)
        if num == -1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            showWarnDialog(self, u"缴费失败！")
            return 0
        status = Sql("stu_money_info").add(values)
        if status == 1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            Sql("flow_money_sel").delete(num)
            showWarnDialog(self, u"缴费失败！")
            return 0
        status1 = stu_addmoney_add(values)
        if status1 == 1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            Sql("flow_money_sel").delete(num)
            Sql("stu_money_info").delete(self.lineEdit0.text())
            showWarnDialog(self, u"缴费失败！")
        else:
            showMessageDialog(self, u"缴费成功！")
            if self.stu_id == "":
                self.reset()
            else:
                self.faWindow.sels()
                self.close()
        return 0

    def reset(self):
        self.lineEdit0.clear()
        for item in self.value_list:
            if isinstance(item, list):
                for i in item:
                    i.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Checked)


def main(object=None, stu_id=""):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    MainWindow_1 = AddMoney(object, stu_id)
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    return MainWindow_1

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app1 = QtGui.QApplication(sys.argv)
    MainWindow_1 = AddMoney("20180009")
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    MainWindow_1.show()
    sys.exit(app1.exec_())