import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MyUnixClock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('alarm')
        self.setGeometry(600, 600, 470, 280)

        when = [
            'once',
            'daily'
        ]

        all_days = [
            'Monday', 
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]

        for tt in range(3):    
            self.time = QLineEdit(self)
            self.time.setMaxLength(2)
            self.time.move(47 * tt + 165, 20)
            self.time.resize(40, 30)

        for cc in range(2):
            self.colon = QLabel(self)
            self.colon.setText(':')
            self.colon.move(47 * cc + 207, 22)

        # self.weekdays = QLabel('Weekdays', self)
        # self.weekdays.move(60, 50)

        for dd in range(6):
            self.days = QCheckBox(all_days[dd], self)
            self.days.move(50, dd * 30 + 70)
            self.days.resize(120, 30)
        
        for ww in range(2):
            self.count = QCheckBox(when[ww], self)
            self.count.move(200, ww * 30 + 130)
            self.count.resize(70, 30)
        
        self.alarm_button = QPushButton('Set an alarm', self)
        self.alarm_button.move(300, 145)
        self.alarm_button.resize(120, 30)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUnixClock()
    ex.show()
    sys.exit(app.exec())
