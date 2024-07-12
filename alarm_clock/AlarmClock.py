from datetime import datetime
from playsound import playsound


def alarmClock():
    alarm_time = input("Enter the time of alarm to be set:HH:MM:SS\n")
    alarm_hour = alarm_time[0:2]
    alarm_minute = alarm_time[3:5]
    alarm_seconds = alarm_time[6:8]

    alarm_period = alarm_time[9:11].upper()
    print("Setting up alarm..")

    while True:
        now = datetime.now()
        current_hour = now.strftime("%I")
        current_minute = now.strftime("%M")
        current_seconds = now.strftime("%S")
        current_period = now.strftime("%p")

        print(alarm_hour + ":" + alarm_minute + ":" + alarm_seconds + ":" + alarm_period)
        print(current_hour + ":" + current_minute + ":" + current_seconds + ":" + current_period)
        if alarm_period == current_period and alarm_hour == current_hour and alarm_minute == current_minute \
                and alarm_seconds == current_seconds:
            print("Wake Up!")
            playsound('/人人车.mp3')
            break


if __name__ == "__main__":
    #playsound('/人人车.mp3')
    alarmClock()
