import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QCheckBox, QInputDialog, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.Qt import QColor

import psutil
import utils
import py_compile
import os
import time
from multiprocessing import Process, Queue


class Demo(QtWidgets.QMainWindow):                  # 继承的类
    def __init__(self):
        super(Demo, self).__init__()                # 对继承自父类的属性进行初始化
        self.setObjectName("Main_widget")           # 创建整体UI
        self.mainName = "郝yj 的 OJ"
        self.setWindowTitle("郝yj 的 OJ")           # GUI 名称
        self.resize(1920, 1080)                     # GUI 大小

        self.m_flag = False                         # m_flag -> move_flag 表示GUI是否移动

        # 这里设置使用的字体，本项目中的所有字体即设置如下
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")      # 设置字体
        self.font.setBold(True)                     # 粗体
        self.font.setPointSize(11)                  # 字的大小

        self.staticId = 0               # staticId是一个递增的id号，对于每一个测试点，将采用独立的测试id号

        ######################
        #     test cases
        ######################
        self.testcasesLabel = QLabel("TestCases", self)                 # 设置testcases的相关字样
        self.testcasesLabel.setFont(self.font)                          # 设置字体
        self.testcasesLabel.setGeometry(QtCore.QRect(50, 50, 100, 30))  # 设置位置长宽
        self.testcasesLabel.setStyleSheet("""QWidget{}""")              # 设置风格，这里为默认风格

        # 以下为存储所有的测试点名字的容器
        self.testcases = {}                     # 用一个字典存储测试点
        self.testcasesNames = []                # 存储所有的测试点的名字
        self.testcasesButton = []               # 存储当前页面的所有测试点的按钮
        self.testcasesButtonAll = []            # 存储所有的测试点的按钮
        self.testcasesAll = []                  # 存储所有的测试点
        self.nowpage = 1                        # 存储当前页面的编号
        self.maxpage = 1                        # 存储一共有多少页面

        ######################
        #     Pages
        ######################
        self.pushLast = QPushButton("last", self)                               # 上一页按钮
        self.pushNext = QPushButton("next", self)                               # 下一页按钮
        self.pushLast.setFont(self.font)                                        # 字体
        self.pushNext.setFont(self.font)
        self.pushLast.setStyleSheet("""QPushButton:hover{background:red;}""")   # 风格，鼠标放上去变成红色
        self.pushNext.setStyleSheet("""QPushButton:hover{background:red;}""")
        self.pages = QLabel("1/1", self)                                        # 页面的Label，先设置为1/1，后续调整
        self.maxInPage = 10                                                     # 设置一页最多展示多少测试点
        self.pushLast.clicked.connect(self.lastPage)                            # 链接函数，按钮被按下将执行什么功能
        self.pushNext.clicked.connect(self.nextPage)

        ######################
        #     input boxes
        ######################
        self.inputBox = QTextEdit(self)                                         # 代码输入窗口
        self.inputBox.setGeometry(QtCore.QRect(200, 10, 1650, 700))             # 设置位置

        ######################
        #     set input
        ######################
        self.testcaseInput = QLabel("Standard Input", self)                     # 设置standard input 字样相关属性
        self.testcaseInput.setGeometry(QtCore.QRect(200, 720, 200, 20))
        self.testcaseInput.setFont(self.font)

        self.standardInput = QTextEdit(self)                                    # 设置标准输入的输入窗口
        self.standardInput.setGeometry(QtCore.QRect(200, 740, 1650, 80))
        self.standardInput.setFont(self.font)
        # self.standardInput.setFontItalic(True)                                  # 斜体
        self.standardInput.setTextColor(QColor(100, 0, 0))                      # 文本字体颜色
        self.standardInput.setStyleSheet("""QWidget{background:white;}""")       # 背景为白色

        ######################
        #     set output
        ######################
        self.testcaseOutput = QLabel("Standard Output", self)                   # 设置standard output 字样相关属性
        self.testcaseOutput.setGeometry(QtCore.QRect(200, 820, 200, 20))
        self.testcaseOutput.setFont(self.font)

        self.standardOutput = QTextEdit(self)                                   # 设置标准输出的文字框相关属性
        self.standardOutput.setGeometry(QtCore.QRect(200, 840, 1650, 80))
        self.standardOutput.setFont(self.font)
        # self.standardOutput.setFontItalic(True)
        self.standardOutput.setTextColor(QColor(0, 100, 0))
        self.standardOutput.setStyleSheet("""QWidget{background:white;}""")

        ######################
        #     your output
        ######################
        self.yourOutputLable = QLabel("Your Output", self)                      # 设置Your Output 字样属性
        self.yourOutputLable.setGeometry(QtCore.QRect(200, 920, 200, 20))
        self.yourOutputLable.setFont(self.font)

        self.yourOutput = QTextEdit(self)                                       # 设置Your Output 文字框相关属性
        self.yourOutput.setGeometry(QtCore.QRect(200, 940, 1650, 80))
        self.yourOutput.setFont(self.font)
        # self.yourOutput.setFontItalic(True)
        self.yourOutput.setTextColor(QColor(0, 0, 100))
        self.yourOutput.setStyleSheet("""QWidget{background:white;}""")


        ######################
        #     Input Box
        ######################
        self.inputBox.setFont(self.font)                    # 设置代码文字框的相关属性
        # self.inputBox.setFontItalic(True)
        self.inputBox.setTextColor(QColor(100, 100, 100))
        self.inputBox.setStyleSheet("""QWidget{background:white;}""")

        # 设置开始测试的按钮的属性
        self.beginTest = QPushButton("Test", self)
        self.beginTest.setFont(self.font)
        self.beginTest.setGeometry(QtCore.QRect(50, 540, 100, 30))
        self.beginTest.clicked.connect(self.testTheCode)
        self.beginTest.setStyleSheet("""QPushButton:hover{background:green;}""")

        # 设置清空代码框的按钮的属性
        self.clearInputBox = QPushButton("Clear Codes", self)
        self.clearInputBox.setGeometry(QtCore.QRect(50, 640, 100, 30))
        self.clearInputBox.setFont(self.font)
        self.clearInputBox.clicked.connect(self.clearCodeInput)
        self.clearInputBox.setStyleSheet("""QPushButton:hover{background:red;}""")

        # 设置清空测试信息按钮的属性
        self.clearTestCase = QPushButton("Clear Test", self)
        self.clearTestCase.setFont(self.font)
        self.clearTestCase.setGeometry(QtCore.QRect(50, 740, 100, 30))
        self.clearTestCase.clicked.connect(self.clearTestInput)
        self.clearTestCase.setStyleSheet("""QPushButton:hover{background:red;}""")

        # 设置保存测试点的相关属性
        self.saveTestCase = QPushButton("Save Case", self)
        self.saveTestCase.setFont(self.font)
        self.saveTestCase.setGeometry(QtCore.QRect(50, 840, 100, 30))
        self.saveTestCase.clicked.connect(self.saveTestCaseFunc)
        self.saveTestCase.setStyleSheet("""QPushButton:hover{background:red;}""")

        #######################
        #     Limit
        #######################
        # 设置最大时间限制的相关内容
        self.timeLimitLabel = QLabel("TimeLimit", self)
        self.timeLimitLabel.setFont(self.font)
        self.timeLimitLabel.setGeometry(QtCore.QRect(0, 400, 150, 30))
        self.timeLimit = QLineEdit("2.0", self)
        self.timeLimit.setFont(self.font)
        self.timeLimit.setStyleSheet("""QLineEdit:hover{background:white;}""")
        self.timeLimit.setGeometry(QtCore.QRect(150, 400, 50, 30))
        self.maxTime = 2.0

        # 设置最大内存限制的相关内容
        self.memoryLimitLable = QLabel("MemoryLimit", self)
        self.memoryLimitLable.setFont(self.font)
        self.memoryLimitLable.setGeometry(QtCore.QRect(0, 450, 150, 30))
        self.memoryLimit = QLineEdit("16", self)
        self.memoryLimit.setFont(self.font)
        self.memoryLimit.setGeometry(QtCore.QRect(150, 450, 50, 30))
        self.memoryLimit.setStyleSheet("""QLineEdit:hover{background:white;}""")
        self.maxMemory = 16

        ##########################
        #      three points
        ##########################
        # 设置左上角 关闭，最小化，还原 三个按钮
        # 关闭按钮的相关功能
        self.left_close = QPushButton("", self)
        self.left_close.setGeometry(QtCore.QRect(20, 20, 15, 15))
        self.left_close.setFixedSize(15, 15)
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_close.clicked.connect(self.closeTheWindow)

        # 最小化按钮的相关功能
        self.left_mini = QPushButton("", self)
        self.left_mini.setGeometry(QtCore.QRect(50, 20, 15, 15))
        self.left_mini.setFixedSize(15, 15)
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_mini.clicked.connect(self.minTheWindow)

        # 最大化按钮的相关功能
        self.left_max = QPushButton("", self)
        self.left_max.setGeometry(QtCore.QRect(80, 20, 15, 15))
        self.left_max.setFixedSize(15, 15)
        self.left_max.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_max.clicked.connect(self.maxTheWindow)

        self.loadTestSets()                                 # 打开时首先将保存的测试点全部读取出来
        self.setWindowOpacity(1)                            # 设置窗口的透明度
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)   # 设置无边框
        self.setStyleSheet(                                 # 设置整体的风格
            """QWidget{background:grey;border-radius:10px;}QLineEdit:hover{background:white;}""")

    ###############################################
    #       three points
    ###############################################
    def closeTheWindow(self):       # 关闭UI窗口
        self.close()

    def minTheWindow(self):         # 最小化UI窗口
        self.showMinimized()

    def maxTheWindow(self):         # 最大化UI窗口
        self.move(QtCore.QPoint(0, 0))

    #############################################
    #       mouse press
    #############################################
    def mousePressEvent(self, event):
        """当鼠标左键按下去后，记录按下去的坐标"""
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 按下鼠标左键后鼠标变成小手

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))         # 释放鼠标后鼠标又变回箭头

    def mouseMoveEvent(self, event):                    # 鼠标按下并且拖动的时候
        if Qt.LeftButton and self.m_flag :              # 使整个窗体移动
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    #############################################
    #       load testsets
    #############################################
    def loadTestSets(self):
        lst = os.listdir("standard_input")              # listdir 罗列出所有的测试文件
        lst = [item.split(".")[0] for item in lst]      # lst保存其所有测试点名字

        maxInPage = self.maxInPage
        self.maxpage = len(lst) // maxInPage            # 根据测试点数目，记录最大页面数
        if len(lst) % maxInPage > 0:
            self.maxpage += 1
        if len(lst) == 0:                               # 当没有测试点的时候，最大页面数为0
            self.maxpage = 1
        self.testcasesAll = [name for name in lst]      # 将所有的测试点的名字保存在testcasesAll中
        self.testcasesButtonAll = []                    # 为每一个测试点，创建一个按钮
        for name in self.testcasesAll:
            button = QCheckBox(name, self)
            button.hide()                               # hide方法，让按钮不显示出来
            self.testcasesButtonAll.append(button)
            self.testcases[name] = button               # 保存在字典里，可以通过名字来索引按钮
        if len(lst) >= maxInPage:                       # 首先判断当前页面应该容纳多少测试点，再进行show
            self.showTestSets(self.testcasesAll[:maxInPage])
        else:
            self.showTestSets(self.testcasesAll[:])

    # 这个方法对于传入的测试点名字，进行展示
    def showTestSets(self, testcases):
        x = 10
        y = 70
        interval = 30
        self.testcasesNames = testcases         # 这两个属性将保存当前页面所展示的测试点的名字和按钮
        self.testcasesButton = []
        for name in testcases:
            button = self.testcases[name]       # 通过字典，以及名字，索引得到按钮
            button.show()                       # show方法，让按钮显示出来
            button.setFont(self.font)
            button.setGeometry(QtCore.QRect(x, y, 180, 27))  # 设置按钮的位置，按顺序的y进行递增
            self.testcasesButton.append(button)             # 保存当前的按钮
            y += interval
        self.pushLast.setGeometry(QtCore.QRect(5, 370, 50, 20))             # 设置上一页按钮的位置
        self.pushNext.setGeometry(QtCore.QRect(140, 370, 50, 20))           # 设置下一页按钮的位置
        self.pages.setText(str(self.nowpage) + "/" + str(self.maxpage))     # 根据当前是哪一页及最大页面，设置目录
        self.pages.setFont(self.font)
        self.pages.setGeometry(QtCore.QRect(80, 370, 40, 20))

    # 这个函数将被用在翻页的按钮中，翻页将隐藏当前页面的所有按钮
    def clearButtons(self):
        for button in self.testcasesButton:
            button.hide()

    # 翻页
    def nextPage(self):
        if self.nowpage != self.maxpage:
            self.clearButtons()
            self.nowpage += 1
            if self.nowpage + 1 == self.maxpage:
                self.showTestSets(self.testcasesAll[self.nowpage * self.maxInPage - self.maxInPage:
                                                    self.nowpage * self.maxInPage])
            else:
                self.showTestSets(self.testcasesAll[self.nowpage * self.maxInPage - self.maxInPage:])
    # 上一页
    def lastPage(self):
        if self.nowpage != 1:
            self.clearButtons()
            self.nowpage -= 1
            self.showTestSets(self.testcasesAll[self.nowpage * self.maxInPage - self.maxInPage:
                                                self.nowpage * self.maxInPage])
    # 清空输入代码框的内容
    def clearCodeInput(self):
        self.inputBox.clear()

    # 清空测试样例数据框的内容
    def clearTestInput(self):
        self.standardInput.clear()
        self.standardOutput.clear()

    # 保存测试点
    def saveTestCaseFunc(self):
        standardInput = self.standardInput.toPlainText()            # 读取标准输入的内容
        standardOutput = self.standardOutput.toPlainText()          # 读取标准输出的内容

        # 弹出对话框，得到保存测试点的相关名字
        name, ok = QInputDialog.getText(self, "Save TestCase", "测试点保存名字", QLineEdit.Normal, "")
        if ok:
            # 如果名字为空则不保存
            if len(name) != 0:
                self.saveFile(standardInput, "./standard_input/{}.in".format(name))
                self.saveFile(standardOutput, "./standard_output/{}.out".format(name))
                self.clearButtons()
                self.loadTestSets()
            else:
                QMessageBox.information(self, "Error", "输入文件名不可为空", QMessageBox.Yes)

    ########################################################################
    #       测试 相关 代码
    ########################################################################
    # 读取两个limits，如果数据大小和类型有错误，则弹窗进行提醒
    def loadLimits(self):
        temp = self.timeLimit.text()
        try:
            self.maxTime = float(temp)
        except:
            QMessageBox.information(self, "Error", "<font size='14' color='red'>Please input time with float number.</font>", QMessageBox.Yes)
            return False
        if self.maxTime <= 0:
            QMessageBox.information(self, "Error", "<font size='14' color='red'>Please input time larger than zero.</font>", QMessageBox.Yes)
            return False
        temp = self.memoryLimit.text()
        try:
            self.maxMemory = int(temp)
        except:
            QMessageBox.information(self, "Error", "<font size='14' color='red'>Please input memory with integer.</font>", QMessageBox.Yes)
            return False
        if self.maxMemory <= 0:
            QMessageBox.information(self, "Error", "<font size='14' color='red'>Please input memory larger than zero.</font>", QMessageBox.Yes)
            return False
        return True

    # 点击test后进行该函数进行函数测试
    def testTheCode(self):
        # 首先加载对应的limits
        if not self.loadLimits():
            return
        code = self.inputBox.toPlainText()                      # 读取用户的代码
        standardInput = self.standardInput.toPlainText()        # 读取标准输入中的内容
        standardOutput = self.standardOutput.toPlainText()      # 读取标准输出中的内容

        self.saveFile(code, "code.py")                           # 将用户的代码保存为"code.py"
        if len(standardInput) != 0 or len(standardOutput) != 0:  # 如果标准输入标准输出不为空，则也保存
            self.saveFile(standardInput, "temp.in")
            self.saveFile(standardOutput, "temp.out")
            self.testByOneCase("code.py", "temp.in", "temp.out")    # 进行单一测试点的测试
        else:
            self.testByTestCases()                                  # 如果上标准输入输出为空，则认为采用多测试点测试（只选择一个已保存测试点也认为是多测试点）

    # 这个函数用于判断该程序是否会出来TLE MLE等错误
    def testWhetherTle(self, testfile, standardIn, standardOut, name):
        q = Queue()
        p2 = Process(target=utils.process_test_tle, name=name, args=(testfile, standardIn, name, q,))  # 用户程序进程
        p1 = Process(target=utils.calculateTime, args=(self.maxTime, self.maxMemory, name, q,))        # 统计进程
        p2.start()      # 两个进程开始运行
        p1.start()
        p1.join()       # join的意思是阻塞在这里，等待统计进程结束才继续进行
        value = q.get() # 统计进程结束后，从q管道中取得返回值
        self.killAllChildren(p2.pid)    # 由于统计进程已经结束，强制杀死所有的用户程序子进程
        if value == '1':        # 返回值为1，表示为MLE
            return 1
        elif value == '2':      # 返回值为2，表示为TLE
            return 2
        else:                   # 返回值为0，表示无上述两种错误
            return 0

    # 杀死所有的子进程
    def killAllChildren(self, pid):
        try:
            proc = psutil.Process(pid)              # 根据进程id号，得到该进程
            lst = proc.children()                   # 再得到其子进程的列表
            if len(lst) == 0:                       # 如果无子进程，即返回
                return
            for proc in lst:                        # 否则
                self.killAllChildren(proc.pid)      # 递归杀死所有的子进程
                proc.terminate()
        except:
            return

    # 测试一个测试点
    def testByOneCase(self, testfile, standardIn, standardOut, flag=True):

        # testfile:        测试用户程序的名称
        # standardIn:      测试的标准输入名称
        # standardOut:     测试的标准输出的名称
        # flag:            flag标记是单测试点测试 还是多测试点测试

        name = "test_" + str(self.staticId)     # 对于每个测试点，递增staticId得到独立的名称
        self.staticId += 1
        value = self.testWhetherTle(testfile, standardIn, standardOut, name)        # 测试是否tle或者mle
        if value == 2:
            self.isTimeLimitError(name, flag)
            return 3
        elif value == 1:
            self.isMemoryLimitError(name, flag)
            return 4
        p = Process(target=utils.process, args=(testfile, standardIn, name))        # 没有tle或者mle时，再进行一次测试
        p.start()
        p.join()
        if self.judgeComplierError():                   # 用一个函数判断是否Compiler Error
            self.isComplierError(name, flag)
            return 2
        if self.hasError(name + "_error.out"):          # 如果程序报错，则认为WA
            self.isWrongAnswer(name, flag)
            return 1
        else:
            if self.compare(standardOut, name + "_result.out"):     # 结果比较，如果相同则认为AC
                self.isAccepted(name, flag)
                return 0
            else:
                self.isWrongAnswer(name, flag)                      # 结果比较，不同则认为WA
                return 1

    # 判断是否编译错误
    def judgeComplierError(self):
        try:
            # 这里使用py_compile库进行编译，判断是否有错误
            py_compile.compile("code.py", doraise=True)  #
        except py_compile.PyCompileError:
            return True
        return False

    # 判断是否有抛出的错误
    def hasError(self, name):
        # 读取错误输出文件，如果输出文件中有相应内容，表示有错误
        f = open(name, "r")
        lines = f.readlines()
        if len(lines) > 0:
            return True
        else:
            return False

    ################################################
    #       接下来的五个函数，进行结果的展示
    ################################################
    # 接下来的函数，会根据传入的名字，将结果输出、以及错误输出文件进行删除
    # flag的作用为，
    # 如果为True，表示其为单测试文件，则直接输出即可
    # 如果为False，表示为多测试文件，不弹窗输出
    def isMemoryLimitError(self, name, flag):
        os.remove(name + "_echo.py")
        self.yourOutput.setText("")
        if flag:
            str = "<font size='26' color='red'>Memory Limit Error</font>"
            QMessageBox.information(self, "Bad News", str, QMessageBox.Yes | QMessageBox.No)

    def isTimeLimitError(self, name, flag):
        os.remove(name + "_echo.py")
        self.yourOutput.setText("")
        if flag:
            str = "<font size='26' color='red'>Time Limit Error</font>"
            QMessageBox.information(self, "Bad News", str, QMessageBox.Yes | QMessageBox.No)

    def isComplierError(self, name, flag):
        self.yourOutput.setText("")
        if flag:
            self.loadYourOutput(name)
            self.removeTempFiles(name)
            str = "<font size='26' color='red'>Compiler Error</font>"
            QMessageBox.information(self, "Bad News", str, QMessageBox.Yes | QMessageBox.No)
        else:
            self.removeTempFiles(name)

    def isAccepted(self, name, flag):
        self.yourOutput.setText("")
        if flag:
            self.loadYourOutput(name)
            self.removeTempFiles(name)
            str = "<font size='26' color='green'>Accepted</font>"
            QMessageBox.information(self, "Congradulations", str, QMessageBox.Yes | QMessageBox.No)
        else:
            self.removeTempFiles(name)

    def isWrongAnswer(self, name, flag):
        self.yourOutput.setText("")
        if flag:
            self.loadYourOutput(name)
            self.removeTempFiles(name)
            str = "<font size='26' color='red'>Wrong Answer</font>"
            QMessageBox.information(self, "Bad News", str, QMessageBox.Yes | QMessageBox.No)
        else:
            self.removeTempFiles(name)

    # 这个函数，将程序的结果放在your Output文字框中展示
    def loadYourOutput(self, name):
        str = ""
        f = open(name + "_result.out")
        lines = f.readlines()
        f.close()
        for line in lines:
            str += line
        f = open(name + "_error.out")
        lines = f.readlines()
        f.close()
        for line in lines:
            str += line
        self.yourOutput.setText(str)

    # 判断结果比较是否正确
    def compare(self, standardOut, result):
        f = open(standardOut, "r")
        g = open(result, "r")
        standardLines = f.readlines()
        resultLines = g.readlines()
        f.close()
        g.close()
        standardLines = self.deleteBlankLines(standardLines)
        resultLines = self.deleteBlankLines(resultLines)
        length1 = len(standardLines)
        length2 = len(resultLines)
        if length1 != length2:
            return False
        for i in range(length1):
            line1 = self.deleteblank(standardLines[i])
            line2 = self.deleteblank(resultLines[i])
            if line1 != line2:
                return False
        return True

    # 删除结果末尾的空行
    def deleteBlankLines(self, lines):
        for i in range(len(lines), 0, -1):
            line = lines[i - 1]
            if line == "" or line == "\n":
                continue
            else:
                return lines[:i]
        return []

    # 删除字符串结尾的空格与回车
    def deleteblank(self, line):
        for i in range(len(line), 0, -1):
            if line[i - 1] == '\n' or line[i - 1] == ' ':
                continue
            else:
                return line[:i]
        return ""

    # 删除一些中间文件
    def removeTempFiles(self, name):
        os.remove(name + "_echo.py")
        os.remove(name + "_error.out")
        os.remove(name + "_result.out")

    # 多文件测试
    def testByTestCases(self):
        lst = []
        strs = []
        str = ""
        output = ""
        for button in self.testcasesButtonAll:                  # 统计被选择的测试点
            if button.isChecked():                              # ischecked 表示该按钮是否被按下
                lst.append(button.text())
                strs.append(button.text() + "\tloading\n")
        if len(lst) == 0:                                       # 如果没有被选择的
            str = "There is no testcases selected!"             # 弹窗警告
            QMessageBox.information(self, "Bad News", str, QMessageBox.Yes | QMessageBox.No)
            return
        result = []
        ret = ["AC", "WA", "CE", "TLE", "MLE"]
        for i in range(len(lst)):                               # 对于每个测试点，进行挨个的测试
            output = str[:]
            for j in range(i, len(lst)):
                output += strs[j]
            self.setWindowTitle("Loading Complete {}/{}".format(i, len(lst)))   # 这句代码本来的是用来表示程序的执行的进度的
                                                                                # 但是为了美观隐藏了窗口，所以看不到了，如需检验只需注释掉上一行代码
            item = lst[i]
            result.append(self.testByOneCase("code.py", "./standard_input/{}.in".format(item),
                                             "./standard_output/{}.out".format(item), False))
            if result[i] == 0:
                str += "<font size='14'>" + item + " " * (10 - len(item)) + "</font><font size='14' color='green'>" + ret[result[i]] + "</font><br>"
            else:
                str += "<font size='14'>" + item + " " * (10 - len(item)) + "</font><font size='14' color='red'>" + ret[result[i]] + "</font><br>"
            time.sleep(1)

        self.setWindowTitle(self.mainName)
        if sum(result) != 0:        # 展示结果
            QMessageBox.information(self, "Bad News", str, QMessageBox.Yes | QMessageBox.No)
        else:
            QMessageBox.information(self, "Congradulations", str, QMessageBox.Yes | QMessageBox.No)


    def deleteFile(self, name):
        os.remove(name)

    def saveFile(self, file, name):
        f = open(name, "w")
        f.write(file)
        f.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Gui = Demo()
    Gui.show()
    sys.exit(app.exec_())