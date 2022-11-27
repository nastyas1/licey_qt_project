#    Проект "БИНАРНЫЕ ЧАСЫ"

## Введение

На главной форме показывается время UNIX, которое является количеством секунд с 1970 года, 
в UTC (Universal Coordinated Time) или местном часовом поясе. UNIX время представляет собой целое в 32 разряда,
что представлено на форме в виде 4 рядов по 8 кнопок. Часовой пояс определяется Combobox'oм с названием часовых поясов. Для понимания того, какое сейчас время в более привычных единицах в нижней части формы представлено время чч:мм:сс, как в бинарном, так и в десятичном виде. Так же представлена дата в формате гг:мм:дд.

С помощью кнопки Alarm  в нижнем правом углу, которая будет показывать форму с добавлением будильников, которые будут хранится в базе данных.

## База данных

База данных состоит из 5 связанных таблиц.

`pallette`

|name              |type|null    |constraints| comment                         |
|------------------|----|--------|-----------|---------------------------------|
| pallette_id      |int |not null|primary key|
| pallette_name    |text|not null|           |
| content          |text|not null|           |


`time_zone`

|name             |type|null    |constrains |
|-----------------|----|--------|-----------|
| time_zone_id    |int |not null|primary key|
| time_zone_name  |text|not null|           |

`config`

|name             |type|null    |constrains |
|-----------------|----|--------|-----------|
| config_id       |int |not null|primary key|
| last_update_time|int |not null|           |
| pos_x           |int |null    |           |
| pos_y           |int |null    |           |
| pallette_id     |int |not null|foreign key|
| time_zone_id    |int |not null|foreign key|

`alarm_type`

|name             |type|null    |constrains |
|-----------------|----|--------|-----------|
| alarm_type_id   |int |not null|primary key|
| alarm_type_name |text|not null|           |

`alarm`

|name             |type|null    |constrains |
|-----------------|----|--------|-----------|
| alarm_id        |int |not null|primary key|
| alarm_time      |int |not null|           |
| alarm_type_id   |int |not null|foreign key|




