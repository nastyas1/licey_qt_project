CREATE TABLE palette(
    palette_id INT PRIMARY KEY,
    palette_name TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE time_zone(
    time_zone_id INT PRIMARY KEY,
    time_zone_name TEXT NOT NULL
);

CREATE TABLE config (
    config_id INT PRIMARY KEY,
    last_update_time INT NOT NULL,
    pos_x INT NULL,
    pos_y INT NOT,
    FOREIGN KEY (palette_id) 
      REFERENCES palette(palette_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION,
    FOREIGN KEY (time_zone_id) 
      REFERENCES time_zone(time_zone_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);
--сохранять при выходе

CREATE TABLE alarm_type(
    alarm_type_id INT PRIMARY KEY,
    alarm_type_name TEXT NOT NULL
);

CREATE TABLE alarm (
    alarm_id INT PRIMARY KEY,
    alarm_time INT NOT NULL,
    FOREIGN KEY (alarm_type_id) 
      REFERENCES alarm_type(alarm_type_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);

INSERT INTO palette(palette_id, palette_name, content) VALUES(1, "warm sun", ["background-color : darkgrey", "background-color : yellow"]);
INSERT INTO palette(palette_id, palette_name, content) VALUES(2, "decorative rose", ["background-color : darkgrey", "background-color : darkred"]);
INSERT INTO palette(palette_id, palette_name, content) VALUES(3, "summer grass", ["background-color : darkgrey", "background-color : darkgreen"]);
INSERT INTO palette(palette_id, palette_name, content) VALUES(4, "winter morning", ["background-color : darkgrey", "background-color : darkblue"]);

INSERT INTO time_zone(time_zone_id, time_zone_name) VALUES(1, 'UTC');
INSERT INTO time_zone(time_zone_id, time_zone_name) VALUES(2, 'local');

INSERT INTO alarm_type(alarm_type_id, alarm_type_name) VALUES(1, 'once');
INSERT INTO alarm_type(alarm_type_id, alarm_type_name) VALUES(2, 'daily');
