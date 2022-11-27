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
| pallette_id      |int |not null|primary key|id палитры                       |
| pallette_name    |text|not null|           |название списка цветов           |
| content          |text|not null|           |список цветов                    |


`time_zone`

|name             |type|null    |constrains | comment                         |
|-----------------|----|--------|-----------|---------------------------------|
| time_zone_id    |int |not null|primary key|id координированного времени     |
| time_zone_name  |text|not null|           |название коорд. времени          |

`config`

|name             |type|null    |constrains | comment                         |
|-----------------|----|--------|-----------|---------------------------------|
| config_id       |int |not null|primary key|id config                        |
| last_update_time|int |not null|           |последнее сохраненное изменение  |
| pos_x           |int |null    |           |позиция на экране(х)             |
| pos_y           |int |null    |           |позиция на экране(у)             |
| pallette_id     |int |not null|foreign key|id палитры                       |
| time_zone_id    |int |not null|foreign key|id координированного времени     |

`alarm_type`

|name             |type|null    |constrains | comment                            |
|-----------------|----|--------|-----------|------------------------------------|
| alarm_type_id   |int |not null|primary key|id типа будильника                  |
| alarm_type_name |text|not null|           |название типа будильника(once/daily)|

`alarm`

|name             |type|null    |constrains | comment                         |
|-----------------|----|--------|-----------|---------------------------------|
| alarm_id        |int |not null|primary key|id будильника                    |
| alarm_time      |int |not null|           |время будильника                 |
| alarm_type_id   |int |not null|foreign key|id типа будильника               |




