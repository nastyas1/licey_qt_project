CREATE TABLE alarm (
    alarm_id int PRIMARY KEY,
    hour int NOT NULL,
    mins int NOT NULL,
    sec int NOT NULL
);

CREATE TABLE binary_alarm (
    binary_id int PRIMARY KEY,
    hour int NOT NULL,
    mins int NOT NULL,
    sec int NOT NULL
);


