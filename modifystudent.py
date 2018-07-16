# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import runpy, sys
import sqlite3


class MainWindow3(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(758, 414)
        self.setWindowTitle(u'修改学籍信息')
        self.setWindowIcon(QtGui.QIcon('icon/png5.png'))
        # 控件
        label = QtGui.QLabel(u'学号：', self)
        label.setGeometry(QtCore.QRect(60, 30, 61, 21))

        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        label.setFont(font)
        label_2 = QtGui.QLabel(u'姓名：', self)
        label_2.setGeometry(QtCore.QRect(330, 30, 61, 21))
        label_2.setFont(font)

        label_3 = QtGui.QLabel(u'性别：', self)
        label_3.setGeometry(QtCore.QRect(60, 70, 51, 21))
        label_3.setFont(font)

        label_4 = QtGui.QLabel(u'出生日期：', self)
        label_4.setGeometry(QtCore.QRect(330, 70, 71, 21))
        label_4.setFont(font)

        label_5 = QtGui.QLabel(u'班号：', self)
        label_5.setGeometry(QtCore.QRect(60, 110, 41, 20))
        label_5.setFont(font)

        label_6 = QtGui.QLabel(u'联系电话：', self)
        label_6.setGeometry(QtCore.QRect(330, 110, 71, 21))
        label_6.setFont(font)

        label_7 = QtGui.QLabel(u'入校日期：', self)
        label_7.setGeometry(QtCore.QRect(60, 152, 71, 21))
        label_7.setFont(font)

        label_8 = QtGui.QLabel(u'家庭住址：', self)
        label_8.setGeometry(QtCore.QRect(330, 150, 71, 21))
        label_8.setFont(font)

        label_9 = QtGui.QLabel(u'备注：', self)
        label_9.setGeometry(QtCore.QRect(60, 200, 51, 21))
        label_9.setFont(font)

        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(140, 30, 131, 20))

        self.lineEdit_2 = QtGui.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(410, 30, 131, 21))

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(140, 70, 91, 22))
        self.comboBox.addItem(u'男')
        self.comboBox.addItem(u'女')
        self.lineEdit_3 = QtGui.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(410, 70, 131, 20))

        self.comboBox_2 = QtGui.QComboBox(self)
        self.comboBox_2.setGeometry(QtCore.QRect(140, 110, 91, 22))
        self.comboBox_2.addItem('1')
        self.comboBox_2.addItem('2')
        self.comboBox_2.addItem('3')
        self.comboBox_2.addItem('4')
        self.comboBox_2.addItem('5')
        self.comboBox_2.addItem('6')

        self.lineEdit_4 = QtGui.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(410, 110, 131, 20))

        self.lineEdit_5 = QtGui.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(140, 150, 131, 20))

        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(410, 150, 131, 81))

        self.textEdit_2 = QtGui.QTextEdit(self)
        self.textEdit_2.setGeometry(QtCore.QRect(140, 200, 131, 81))

        groupBox = QtGui.QGroupBox(self)
        groupBox.setTitle(u'查看学籍信息')
        groupBox.setGeometry(QtCore.QRect(570, 30, 151, 211))
        groupBox.setFont(font)
        groupBox.setFlat(True)
        pushButton = QtGui.QPushButton(groupBox)
        pushButton.setText(u'第一条记录')
        pushButton.setGeometry(QtCore.QRect(30, 20, 101, 31))
        pushButton_2 = QtGui.QPushButton(groupBox)
        pushButton_2.setText(u'上一条记录')
        pushButton_2.setGeometry(QtCore.QRect(30, 60, 101, 31))
        pushButton_3 = QtGui.QPushButton(groupBox)
        pushButton_3.setText(u'下一条记录')
        pushButton_3.setGeometry(QtCore.QRect(30, 110, 101, 31))
        pushButton_4 = QtGui.QPushButton(groupBox)
        pushButton_4.setText(u'最后一条记录')
        pushButton_4.setGeometry(QtCore.QRect(30, 160, 101, 31))

        groupBox1 = QtGui.QGroupBox(self)
        groupBox1.setTitle(u'修改记录')
        groupBox1.setGeometry(QtCore.QRect(100, 300, 471, 71))
        groupBox1.setFont(font)
        groupBox1.setFlat(True)
        pushButton_5 = QtGui.QPushButton(groupBox1)
        pushButton_5.setText(u'修改记录')
        pushButton_5.setGeometry(QtCore.QRect(30, 30, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        pushButton_5.setFont(font)
        pushButton_6 = QtGui.QPushButton(groupBox1)
        pushButton_6.setText(u'取消修改')
        pushButton_6.setGeometry(QtCore.QRect(180, 30, 91, 31))
        pushButton_6.setFont(font)
        pushButton_7 = QtGui.QPushButton(groupBox1)
        pushButton_7.setText(u'删除记录')
        pushButton_7.setGeometry(QtCore.QRect(330, 30, 91, 31))
        pushButton_7.setFont(font)

        QtCore.QObject.connect(pushButton_6, QtCore.SIGNAL("clicked()"), self.lineEdit.clear)
        QtCore.QObject.connect(pushButton_6, QtCore.SIGNAL("clicked()"), self.lineEdit_2.clear)
        QtCore.QObject.connect(pushButton_6, QtCore.SIGNAL("clicked()"), self.lineEdit_3.clear)
        QtCore.QObject.connect(pushButton_6, QtCore.SIGNAL("clicked()"), self.lineEdit_4.clear)
        QtCore.QObject.connect(pushButton_6, QtCore.SIGNAL("clicked()"), self.lineEdit_5.clear)
        QtCore.QObject.connect(pushButton_6, QtCore.SIGNAL("clicked()"), self.textEdit.clear)
        QtCore.QObject.connect(pushButton_6, QtCore.SIGNAL("clicked()"), self.textEdit_2.clear)
        QtCore.QObject.connect(pushButton_5, QtCore.SIGNAL("clicked()"), self.modif)
        QtCore.QObject.connect(pushButton_7, QtCore.SIGNAL("clicked()"), self.delet)

    def modif(self):
        print 5
        conn = sqlite3.connect('example.db')
        cur = conn.cursor()
        v1 = str(self.lineEdit.text())
        v2 = str(self.lineEdit_2.text())
        v3 = str(self.comboBox.currentText())
        v4 = str(self.lineEdit_3.text())
        v5 = str(self.comboBox_2.currentText())
        v6 = str(self.lineEdit_4.text())
        v7 = str(self.lineEdit_5.text())
        v8 = str(self.textEdit.toPlainText())
        v9 = str(self.textEdit_2.toPlainText())
        sql = "update student_info set 姓名=%s,性别=%s,出生日期=%s,班号=%s,联系电话=%s,入校日期=%s,家庭住址=%s,备注=%s where 学号=%s"
        value = ((v2, v3, v4, v5, v6, v7, v8, v9, v1))
        cur.execute(sql, value)
        conn.commit()
        cur.close()
        conn.close()

    def delet(self):
        print 6
        conn = sqlite3.connect('example.db')
        cur = conn.cursor()
        v1 = str(self.lineEdit.text())
        sql = "delete from student_info where 学号=%s"
        value = ((v1))
        cur.execute(sql, value)
        conn.commit()
        cur.close()
        conn.close()

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    MainWindow_3 = MainWindow3()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_3.setPalette(palette)
    return MainWindow_3

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = QtGui.QApplication(sys.argv)
    MainWindow_3 = MainWindow3()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg5.jpg")))
    MainWindow_3.setPalette(palette)
    MainWindow_3.show()
    sys.exit(app.exec_())
