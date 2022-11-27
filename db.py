import sqlite3
from typing import Dict, Union, Tuple
from PyQt5.QtCore import *


class Config:
    """
    возвращает из базы данных переменные, указанные в init в нужном формате
    """
    def __init__(self, last_update_time=0, pos_x=0, pos_y=0, pallette_id=1, time_zone_id=1) -> None:
        self._id = 1
        self._last_update_time: int = last_update_time
        self._pos_x: int = pos_x
        self._pos_y: int = pos_y
        self._pallette_id: int = pallette_id
        self._time_zone_id: int = time_zone_id

    @property # использую property, чтобы потом не писать скобки
    def id(self) -> int:
        """
        возвращает id
        """
        return self._id

    @property
    def last_update_time(self):
        """
        возвращает последнее добавленное время
        """
        return self._last_update_time

    @property
    def last_update_time_as_dt(self):
        """
        обновляю дату и время
        """
        return QDateTime.fromSecsSinceEpoch(self._last_update_time)


    def set_last_update_time(self, when: QDateTime):
        """
        перевод в unix time
        """
        self._last_update_time = when.toSecsSinceEpoch()

    @property
    def pos(self) -> Tuple[int, int]:
        """
        сохранение позиции формы в бд
        """
        return (self._pos_x, self._pos_y)

    def set_pos(self, pos):
        """
        позиция формы
        """
        self._pos_x = pos.x()
        self._pos_y = pos.y()

    @property
    def pallette_id(self) -> int:
        """
        возвращает id палитры
        """
        return self._pallette_id

    @property
    def timezone_id(self) -> int:
        """
        возвращает id time_zone, то есть id utc/local
        """
        return self._time_zone_id


class Alarm:
    """
    возвращает из базы данных переменные, указанные в init в нужном формате
    """
    def __init__(self, id = 0, time:str = "00:00:00", type_id = 1) -> None:
        self._id: int = id
        self._time: int = time
        self._type_id: int = type_id

    @property
    def id(self) -> int:
        """
        возвращает id будильника
        """
        return self._id

    @property
    def time(self) -> str:
        """
        возвращает время будильника как строку
        """
        return self._time
    
    @property
    def time_as_tm(self) -> str:
        """
        перевод времени QTime из формата "hh:mm:ss"
        """
        return QTime.fromString(self._time, "hh:mm:ss")

    @property
    def time_as_dt(self) -> QDateTime:
        """
        в зависимости от текущего времени, ставлю я будильник на завтра или же на сегодня
        я возвращаю время и дату будильника
        """
        tm: QTime = self.time_as_tm
        now = QDateTime.currentDateTime()
        if now.time() > tm: # если нынешнее время позже поставленного будильника я добавляю день
            return QDateTime(now.date().addDays(1)).addMSecs(tm.msecsSinceStartOfDay())
        else: # если нет, то рассчитываю колво милисекунд до будильника
            return QDateTime(now.date()).addMSecs(tm.msecsSinceStartOfDay())


    @property
    def type_id(self) -> int:
        """
        возвращает id типа указанного времени в формате int
        """
        return self._type_id


class Pallette:
    """
    возвращает из базы данных переменные, указанные в init в нужном формате
    """
    def __init__(self, id=0, name="", true_color="", false_color="") -> None:
        self._id = id
        self._name = name
        self._true_color = true_color
        self._false_color = false_color

    @property
    def id(self) -> int:
        """
        возвращает id цвета в формате int
        """
        return self._id

    @property
    def name(self):
        """
        возвращает название цвета
        """
        return self._id

    @property
    def true_color(self):
        """
        возвращает цвет, который окрашивает кнопки, которые инициализируются как "1"
        """
        return self._true_color

    @property
    def false_color(self):
        """
        возвращает цвет, который окрашивает кнопки, которые инициализируются как "0"
        """
        return self._false_color

    @property
    def colors(self):
        """
        возвращает list цветов
        """
        return [self._false_color, self._true_color]


