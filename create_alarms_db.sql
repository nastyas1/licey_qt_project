DROP TABLE IF EXISTS pallette;
CREATE TABLE pallette(
    pallette_id INT PRIMARY KEY,
    pallette_name TEXT NOT NULL,
    true_color TEXT NOT NULL,
    false_color TEXT NOT NULL
);

DROP TABLE IF EXISTS time_zone;
CREATE TABLE time_zone(
    time_zone_id INT PRIMARY KEY,
    time_zone_name TEXT NOT NULL
);

DROP TABLE IF EXISTS config;
CREATE TABLE config(
    config_id INT PRIMARY KEY,
    last_update_time INT NOT NULL,
    pos_x INT NULL,
    pos_y INT NULL,
    pallette_id INT NOT NULL,
    time_zone_id INT NOT NULL,
    FOREIGN KEY (pallette_id) 
      REFERENCES pallette(pallette_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION,
    FOREIGN KEY (time_zone_id) 
      REFERENCES time_zone(time_zone_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);
--сохранять при выходе

DROP TABLE IF EXISTS alarm_type;
CREATE TABLE alarm_type(
    alarm_type_id INT PRIMARY KEY,
    alarm_type_name TEXT NOT NULL
);

DROP TABLE IF EXISTS alarm;
CREATE TABLE alarm (
    alarm_id INT PRIMARY KEY,
    alarm_time TEXT NOT NULL,
    alarm_type_id INT NOT NULL,
    FOREIGN KEY (alarm_type_id) 
      REFERENCES alarm_type(alarm_type_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);

INSERT INTO pallette(pallette_id, pallette_name, false_color, true_color) VALUES(1, "warm sun", "background-color : darkgrey", "background-color : yellow");
INSERT INTO pallette(pallette_id, pallette_name, false_color, true_color) VALUES(2, "decorative rose", "background-color : darkgrey", "background-color : darkred");
INSERT INTO pallette(pallette_id, pallette_name, false_color, true_color) VALUES(3, "summer grass", "background-color : darkgrey", "background-color : darkgreen");
INSERT INTO pallette(pallette_id, pallette_name, false_color, true_color) VALUES(4, "winter morning", "background-color : darkgrey", "background-color : darkblue");

INSERT INTO time_zone(time_zone_id, time_zone_name) VALUES(1, 'UTC');
INSERT INTO time_zone(time_zone_id, time_zone_name) VALUES(2, 'local');

INSERT INTO alarm_type(alarm_type_id, alarm_type_name) VALUES(1, 'once');
INSERT INTO alarm_type(alarm_type_id, alarm_type_name) VALUES(2, 'daily');

INSERT INTO alarm(alarm_id, alarm_time, alarm_type_id) VALUES(1, '06:30:00', 1);
INSERT INTO alarm(alarm_id, alarm_time, alarm_type_id) VALUES(2, '08:00:00', 2);
