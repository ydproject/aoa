# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from util import *


class AddUser(QtGui.QWidget):

    def __init__(self, object=None):
        super(AddUser, self).__init__()
        self.faWindows = object
        frame = QtGui.QFrame(self)

        #编辑控件
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        student_info = read_file("auth.txt")
        self.label_list = []
        self.value_list = []
        self.null_list = []
        for item_info, item_value in student_info:
            if item_value[0] == "":
                continue
            label = QtGui.QLabel(item_info)
            # label.setFont(font)
            self.label_list.append(label)
            self.null_list.append(str(item_value[0]))
            #0，必填；1，可不填；2，passwd选项
            if str(item_value[0]) == "0" or str(item_value[0]) == "1" or str(item_value[0]) == "2":
                lineEdit = QtGui.QLineEdit()
                if str(item_value[0]) == "2":
                    lineEdit.setEchoMode(QtGui.QLineEdit.Password)
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
        grid1 = QtGui.QGridLayout()
        grid1.setAlignment(QtCore.Qt.AlignTop)
        grid1.setSpacing(20)

        i = 0
        x = 1
        y = 0
        while i < len(self.label_list):
            grid1.addWidget(self.label_list[i], x, y)
            grid1.addWidget(self.value_list[i], x, y + 1)
            x = x + 1
            i = i + 1

        grid2 = QtGui.QGridLayout()
        grid2.setAlignment(QtCore.Qt.AlignCenter)
        grid2.setSpacing(40)
        grid2.addWidget(pushButton_1, 1, 1)
        grid2.addWidget(pushButton_2, 1, 3)

        vlayout.addLayout(grid1)
        vlayout.addLayout(grid2)
        vlayout.setSpacing(20)

        self.setLayout(vlayout)
        self.setWindowTitle(u'添加用户信息')
        self.resize(435, 229)
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'icon', 'png_3.png')))

    def clears(self):
        for value in self.value_list:
            if not isinstance(value, QtGui.QComboBox):
                value.clear()

    def confirm(self):
        values = []
        i = 0
        for item in self.value_list:
            if isinstance(item, QtGui.QLineEdit):
                values.append(str(item.text()))
                if len(str(item.text())) == 0 and self.null_list[i] != "1":
                    showWarnDialog(self, u"%s不能为空！" % self.label_list[i].text())
                    return 1
            if isinstance(item, QtGui.QComboBox):
                values.append(str(item.currentText()))
            i = i + 1

        ask_info = showComfirmDialog(self, u"是否添加该用户信息？")
        if ask_info == 1:
            return 1
        values = [get_user_id()] + values
        status = Sql("auth").add(values)
        if status == 1:
            showWarnDialog(self, u"添加用户信息失败！")
            ERROR(u"Add user failed! user: %s, values: %s" % (unicode(query_current_user()[1]), unicode(values)))
        else:
            showMessageDialog(self, u"添加用户信息成功！")
            INFO(u"Add user success! user: %s, add user: %s" % (unicode(query_current_user()[1]), unicode(values[1])))
            self.close()
        return 0


def main(object=None):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    MainWindow_1 = AddUser(object)
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    return MainWindow_1

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app1 = QtGui.QApplication(sys.argv)
    MainWindow_1 = AddUser()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    MainWindow_1.show()
    sys.exit(app1.exec_())





