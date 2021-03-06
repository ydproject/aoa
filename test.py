# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from util import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle(self.tr("打印机"))
        self.text = QTextEdit()
        self.setCentralWidget(self.text)

        self.createActions()
        self.createMenus()
        self.createToolBars()

        file = QFile("requirement.txt")
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            textStream = QTextStream(file)
            while not textStream.atEnd():
                self.text.append(textStream.readLine())
        file.close()

    def createActions(self):
        self.PrintAction = QAction(QIcon("images/print.png"), self.tr("打印"), self)
        self.PrintAction.setShortcut("Ctrl+P")
        self.PrintAction.setStatusTip(self.tr("打印"))
        self.connect(self.PrintAction, SIGNAL("triggered()"), self.slotPrint)

    def createMenus(self):
        PrintMenu = self.menuBar().addMenu(self.tr("打印"))
        PrintMenu.addAction(self.PrintAction)

    def createToolBars(self):
        fileToolBar = self.addToolBar("Print")
        fileToolBar.addAction(self.PrintAction)

    def slotPrint(self):
        self.on_htmlButton_clicked()
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_():
            doc = self.text.document()
            doc.print_(printer)

    def on_htmlButton_clicked(self):
        printer = QPrinter()
        # /* 打印预览 */
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(printHtml)
        preview.exec_()


def printHtml(printer):
    textDocument = QTextDocument()
    textDocument.setHtml(html_text)
    # textDocument.print(printer)
    textDocument.print_(printer)


html_text = stu_addmoney_print([u'20180001', u'201803', u'1200', u'100,0,0', u'60,60,0', u'1200', u'0'], [u'20180001', u'201803', u'1200', u'100,100,0', u'60,60,0', u'1200', u'0'], 200)
# html_text = stu_addpre_print("20180001", -100)
print html_text



app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec_()

# print os.path.abspath(__file__)