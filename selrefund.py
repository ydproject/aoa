# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from util import *
from log import INFO, ERROR


class Refund(QtGui.QWidget):

    def __init__(self, object=None, stu_id = ""):
        super(Refund, self).__init__()
        self.faWindows = object
        print stu_id
        self.stu_id = stu_id
        self.initUI()

    def initUI(self):
        frame = QtGui.QFrame(self)
        # 表格控件
        self.label_value = QtGui.QLabel(u"输入退费金额:")
        self.edit_value = QtGui.QLineEdit()
        self.edit_value.setFixedWidth(150)
        # 按钮控件
        selectButton = QtGui.QPushButton(frame)
        selectButton.setText(u'确认')
        selectButton.setFixedWidth(80)
        QtCore.QObject.connect(selectButton, QtCore.SIGNAL("clicked()"), self.confirm)


        modifyButton = QtGui.QPushButton(frame)
        modifyButton.setText(u'清空')
        modifyButton.setFixedWidth(80)
        QtCore.QObject.connect(modifyButton, QtCore.SIGNAL("clicked()"), self.clears)


        #布局vlayout = QtGui.QVBoxLayout()
        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.setColumnStretch(200, 200)
        grid1.setAlignment(QtCore.Qt.AlignLeft)
        grid1.addWidget(self.label_value, 1, 0)
        grid1.addWidget(self.edit_value, 1, 1)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.setColumnStretch(200, 200)
        grid2.setAlignment(QtCore.Qt.AlignLeft)
        grid2.addWidget(selectButton, 1, 0)
        grid2.addWidget(modifyButton, 1, 2)

        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(grid1)
        vlayout.addLayout(grid2)

        self.setLayout(vlayout)

        self.resize(200, 200)
        self.setWindowTitle(u'退费信息')
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QtGui.QIcon('icon/png12.png'))

    def clears(self):
        clear_text(self.edit_value)

    def confirm(self):
        try:
            money = 0 - round(abs(float(self.edit_value.text())),2)
        except Exception, e:
            return
        if money == 0:
            return
        num = add_flowing(self, str(money), self.stu_id, u"退费")
        if num == -1:
            showWarnDialog(self, u"退费失败！")
        else:
            showMessageDialog(self, u"退费成功！")
            html = u""
            try:
                html = stu_addflowing_print(num)
                res = showComfirmDialog(self, u"是否打印收据？")
                if res == 0:
                    print_html(html)
            except Exception,e :
                showWarnDialog(self, u"无法打印收据，请手动处理！")
                ERROR(u"Print html failed: html:%s error %s" % (html, traceback.format_exc()))
            self.faWindows.sels()
            self.close()
        return 0


def main(object=None, infos=[]):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    MainWindow_1 = Refund(object, infos)
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    return MainWindow_1

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app1 = QtGui.QApplication(sys.argv)
    MainWindow_1 = Refund()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_1.setPalette(palette)
    MainWindow_1.show()
    sys.exit(app1.exec_())





