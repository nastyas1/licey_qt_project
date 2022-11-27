import sqlite3
from typing import Dict, Union, Tuple
from PyQt5.QtCore import *


class Config:
    def __init__(self, last_update_time=0, pos_x=0, pos_y=0, pallette_id=1, time_zone_id=1) -> None:
        self._id = 1
        self._last_update_time: int = last_update_time
        self._pos_x: int = pos_x
        self._pos_y: int = pos_y
        self._pallette_id: int = pallette_id
        self._time_zone_id: int = time_zone_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def last_update_time(self):
        return self._last_update_time

    @property
    def last_update_time_as_dt(self):
        return QDateTime.fromSecsSinceEpoch(self._last_update_time)

    def set_last_update_time(self, when: QDateTime):
        self._last_update_time = when.toSecsSinceEpoch()

    @property
    def pos(self) -> Tuple[int, int]:
        return (self._pos_x, self._pos_y)

    def set_pos(self, pos):
        self._pos_x = pos.x()
        self._pos_y = pos.y()

    @property
    def pallette_id(self) -> int:
        return self._pallette_id

    @property
    def timezone_id(self) -> int:
        return self._time_zone_id


class Alarm:
    def __init__(self, id = 0, time:str = "00:00:00", type_id = 1) -> None:
        self._id: int = id
        self._time: int = time
        self._type_id: int = type_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def time(self) -> str:
        return self._time
    
    @property
    def time_as_tm(self) -> str:
        return QTime.fromString(self._time, "hh:mm:ss")

    @property
    def time_as_dt(self) -> QDateTime:
        tm: QTime = self.time_as_tm
        now = QDateTime.currentDateTime()
        if now.time() > tm:
            return QDateTime(now.date().addDays(1)).addMSecs(tm.msecsSinceStartOfDay())
        else:
            return QDateTime(now.date()).addMSecs(tm.msecsSinceStartOfDay())

    @property
    def type_id(self) -> int:
        return self._type_id


class Pallette:
    def __init__(self, id=0, name="", true_color="", false_color="") -> None:
        self._id = id
        self._name = name
        self._true_color = true_color
        self._false_color = false_color

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self):
        return self._id

    @property
    def true_color(self):
        return self._true_color

    @property
    def false_color(self):
        return self._false_color

    @property
    def colors(self):
        return [self._false_color, self._true_color]


class AlarmDb:
    def __init__(self, db_path='alarms.sqlite') -> None:
        self._con = sqlite3.connect(db_path)
        self._alarm_type: Dict[int, str] = {}
        self._alarms: Dict[int, Alarm] = {}
        self._pallettes: Dict[str, Pallette] = {}
        self._time_zones: Dict[int, str] = {}
        self._config: Config = Config()
        self.load_data()
    
    def load_data(self):
        """
        s,fvg;ldfm;mg;dfnmbm"
        """
        # load alarm types
        cur = self._con.cursor()
        alarm_type_rowset = cur.execute("SELECT alarm_type_id, alarm_type_name FROM alarm_type").fetchall()
        for alarm_type in alarm_type_rowset:
            self._alarm_type[alarm_type[0]] = alarm_type[1]

        # load alarms
        cur = self._con.cursor()
        alarm_rowset = cur.execute("SELECT alarm_id, alarm_time, alarm_type_id FROM alarm").fetchall()
        for alarm in alarm_rowset:
            self._alarms[alarm[0]] = Alarm(alarm[0], alarm[1], alarm[2])

        # load alarms
        cur = self._con.cursor()
        pallette_rowset = cur.execute("SELECT pallette_id, pallette_name, true_color, false_color FROM pallette").fetchall()
        for pallette in pallette_rowset:
            self._pallettes[pallette[1]] = Pallette(pallette[0], pallette[1], pallette[2], pallette[3])

        # load time zones
        cur = self._con.cursor()
        tz_rowset = cur.execute("SELECT time_zone_id, time_zone_name FROM time_zone").fetchall()
        for tz in tz_rowset:
            self._time_zones[tz[0]] = tz[1]

        # load config
        cur = self._con.cursor()
        cfg_rowset = cur.execute("SELECT config_id, last_update_time, pos_x, pos_y, pallette_id, time_zone_id FROM config WHERE config_id=1").fetchall()
        for cfg in cfg_rowset:
            self._config = Config(cfg[1], cfg[2], cfg[3], cfg[4], cfg[5])

    @property
    def alarm_type(self) -> Dict[int, str]:
        return self._alarm_type

    @property
    def alarms(self) -> Dict[int, Alarm]:
        return self._alarms

    @property
    def pallettes(self) -> Dict[int, Pallette]:
        return self._pallettes

    @property
    def time_zones(self) -> Dict[int, str]:
        return self._time_zones

    @property
    def config(self) -> Config:
        return self._config

    def save_config(self, cfg: Config):
        # save config
        cfg.set_last_update_time(QDateTime.currentDateTime())
        cmd = f"UPDATE config SET last_update_time={cfg.last_update_time}, pos_x={cfg.pos[0]}, pos_y={cfg.pos[1]}, pallette_id={cfg.pallette_id}, time_zone_id={cfg.timezone_id} WHERE config_id=1"
        cur = self._con.execute(cmd)
        self._con.commit()

def test_db():
    al = [Alarm(1, "01:01:01", 1), Alarm(1, "21:34:56", 2)]
    print("test alarm:", ",".join([f"{a.id}={a.time_as_dt}({a.time})" for a in al]))

    db = AlarmDb()
    print("alarm types:", ",".join([f"{id}={name}" for id, name in db.alarm_type.items()]))
    print("pallettes:", ",".join([f"{name}={{{pal.id},{pal.colors}}}" for name, pal in db.pallettes.items()]))
    print("time_zones:", ",".join([f"{id}={name}" for id, name in db.time_zones.items()]))
    print("alarms:", ",".join([f"{id}={{{al.time_as_dt},{al.type_id}}}" for id, al in db.alarms.items()]))
    print(f"config: {db.config.id}={{{db.config.last_update_time_as_dt},{db.config.pos},pallette:{db.config.pallette_id},timezone:{db.config._time_zone_id}}}")
    
    cfg = Config()
    cfg._pallette_id = 2
    db.save_config(cfg)
    db.load_data()
    print(f"new config: {db.config.id}={{{db.config.last_update_time_as_dt},{db.config.pos},pallette:{db.config.pallette_id},timezone:{db.config._time_zone_id}}}")

if __name__ == "__main__": 
    test_db()