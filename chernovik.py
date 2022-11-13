import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLCDNumber, QComboBox, QVBoxLayout, QLayoutItem
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MyUnixClock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    bin_color = ["background-color : darkgrey", "background-color : yellow"]

    def initUI(self):
        self.setWindowTitle('UNIX Time')
        self.setGeometry(600, 600, 600, 500)

        self.unix_time = QLCDNumber(self)
        self.unix_time.setNumDigits(10)
        self.unix_time.move(245, 20)
        self.unix_time.resize(110, 40)
        self.unix_time.setFrameShape(QFrame.Shape.Panel)

        self.time = QComboBox(self)
        self.time.addItem('UTC')
        self.time.addItem('local')
        self.time.move(480, 17)
        self.time.resize(100, 30)
        self.choise = 'UTC'

        self.time.activated[str].connect(self.time_format_connection)

        self.color = QComboBox(self)
        self.color.addItem('warm_sun')
        self.color.addItem('decorative rose')
        self.color.addItem('summer grass')
        self.color.addItem('winter morning')
        self.color.move(20, 17)
        self.color.resize(130, 30)

        self.color.activated[str].connect(self.color_selection)

        # self.vertical = QVBoxLayout(self)
        # self.vertical.addItem(QLayoutItem(Qt.Alignment(Qt.AlignmentFlag.)))

        self.bin_unix = []
        for y in range(4):
            self.bin_unix.append([])
            for x in range(8):
                btn = QPushButton(self)
                btn.move(65 * x + 40, 55 * y + 75)
                btn.resize(60, 50)
                btn.setEnabled(False)
                btn.setStyleSheet(MyUnixClock.bin_color[0])
                self.bin_unix[-1].append(btn)

        self.hours = QLabel(self)
        self.hours.setText('hours')
        self.hours.move(10, 350)

        self.minutes = QLabel(self)
        self.minutes.setText('minutes')
        self.minutes.move(10, 400)

        self.seconds = QLabel(self)
        self.seconds.setText('seconds')
        self.seconds.move(10, 450)

        self.bin_hhmmss = []
        for y in range(3):
            self.bin_hhmmss.append([])
            for x in range(6):
                btn = QPushButton(self)
                btn.move(55 * x + 75, 50 * y + 340)
                btn.resize(50, 45)
                btn.setEnabled(False)
                btn.setStyleSheet(MyUnixClock.bin_color[0])
                self.bin_hhmmss[-1].append(btn)
        
        self.hh_label = QLabel(self)
        self.hh_label.setText('h')
        self.hh_label.move(410, 350)

        self.mm_label = QLabel(self)
        self.mm_label.setText('m')
        self.mm_label.move(407, 400)

        self.ss_label = QLabel(self)
        self.ss_label.setText('s')
        self.ss_label.move(410, 450)
        
        self.hhmmss = []
        for i in range(3):
            btn = QLCDNumber(self)
            btn.move(425, 50 * i + 345)
            btn.resize(50, 33)
            self.hhmmss.append(btn)

        self.year = QLabel(self)
        self.year.setText('year')
        self.year.move(490, 350)

        self.month = QLabel(self)
        self.month.setText('month')
        self.month.move(490, 400)

        self.day = QLabel(self)
        self.day.setText('day')
        self.day.move(490, 450)
        
        self.yyyymmdd = []
        for i in range(3):
            btn = QLCDNumber(self)
            btn.move(540, 50 * i + 345)
            btn.resize(50, 33)
            self.yyyymmdd.append(btn)

        self.second_timer = QTimer()
        self.second_timer.timeout.connect(self.on_second_timer)
        self.second_timer.start(1000)

        self.alarm = QPushButton('alarm', self)
        self.alarm.move(480, 305)
        self.alarm.resize(100, 30)

    format_hhmmss = ["hh", "mm", "ss"]
    format_yyyymmdd = ["yyyy", "MM", "dd"]
    def on_second_timer(self):
        if self.choise == 'UTC':
            now = QDateTime.currentDateTimeUtc() # перенести UTC и local в массив и вызывать по элементу
        elif self.choise == 'local':
            now = QDateTime.currentDateTime()
        for i in range(3):
            self.hhmmss[i].display(now.toString(MyUnixClock.format_hhmmss[i]))
            self.yyyymmdd[i].display(now.toString(MyUnixClock.format_yyyymmdd[i]))
        now_time = now.time()
        self.display_bin(now_time.hour(), self.bin_hhmmss[0])
        self.display_bin(now_time.minute(), self.bin_hhmmss[1])
        self.display_bin(now_time.second(), self.bin_hhmmss[2])
        now_unix = now.currentSecsSinceEpoch()
        self.unix_time.display(now_unix)
        self.display_unix_bin(now_unix, self.bin_unix)

    def display_bin(self, val: int, where):
        bin_val = bin(val)[2:]  # remove leading 0b
        while len(bin_val) < 6:
            bin_val = '0' + bin_val
        for i in range(len(bin_val) - 1, -1, -1):
            where[i].setStyleSheet(MyUnixClock.bin_color[int(bin_val[i])])

    def display_unix_bin(self, val: int, where):
        bin_val = bin(val)[2:]  # remove leading 0b
        while len(bin_val) < 32:
            bin_val = '0' + bin_val
        for row in range(3, -1, -1):
            for col in range(7, -1, -1):
                where[row][col].setStyleSheet(MyUnixClock.bin_color[int(bin_val[row * 8 + col])])

    def color_selection(self, clr):
        if clr == 'warm sun':
            MyUnixClock.bin_color[1] = "background-color : yellow"
        if clr == 'decorative rose':
            MyUnixClock.bin_color[1] = "background-color : darkred"
        if clr == 'summer grass':
            MyUnixClock.bin_color[1] = "background-color : darkgreen"
        if clr == 'winter morning':
            MyUnixClock.bin_color[1] = "background-color : darkblue"


    def time_format_connection(self, frmt_tm):
        self.choise = frmt_tm










if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUnixClock()
    ex.show()
    sys.exit(app.exec())
