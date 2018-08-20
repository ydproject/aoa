# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from util import *
import traceback


class EditPreMoney(QtGui.QWidget):

    def __init__(self, object=None, stu_id=""):
        super(EditPreMoney, self).__init__()
        self.faWindow = object
        frame = QtGui.QFrame(self)
        self.stu_id = stu_id

        #编辑控件
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.student_info = read_file("stu_money_pre.txt")
        self.label_list = []
        self.value_list = []
        self.money_list = []
        for item_info, item_value in self.student_info:
            if item_value[0] == "":
                continue
            label = QtGui.QLabel(item_info)
            # label.setFont(font)
            self.label_list.append(label)
            # self.null_list.append(str(item_value[0]))
            if str(item_value[0]) == "0" or str(item_value[0]) == "1":
                lineEdit = QtGui.QLineEdit()
            else:
                lineEdit = QtGui.QComboBox()
                for item in item_value:
                    lineEdit.addItem(item)
            self.value_list.append(lineEdit)

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
        number = 5
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

        i = 0
        for label in self.label_list:
            x = x + 1
            grid1.addWidget(label, x, 0)
            grid1.addWidget(self.value_list[i], x, 1, 1, 2)
            for index in range(2, number):
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
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.resize(335, 156)
        self.setWindowIcon(QtGui.QIcon(os.path.join(get_cwd(), 'icon', 'png_3.png')))

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
        values = [self.lineEdit0.text()]
        for item in self.value_list:
            if isinstance(item, QtGui.QLineEdit):
                values.append(str(item.text()))
            if isinstance(item, QtGui.QComboBox):
                values.append(str(item.currentText()))
        total = sum(map(str_to_sum, values[1:]))

        old_list = Sql("stu_money_pre").select({u"学号": self.lineEdit0.text()})
        old_list = old_list[0]
        new_list = [old_list[0], str(total)]
        total = total - float(old_list[1])

        ask_info = showComfirmDialog(self, u"合计：%8.2f 元，确认缴费？" % total)
        if ask_info == 1:
            return 1

        if total != 0:
            if total > 0:
                f_str = u"预收费"
            else:
                f_str = u"退预收费"
            num = add_flowing(self, u"%8.2f" % total, self.lineEdit0.text(), f_str)
            if num == -1:
                showWarnDialog(self, u"缴费失败！")
                return 0

            if len(old_list) == 0:
                status = Sql("stu_money_pre").add(new_list)
            else:
                status = Sql("stu_money_pre").update(old_list, new_list)

            if status == 1:
                showWarnDialog(self, u"缴费失败！")
                ERROR(u"Edit student prepare money failed! user: %s, stu_id: %s, values: %s" % (
                unicode(query_current_user()[1]), unicode(self.lineEdit0.text()), unicode(new_list)))
                Sql("flow_money_sel").delete(num)
                return 0
            else:
                showMessageDialog(self, u"缴费成功！")
                INFO(u"Edit student prepare money success!user: %s, stu_id: %s, values: %s" % (
                unicode(query_current_user()[1]), unicode(self.lineEdit0.text()), unicode(new_list)))
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
    MainWindow_1 = EditPreMoney(object, stu_id)
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    return MainWindow_1

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app1 = QtGui.QApplication(sys.argv)
    MainWindow_1 = EditPreMoney("20180009")
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    MainWindow_1.show()
    sys.exit(app1.exec_())