class AlarmDb:
    """
    возвращает из базы данных переменные, указанные в init в нужном формате,
    так же тут я указываю изначальную базу данных, config хранится всегда с 1й id=1
    """
    def __init__(self, db_path='alarms.sqlite') -> None:
        self._con = sqlite3.connect(db_path)
        self._alarm_type: Dict[int, str] = {}
        self._alarms: Dict[int, Alarm] = {}
        self._pallettes: Dict[str, Pallette] = {}
        self._time_zones: Dict[int, str] = {}
        self._config: Config = Config()
        self.load_data()
    
    def load_alarms(self):
        """
        загружаю из бд все, что понадобилось для будильника
        """
        self._alarms.clear()
        cur = self._con.cursor()
        alarm_rowset = cur.execute("SELECT alarm_id, alarm_time, alarm_type_id FROM alarm").fetchall()
        for alarm in alarm_rowset:
            self._alarms[alarm[0]] = Alarm(alarm[0], alarm[1], alarm[2])
        self._sorted_alarms = [(v.time_as_dt, v) for v in self._alarms.values()]
        self._sorted_alarms.sort(key=lambda a: a[0])

    
    def load_data(self):
        """
        загрузка различных значений из бд
        """
        self._alarm_type.clear()
        self._pallettes.clear()
        self._time_zones.clear()

        # загружаю из бд тип будильника, то есть once/daily
        cur = self._con.cursor()
        alarm_type_rowset = cur.execute("SELECT alarm_type_id, alarm_type_name FROM alarm_type").fetchall()
        for alarm_type in alarm_type_rowset:
            self._alarm_type[alarm_type[0]] = alarm_type[1]

        # загружаю из бд палитру
        cur = self._con.cursor()
        pallette_rowset = cur.execute("SELECT pallette_id, pallette_name, true_color, false_color FROM pallette").fetchall()
        for pallette in pallette_rowset:
            self._pallettes[pallette[1]] = Pallette(pallette[0], pallette[1], pallette[2], pallette[3])

        # загружаю из бд координированное время, то есть utc/local
        cur = self._con.cursor()
        tz_rowset = cur.execute("SELECT time_zone_id, time_zone_name FROM time_zone").fetchall()
        for tz in tz_rowset:
            self._time_zones[tz[0]] = tz[1]

        # загружаю из бд все изменения, которые были при открытии программы
        cur = self._con.cursor()
        cfg_rowset = cur.execute("SELECT config_id, last_update_time, pos_x, pos_y, pallette_id, time_zone_id FROM config WHERE config_id=1").fetchall()
        for cfg in cfg_rowset:
            self._config = Config(cfg[1], cfg[2], cfg[3], cfg[4], cfg[5])

        self.load_alarms()

    @property
    def alarm_type(self) -> Dict[int, str]:
        """
        возвращает библиотеку с индексом и типом будильника(once/daily)
        """
        return self._alarm_type

    @property
    def alarms(self) -> Dict[int, Alarm]:
        """
        возвращает библиотеку с индексом и временем будильника
        """
        return self._alarms

    @property
    def pallettes(self) -> Dict[int, Pallette]:
        """
        возвращает библиотеку с индексом и временем будильника
        """
        return self._pallettes

    @property
    def time_zones(self) -> Dict[int, str]:
        """
        возвращает библиотеку с индексом и типом времени(utc/local)
        """
        return self._time_zones

    @property
    def config(self) -> Config:
        """
        возвращает объект класса Config, который хранится в одном экземпляре с id=1
        """
        return self._config

    def save_config(self, cfg: Config):
        """
        сохраняю все изменения
        """
        cfg.set_last_update_time(QDateTime.currentDateTime())
        cmd = f"UPDATE config SET last_update_time={cfg.last_update_time}, pos_x={cfg.pos[0]}, pos_y={cfg.pos[1]}, pallette_id={cfg.pallette_id}, time_zone_id={cfg.timezone_id} WHERE config_id=1"
        cur = self._con.execute(cmd)
        self._con.commit()

    def delete_alarm(self, id: int):
        """
        удаляю будильник из бд
        """
        cmd = f"DELETE FROM alarm WHERE alarm_id={id}"
        cur = self._con.execute(cmd)
        self._con.commit()
        self.load_alarms()

    def add_alarm(self, alarm: Alarm):
        """
        добавляю будильник в бд
        """
        cmd_max_id = "SELECT MAX(alarm_id) FROM alarm"
        cur = self._con.execute(cmd_max_id).fetchall()
        max_id = cur[0][0] + 1
        cmd = f"INSERT INTO alarm(alarm_id, alarm_time, alarm_type_id) VALUES({max_id},'{alarm.time}',{alarm.type_id})"
        cur = self._con.execute(cmd)
        self._con.commit()
        self.load_alarms()
        return max_id

    def update_alarm(self, alarm: Alarm):
        """
        изменяю уже существующий будильник на тот, который я изменила
        """
        cmd = f"UPDATE alarm SET alarm_time='{alarm.time}', alarm_type_id={alarm.type_id} WHERE alarm_id={alarm.id}"
        cur = self._con.execute(cmd)
        self._con.commit()
        self.load_alarms()

    @property
    def sorted_alarms(self) -> list[Alarm]:
        """
        возвращает сортированные по времени список из пар(время срабатывания с датой, будильник)
        """
        return self._sorted_alarms



def test_db():
    def print_alarms():
        print("alarms:", ",".join([f"{id}={{{al.time_as_dt},{al.type_id}}}" for id, al in db.alarms.items()]))

    al = [Alarm(1, "01:01:01", 1), Alarm(1, "21:34:56", 2)]
    print("test alarm:", ",".join([f"{a.id}={a.time_as_dt}({a.time})" for a in al]))

    db = AlarmDb()
    print("alarm types:", ",".join([f"{id}={name}" for id, name in db.alarm_type.items()]))
    print("pallettes:", ",".join([f"{name}={{{pal.id},{pal.colors}}}" for name, pal in db.pallettes.items()]))
    print("time_zones:", ",".join([f"{id}={name}" for id, name in db.time_zones.items()]))
    print(f"config: {db.config.id}={{{db.config.last_update_time_as_dt},{db.config.pos},pallette:{db.config.pallette_id},timezone:{db.config._time_zone_id}}}")
    print_alarms()    

    cfg = Config()
    cfg._pallette_id = 2
    db.save_config(cfg)
    db.load_data()
    print_alarms()    

    a1_id = db.add_alarm(Alarm(0, "12:23:45", 1))
    a2_id = db.add_alarm(Alarm(0, "21:32:54", 2))
    print(len(db.alarms)) # должно быть 4
    print_alarms()    

    db.delete_alarm(a1_id)
    print(len(db.alarms)) # должно быть 3
    print_alarms()    

    db.update_alarm(Alarm(a2_id, "01:02:03", 1))
    print(len(db.alarms)) # должно быть 3
    print_alarms()    

    db.delete_alarm(a2_id)
    print(len(db.alarms)) # должно быть 2
    print_alarms()    

if __name__ == "__main__": 
    test_db()
