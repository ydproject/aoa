# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from util import *
import traceback


class EditByMoney(QtGui.QWidget):

    def __init__(self, object=None, stu_id=""):
        super(EditByMoney, self).__init__()
        self.faWindow = object
        frame = QtGui.QFrame(self)
        self.stu_id = stu_id

        self.data = Sql("stu_money_info").select({u"学号": stu_id, u"学期": get_term()})[0]
        self.old_value = sum(map(str_to_sum, self.data[2:]))

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
        i = 0
        for item_info, item_value in self.student_info:
            if item_value[0] == "":
                i = i + 1
                continue
            label = QtGui.QLabel(item_info)
            label.setFixedWidth(60)
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
                if self.data[i] != "0":
                    chkBoxItem.setCheckState(QtCore.Qt.Checked)
                    # chkBoxItem.setDisabled(True)
                else:
                    chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                self.value_list.append(chkBoxItem)
            else:
                chkBoxItem_list = []
                j = 0
                data_j = self.data[i].split(",")
                for item in item_value[1:]:
                    chkBoxItem = QtGui.QCheckBox(item)
                    if data_j[j] != "0":
                        chkBoxItem.setCheckState(QtCore.Qt.Checked)
                        # chkBoxItem.setDisabled(True)
                    else:
                        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                    chkBoxItem_list.append(chkBoxItem)
                    j = j + 1
                self.value_list.append(chkBoxItem_list)
            i = i + 1

        pushButton_1 = QtGui.QPushButton(frame)
        pushButton_1.setGeometry(QtCore.QRect(120, 360, 71, 31))
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        pushButton_1.setFont(font2)
        pushButton_1.setText(u'确定添加')
        pushButton_1.setFixedWidth(80)
        pushButton_2 = QtGui.QPushButton(frame)
        pushButton_2.setGeometry(QtCore.QRect(390, 360, 75, 31))
        # pushButton_2.setFont(font2)
        pushButton_2.setText(u'清空信息')
        pushButton_2.setFixedWidth(80)
        QtCore.QObject.connect(pushButton_1, QtCore.SIGNAL("clicked()"), self.confirm)
        QtCore.QObject.connect(pushButton_2, QtCore.SIGNAL("clicked()"), self.clears)

        #布局
        vlayout = QtGui.QVBoxLayout()
        vlayout.setAlignment(QtCore.Qt.AlignTop)
        grid1 = QtGui.QGridLayout()
        grid1.setColumnStretch(200, 200)
        grid1.setAlignment(QtCore.Qt.AlignBottom)
        grid1.setSpacing(20)
        number = 12
        x = 1
        label0 = QtGui.QLabel(u"学号")
        label0.setFixedWidth(60)
        self.lineEdit0 = QtGui.QLineEdit()
        self.lineEdit0.setFixedWidth(150)
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
        label1.setFixedWidth(60)
        self.lineEdit1 = QtGui.QLineEdit()
        self.lineEdit1.setFixedWidth(150)
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
        grid2.setAlignment(QtCore.Qt.AlignCenter)
        grid2.setSpacing(80)
        grid2.setColumnStretch(200, 200)
        grid2.addWidget(pushButton_1, 1, 1)
        grid2.addWidget(pushButton_2, 1, 3)

        vlayout.addLayout(grid2)

        self.setLayout(vlayout)
        self.setWindowTitle(u'缴费信息')
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.resize(335, 549)
        self.setWindowIcon(QtGui.QIcon(os.path.join(get_cwd(), 'icon', 'png_3.png')))

    def clears(self):
        self.reset()

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
        spend = total - self.old_value
        pre_before = u"0.0"
        pre_end = u"0.0"
        pre_info = Sql("stu_money_pre").select({u"学号": self.lineEdit0.text()})
        if len(pre_info) == 0:
            Sql("stu_money_pre").add([self.lineEdit0.text(), unicode(pre_end)])
            premoney = 0.0
        elif spend <= 0:
            pre_end = pre_before = unicode(pre_info[0][1])
            premoney = 0.0
        else:
            premoney = float(pre_info[0][1])
            if premoney != 0:
                ask_info = showComfirmDialog(self, u"是否抵扣预收款？ %8.2f" % premoney)
                if ask_info == 1:
                    premoney = 0.0
            pre_before = unicode(premoney)
            if spend >= premoney:
                pre_status = Sql("stu_money_pre").update([self.lineEdit0.text(), unicode(premoney)], [self.lineEdit0.text(), pre_end])
            else:
                pre_end = unicode(premoney - spend)
                pre_status = Sql("stu_money_pre").update([self.lineEdit0.text(), unicode(premoney)], [self.lineEdit0.text(), pre_end])
                premoney = spend
            if pre_status != 0:
                pre_end = pre_before
                premoney = 0.0
                showWarnDialog(self, u"抵扣预收费失败！")

        ask_info = showComfirmDialog(self, u"合计：%8.2f 元，抵扣预收费：%8.2f 元，需缴纳：%8.2f 元，确认缴费？" % (spend, premoney, spend - premoney))
        if ask_info == 1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            return 1
        spend = spend - premoney

        if spend >= 0:
            f_str = u"缴费"
        else:
            f_str = u"退费"
        num = add_flowing(self, u"%8.2f" % spend, self.lineEdit0.text(), f_str)
        if num == -1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            showWarnDialog(self, u"%s失败！" % f_str)
            ERROR(u"Edit student money failed! user: %s, stu_id: %s" % (
            unicode(query_current_user()[1]), unicode(self.lineEdit0.text())))
            return 0
        status = Sql("stu_money_info").update(list(self.data), values)
        old_values = list(self.data)
        if status == 1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            Sql("flow_money_sel").delete(num)
            self.reset()
            showWarnDialog(self, u"%s失败！" % f_str)
            ERROR(u"Edit student money failed! user: %s, stu_id: %s" % (
            unicode(query_current_user()[1]), unicode(self.lineEdit0.text())))
            return 1
        status1 = stu_addmoney_add(values)
        if status1 == 1:
            Sql("stu_money_pre").update([self.lineEdit0.text(), pre_end], [self.lineEdit0.text(), pre_before])
            Sql("flow_money_sel").delete(num)
            Sql("stu_money_info").update(values, list(self.data))
            showWarnDialog(self, u"%s失败！" % f_str)
            ERROR(u"Edit student money failed! user: %s, stu_id: %s" % (
            unicode(query_current_user()[1]), unicode(self.lineEdit0.text())))
            self.reset()
        else:
            showMessageDialog(self, u"%s成功！" % f_str)
            INFO(u"Edit student money success!user: %s, stu_id: %s, values: %s" % (
            unicode(query_current_user()[1]), unicode(self.lineEdit0.text()), unicode(values)))
            html = u""
            if spend != 0:
                try:
                    html = stu_addmoney_print(old_values, values)
                    res = showComfirmDialog(self, u"是否打印收据？")
                    if res == 0:
                        print_html(html)
                except Exception,e :
                    showWarnDialog(self, u"无法打印收据，请手动处理！")
                    ERROR(u"Print html failed: html:%s error %s" % (html, traceback.format_exc()))
            self.faWindow.sels()
            self.close()
        return 0

    def reset(self):
        i = 2
        for items in self.value_list:
            if isinstance(items, list):
                j = 0
                data = self.data[i].split(",")
                for item in items:
                    if data[j] != "0":
                        pass
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)
                    j = j + 1
            else:
                if self.data[i] != "0":
                    pass
                else:
                    items.setCheckState(QtCore.Qt.Unchecked)
            i = i + 1


def main(object=None, stu_id=""):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    MainWindow_1 = EditByMoney(object, stu_id)
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    return MainWindow_1

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app1 = QtGui.QApplication(sys.argv)
    MainWindow_1 = EditByMoney(stu_id = "20180007")
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    MainWindow_1.show()
    sys.exit(app1.exec_())