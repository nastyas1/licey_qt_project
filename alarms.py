import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from db import *

class MyUnixAlarms(QDialog):
    def __init__(self, db: AlarmDb):
        super().__init__()
        self._db = db
        self.initUI()


    def initUI(self):
        self.setWindowTitle('alarm')
        self.setGeometry(600, 600, 390, 331)

        self.all_alarms = QListWidget(self)
        self.all_alarms.resize(171, 261)
        self.all_alarms.move(10, 10)
        self.all_alarms.currentItemChanged.connect(self.on_all_alarms_changed)

        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat('hh:mm:ss')
        self.time_edit.resize(181, 45)
        self.time_edit.move(200, 10)

        self.alarm_type_radios = []
        for alarm_type_id, alarm_type in self._db.alarm_type.items():
            al_rbtn = QRadioButton(self)
            al_rbtn.resize(161, 31)
            al_rbtn.move(200, 80 + 31 * (alarm_type_id - 1))
            al_rbtn.setText(alarm_type)
            self.alarm_type_radios.append(al_rbtn)
        # вывожу на экран Checkbox'ы с помощью обращения к бд, в моем случае это once, daily

        self.add_btn = QPushButton('add', self)
        self.add_btn.resize(81, 41)
        self.add_btn.move(10, 280)
        self.add_btn.clicked.connect(self.on_add_btn_clicked)

        self.del_btn = QPushButton('del', self)
        self.del_btn.resize(81, 41)
        self.del_btn.move(100, 280)
        self.del_btn.clicked.connect(self.on_del_btn_clicked)

        self.save_btn = QPushButton('save', self)
        self.save_btn.resize(191, 41)
        self.save_btn.move(190, 280)
        self.save_btn.clicked.connect(self.on_save_btn_clicked)
        
        self._selected_alarm = 0
        self.display_alarm_list()


    def on_all_alarms_changed(self, current: QListWidgetItem, previous: QListWidgetItem):
        if current is not None:
            self._selected_alarm = current.data(1)
            self.display_alarm()
    # если в бд существуют будильники, то я вывожу их на экран в QListWidget
        
    def display_alarm_list(self):
        self.all_alarms.clear()
        for alarm_id, alarm in self._db.alarms.items():
            if self._selected_alarm == 0:
                self._selected_alarm = alarm_id
            item = QListWidgetItem()
            item.setData(1, alarm_id)
            item.setText(alarm.time)
            self.all_alarms.addItem(item)
        self.display_alarm()
    # при нажатии на будильник в QTimeEdit'e будет показываться этот будильник
    
    def display_alarm(self):
        alarm = self._db.alarms[self._selected_alarm]
        self.time_edit.setTime(alarm.time_as_tm)
        self.alarm_type_radios[alarm.type_id - 1].setChecked(True)
    """
    передаю данные из бд, то есть указанные данные(once/daily).
    то есть при нажатии на будильник я так же буду видеть, 
    установлен этот будильник единично или каждый день
    """
        
    def on_del_btn_clicked(self):
        row = self.all_alarms.currentRow()
        self._db.delete_alarm(self._selected_alarm)
        self._selected_alarm = 0
        self.display_alarm_list()
        self.all_alarms.setCurrentRow(row if row < len(self._db.alarms) else len(self._db.alarms) - 1)
    """
    удаляю будильник при нажатии на кнопку del.
    если будильник был в конце, то мы переходим на будильник, стоящий выше,
    если в середине, то переходим на будильник, стоящий ниже
    """

    def on_add_btn_clicked(self):
        tm = self.time_edit.time().toString("hh:mm:ss")
        for i in range(len(self.alarm_type_radios)):
            if self.alarm_type_radios[i].isChecked():
                alarm_type_id = i
                break
        alarm_idx = self._db.add_alarm(Alarm(0, tm, alarm_type_id + 1))
        self.display_alarm_list()
        self.all_alarms.setCurrentRow(len(self._db.alarms) - 1)
    # добавляю будильник, он добавляется в самый конец
    
    def on_save_btn_clicked(self):
        row = self.all_alarms.currentRow()
        tm = self.time_edit.time().toString("hh:mm:ss")
        for i in range(len(self.alarm_type_radios)):
            if self.alarm_type_radios[i].isChecked():
                alarm_type_id = i + 1
                break
        self._db.update_alarm(Alarm(self._db.alarms[self._selected_alarm].id, tm, alarm_type_id))
        self.display_alarm_list()
        self.all_alarms.setCurrentRow(row)
    """
    сохраняю будильник в базу данных, при нажатии на кнопку save,
    то есть я могу изменять будильники и измененные будильники будут хранится в бд,
    а изначальные, которые я изменяла, будут удалены из бд
    """

    def refresh(self):
        self._selected_alarm = 0
        self.display_alarm_list()
        self.all_alarms.setCurrentRow(0)
    """
    чтобы при закрытии формы alarms и повторном открытии программа не заканчивалась
    я обнуляю прошлые данные
    """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUnixAlarms(AlarmDb())
    ex.show()
    sys.exit(app.exec())
