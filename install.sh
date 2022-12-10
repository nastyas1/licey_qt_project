pyinstaller --add-binary alarms.sqlite:. --add-binary  sound/Alarm-ringtone.wav:sound unix_time.py

echo ----------------------------
echo run dist/unix_time/unit_time
echo ----------------------------
