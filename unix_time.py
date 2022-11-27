import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from db import *
from alarms import *


class MyUnixClock(QMainWindow):
    """
    Первая, основная форма, которая показывается unix время.
    """

    def __init__(self):
        super().__init__()
        self._db = AlarmDb('alarms.sqlite')
        self._bin_color = self._db.pallettes
        self._form = MyUnixAlarms(self._db)
        self._msg_box = QMessageBox()
        self._msg_box.setIcon(QMessageBox.Information)
        self._msg_box.setWindowTitle("A L A R M")
        self._msg_box.setStandardButtons(QMessageBox.Ok)
        self._sound = QSound("sound/Alarm-ringtone.wav")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('UNIX Time')
        self.setGeometry(
            self._db.config.pos[0], self._db.config.pos[1], 600, 520)
        # изначально беру позицию x и y из бд,
        # то есть при закрытии программы и повторном открытии окно будет на том месте,
        # где его закрыли в прошлый раз. Это происходит за счет того, что я сохраняю в бд(config) позицию формы
        self.unix_time = QLCDNumber(self)
        self.unix_time.setNumDigits(10)
        self.unix_time.move(245, 20)
        self.unix_time.resize(110, 40)
        self.unix_time.setFrameShape(QFrame.Shape.Panel)

        self.time = QComboBox(self)
        for tz_id, tz in self._db.time_zones.items():
            self.time.addItem(tz)
        self.time.move(480, 17)
        self.time.resize(100, 30)
        self.tz_choice = self._db.time_zones[self._db.config.timezone_id]
        self.time.setCurrentText(self.tz_choice)
        self.time.activated[str].connect(self.time_format_connection)
        # здесь так же работа с бд. Я беру значения из time_zones,
        # в моем случае это utc и local, так как это работа с бд,
        # то это означает, что при закрытии программы все изменения сохраняться
        self.color = QComboBox(self)
        for name_color in self._bin_color.keys():
            self.color.addItem(name_color)
            if self._bin_color[name_color].id == self._db.config.pallette_id:
                self.current_pallette = name_color
        self.color.move(20, 17)
        self.color.resize(130, 30)
        self.color.activated[str].connect(self.color_selection)
        # Идентично тому, что и с time_zones, только тут я беру значения цветов из бд,
        # присваивая list цветов к ключу названий цветов(то, что будет отображаться в combobox'e),
        # то есть теперь у меня dict цветов, который так же храниться в бд
        # и будет сохраняться при закрытии программы
        self.bin_unix = []
        for col in range(4):
            self.bin_unix.append([])
            for row in range(8):
                normal_time_btn = QPushButton(self)
                normal_time_btn.move(65 * row + 40, 55 * col + 75)
                normal_time_btn.resize(60, 50)
                normal_time_btn.setEnabled(False) # нельзя нажимать
                normal_time_btn.setStyleSheet(
                    self._bin_color[self.current_pallette].colors[0])
                self.bin_unix[-1].append(normal_time_btn)
        # создаю в цикле 32 кнопки, по 4 кнопки в высоту и 8 кнопок в ширину.
        # так же задаю изначальный цвет

        self.hours = QLabel(self)
        self.hours.setText('hours')
        self.hours.move(10, 330)

        self.minutes = QLabel(self)
        self.minutes.setText('minutes')
        self.minutes.move(10, 380)

        self.seconds = QLabel(self)
        self.seconds.setText('seconds')
        self.seconds.move(10, 430)

        self.bin_hhmmss = []
        for col in range(3):
            self.bin_hhmmss.append([])
            for row in range(6):
                normal_time_btn = QPushButton(self)
                normal_time_btn.move(55 * row + 75, 50 * col + 320)
                normal_time_btn.resize(50, 45)
                normal_time_btn.setEnabled(False) # не нажать
                normal_time_btn.setStyleSheet(
                    self._bin_color[self.current_pallette].colors[0])
                self.bin_hhmmss[-1].append(normal_time_btn)
        # создаю 18 кнопок, 3 в высоту и 6 в длину.
        # так же задаю им цвет

        self.hh_label = QLabel(self)
        self.hh_label.setText('h')
        self.hh_label.move(410, 330)

        self.mm_label = QLabel(self)
        self.mm_label.setText('m')
        self.mm_label.move(407, 380)

        self.ss_label = QLabel(self)
        self.ss_label.setText('s')
        self.ss_label.move(410, 430)

        self.hhmmss = []
        for x in range(3):
            normal_time_btn = QLCDNumber(self)
            normal_time_btn.move(425, 50 * x + 325)
            normal_time_btn.resize(50, 33)
            self.hhmmss.append(normal_time_btn)
            # чтобы было понятно реальное время, создаю показывающий это QLCDNumber

        self.year = QLabel(self)
        self.year.setText('year')
        self.year.move(490, 330)

        self.month = QLabel(self)
        self.month.setText('month')
        self.month.move(490, 380)

        self.day = QLabel(self)
        self.day.setText('day')
        self.day.move(490, 430)

        self.yyyymmdd = []
        for x in range(3):
            normal_date_btn = QLCDNumber(self)
            normal_date_btn.move(540, 50 * x + 325)
            normal_date_btn.resize(50, 33)
            self.yyyymmdd.append(normal_date_btn)
            # чтобы была понятна реальная дата, создаю показывающий это QLCDNumber

        self.alarm_button = QPushButton('alarm', self)
        self.alarm_button.move(480, 475)
        self.alarm_button.resize(100, 30)
        self.alarm_button.clicked.connect(self.on_alarm_btn_clicked)
        # по кнопке обращаюсь к MyUnixAlarms, который открывает вторую форму, которая настраивает будильники

        self.second_timer = QTimer()
        self.second_timer.timeout.connect(self.on_second_timer)
        self.second_timer.start(1000)
        # добавляю QTimer, по сути обновляя каждую секунду форму,
        # чтобы время отсчитывалось по секундам

    def closeEvent(self, event):
        """
        при повторном запуске программы все изменения сохраняться
        """
        cfg = self._db.config
        cfg.set_pos(self.geometry().topLeft())
        cfg._pallette_id = self._db.pallettes[self.current_pallette].id
        tz_choice = 1
        for tz_id, tz in self._db.time_zones.items():
            if self.tz_choice == tz:
                tz_choice = tz_id
                break
        cfg._time_zone_id = tz_choice
        self._db.save_config(cfg)
        event.accept()
        

    format_hhmmss = ["hh", "mm", "ss"]
    format_yyyymmdd = ["yyyy", "MM", "dd"]

    def on_second_timer(self):
        """
        отображение времени
        """
        if self.tz_choice == 'UTC':
            now = QDateTime.currentDateTimeUtc() # нынешние дата и время в формате UTC
        elif self.tz_choice == 'local':
            now = QDateTime.currentDateTime()
            # нынешние дата и время, которые зависят от указанного местоположения на вашем компьютере
        for i in range(3):
            self.hhmmss[i].display(now.toString(MyUnixClock.format_hhmmss[i]))
            # вывожу на экран реальное время
            self.yyyymmdd[i].display(now.toString(
                MyUnixClock.format_yyyymmdd[i]))
            # вывожу на экран реальную дату
        now_time = now.time()
        self.display_bin(now_time.hour(), self.bin_hhmmss[0])
        self.display_bin(now_time.minute(), self.bin_hhmmss[1])
        self.display_bin(now_time.second(), self.bin_hhmmss[2])
        now_unix = now.currentSecsSinceEpoch()
        self.unix_time.display(now_unix) # вывожу на верхний QLCDNumber количество секунд с 1970 года
        self.display_unix_bin(now_unix, self.bin_unix)
        self.check_alarm_worked()

    def display_bin(self, val: int, where):
        """
        преобразую время в бинарный формат и в зависимости от того,
        0 или 1 мне встречаются окрашиваю левую нижнюю таблицу QPushButton'ов в два цвета
        """
        bin_val = bin(val)[2:]  # удаляю начальные 0b
        while len(bin_val) < 6:
            bin_val = '0' + bin_val
        for i in range(len(bin_val) - 1, -1, -1):
            where[i].setStyleSheet(
                self._bin_color[self.current_pallette].colors[int(bin_val[i])])
    
    def display_unix_bin(self, val: int, where):
        """
        преобразую количество секунд с 1970 года в бинарный вид и в зависимости от того,
        0 или 1 мне встречается окрашиваю таблицу QPushButton'ов по центру в два цвета
        """
        bin_val = bin(val)[2:]  # удаляю начальное 0b
        while len(bin_val) < 32:
            bin_val = '0' + bin_val
        for row in range(3, -1, -1):
            for col in range(7, -1, -1):
                where[row][col].setStyleSheet(
                    self._bin_color[self.current_pallette].colors[int(bin_val[row * 8 + col])])

    def color_selection(self, clr):
        """
        выбор цвета
        """
        self.current_pallette = clr

    def time_format_connection(self, frmt_tm):
        """
        выбор времени
        """
        self.tz_choice = frmt_tm

    def on_alarm_btn_clicked(self):
        """
        загрузка формы с обновленными данными
        """
        self._form.refresh()
        self._form.show()

    def check_alarm_worked(self):
        """
        в зависимости от того, выбран once/daily будильник, либо удаляется, либо сохраняется после проигрывания
        """
        now = QDateTime.currentDateTime()
        for alarm_time, alarm in self._db.sorted_alarms:
            if alarm_time > now:
                break
            self.signal_alarm(alarm)
            if alarm.type_id == 1:  # once
                self._db.delete_alarm(alarm.id) # удалить после единичного срабатывания
            else:  # daily
                self._db.update_alarm(alarm) # не удалять, а сохранять в бд, чтобы он сработал на следующий день
            self._form.close()


    def signal_alarm(self, alarm: Alarm):
        """
        при срабатывании будильника открывается форма и начинает звенеть будильник,
        так же, при закрытии формы будильник перестает звенеть
        """
        self._sound.play()
        self._msg_box.setText(f"Wake up @ {alarm.time}")
        self._msg_box.show()
        self._msg_box.buttonClicked.connect(self.stop_playing)
        

    def stop_playing(self):
        """
        прекращение звонка будильника
        """
        self._sound.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUnixClock()
    ex.show()
    sys.exit(app.exec())
