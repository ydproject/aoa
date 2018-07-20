# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import addstudent, selstudent, addmoney, selmoney, adduser, changeuser, changepasswd, selectmoney, preaddmoney
from util import *


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.resize(650, 450)
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'icon/png_2.png')))
        # 学生信息菜单子菜单
        self.addstu = QtGui.QAction(u'添加学生信息', self)
        self.connect(self.addstu, QtCore.SIGNAL('triggered()'), self.adds)
        self.selstu = QtGui.QAction(u'查询学生信息', self)
        self.connect(self.selstu, QtCore.SIGNAL('triggered()'), self.sels)
        # 缴费信息菜单子菜单
        self.addmoney = QtGui.QAction(u'首次缴费', self)
        self.connect(self.addmoney, QtCore.SIGNAL('triggered()'), self.addm)
        self.modifymoney = QtGui.QAction(u'学生缴费', self)
        self.connect(self.modifymoney, QtCore.SIGNAL('triggered()'), self.modifm)
        self.selecmoney = QtGui.QAction(u'查询缴费', self)
        self.connect(self.selecmoney, QtCore.SIGNAL('triggered()'), self.select_money)
        self.preaddmoney = QtGui.QAction(u'预收查询', self)
        self.connect(self.preaddmoney, QtCore.SIGNAL('triggered()'), self.pre_add_money)
        # 用户信息菜单子菜单
        self.chpasswd = QtGui.QAction(u'修改密码', self)
        self.connect(self.chpasswd, QtCore.SIGNAL('triggered()'), self.chpass)
        self.adduser = QtGui.QAction(u'添加用户', self)
        self.connect(self.adduser, QtCore.SIGNAL('triggered()'), self.addu)
        self.chuser = QtGui.QAction(u'切换用户', self)
        self.connect(self.chuser, QtCore.SIGNAL('triggered()'), self.chus)
        # 帮助菜单子菜单
        exit = QtGui.QAction(QtGui.QIcon('icon/x.png'), u'退出', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        # 学生信息菜单栏
        menubar1 = self.menuBar()
        file1 = menubar1.addMenu(u'学籍信息管理')
        file1.addAction(self.addstu)
        file1.addAction(self.selstu)
        # 缴费信息菜单栏
        menubar5 = self.menuBar()
        file5 = menubar5.addMenu(u'缴费信息管理')
        file5.addAction(self.addmoney)
        file5.addAction(self.modifymoney)
        file5.addAction(self.selecmoney)
        file5.addAction(self.preaddmoney)
        #用户管理菜单
        menubar4 = self.menuBar()
        file4 = menubar4.addMenu(u'用户管理')
        file4.addAction(self.chpasswd)
        file4.addAction(self.adduser)
        file4.addAction(self.chuser)
        # 帮助菜单栏
        menubar = self.menuBar()
        file = menubar.addMenu(u'帮助')
        file.addAction(exit)

        self.initUI()

    def initUI(self):
        self.auth = query_current_user()
        self.setWindowTitle(u'学生信息管理系统(用户：%s)' % self.auth[1])
        if self.auth[2] == "Guest":
            self.addstu.setDisabled(True)
        else:
            self.addstu.setDisabled(False)
        if self.auth[2] != "Admin":
            self.adduser.setDisabled(True)
        else:
            self.adduser.setDisabled(False)
        if self.auth[2] == "Guest":
            self.addmoney.setDisabled(True)
        else:
            self.addmoney.setDisabled(False)
        if self.auth[2] == "Guest":
            self.chpasswd.setDisabled(True)
        else:
            self.chpasswd.setDisabled(False)

    # 点击按钮响应函数
    def pre_add_money(self):
        self.premoney = preaddmoney.main()
        self.premoney.show()

    def addm(self):
        if query_current_user()[2] == "Guest":
            showWarnDialog(self, u"权限不足！")
            return
        self.addmoney = addmoney.main()
        self.addmoney.show()

    def modifm(self):
        self.selmoney = selmoney.main()
        self.selmoney.show()

    def adds(self):
        if query_current_user()[2] == "Guest":
            showWarnDialog(self, u"权限不足！")
            return
        self.addstudent = addstudent.main()
        self.addstudent.show()

    def sels(self):
        self.selstudent = selstudent.main()
        self.selstudent.show()

    def chpass(self):
        if query_current_user()[2] == "Guest":
            showWarnDialog(self, u"请先切换用户！")
            return
        self.changepass = changepasswd.main()
        self.changepass.show()

    def addu(self):
        if query_current_user()[2] != "Admin":
            showWarnDialog(self, u"权限不足！")
            return
        self.adduser = adduser.main()
        self.adduser.show()

    def chus(self):
        self.chuser = changeuser.main(self)
        self.chuser.show()

    def select_money(self):
        self.selmon = selectmoney.main()
        self.selmon.show()

if __name__ == "__main__":
    init_user()
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("icon/bkg4.jpg")))
    main.setPalette(palette)
    main.show()
    sys.exit(app.exec_())