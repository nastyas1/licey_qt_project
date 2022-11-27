import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from db import *

class MyUnixAlarms(QWidget):
    def __init__(self, db: AlarmDb):
        super().__init__()
        self._db = db
        self._selected_alarm = 1
        self.initUI()


    def initUI(self):
        self.setWindowTitle('alarm')
        self.setGeometry(600, 600, 390, 331)

        self.all_alarms = QListWidget(self)
        self.all_alarms.resize(171, 311)
        self.all_alarms.move(10, 10)
        for alarm_id, alarm in self._db.alarms.items():
            item = QListWidgetItem()
            item.setData(1, alarm_id)
            item.setText(alarm.time)
            self.all_alarms.addItem(item)
        self.all_alarms.currentItemChanged.connect(self.on_all_alarms_changed)
        self._selected_alarm = 1

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

        self.save_btn = QPushButton('save', self)
        self.save_btn.resize(81, 41)
        self.save_btn.move(200, 280)

        self.delete_btn = QPushButton('delete', self)
        self.delete_btn.resize(81, 41)
        self.delete_btn.move(300, 280)
        
        self.display_alarm()

    def on_all_alarms_changed(self, current: QListWidgetItem, prevous: QListWidgetItem):
        self._selected_alarm = current.data(1)
        self.display_alarm()
        
    def display_alarm(self):
        alarm = self._db.alarms[self._selected_alarm]
        self.time_edit.setTime(alarm.time_as_tm)
        self.alarm_type_radios[self._selected_alarm - 1].setChecked(True)
        
        # con = sqlite3.connect('alarms.sqlite')
        # cur = con.cursor()
        # alarm_type_rowset = cur.execute("""SELECT alarm_type_id, alarm_type_name FROM alarm_type""").fetchall()
        # alarm_type_name = {}
        # for id_type in alarm_type_rowset:
        #     alarm_type_name.append(id_type[0])
        #     alarm_type_name[id_type[0]] = id_type[1]

        # for id_and_type in range(len(alarm_type_name)):
        #     self.chek_box = QCheckBox(f'{alarm_type_name[1]}', self)
            


        # count_alarms = []
        # count_alarms = cur.execute("""SELECT alarm_id FROM alarm""").fetchall()
        # budilniki = []
        # # count_budiln = []
        # con = sqlite3.connect('alarms.sqlite')
        # cur = con.cursor()
        # result_budilniki = cur.execute("""SELECT alarm_time FROM alarm""").fetchall()
        # count_budiln = cur.execute("""SELECT alarm_id FROM alarm""").fetchall()

        # window = QWidget(self)
        # table_time = QVBoxLayout(self)
        # for table in range(len(count_budiln)):
        #     self.window = QWidget(self)
        #     table_time.addWidget(QPushButton(f'{budilniki[table]}', self))
        #     table_time.moveToThread(self)
        #     self.window.setLayout(table_time)
        
        # for bb in result_budilniki:
        #     budilniki.append(bb[0])

        # for id_type in alarm_type_rowset:
        #     alarm_type_name.append(id_type[0])
        
        # for tt in range(3):    
        #     self.time = QLineEdit(self)
        #     self.time.setMaxLength(2)
        #     self.time.move(47 * tt + 215, 20)
        #     self.time.resize(40, 30)

        # for cc in range(2):
        #     self.colon = QLabel(self)
        #     self.colon.setText(':')
        #     self.colon.move(47 * cc + 237, 22)

        # for ww in range(2):
        #     self.count = QCheckBox(alarm_type_name[ww], self)
        #     self.count.move(200, ww * 30 + 130)
        #     self.count.resize(70, 30)
        
        # self.alarm_button = QPushButton('Set an alarm', self)
        # self.alarm_button.move(300, 165)
        # self.alarm_button.resize(120, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUnixAlarms(AlarmDb())
    ex.show()
    sys.exit(app.exec())
