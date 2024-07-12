# 目的：创建一个提醒应用程序，在特定的时间提醒你做一些事情(桌面通知)。

# 提示：Time模块可以用来跟踪提醒时间，toastnotifier库可以用来显示桌面通知。

# 安装：win10toast

from pkg_resources import get_distribution

from win10toast import ToastNotifier
import time

def toastWin():
    toaster = ToastNotifier()
    try:
        print("Title of reminder")
        header = input()
        print("Message of reminder")
        text = input()
        print("In how many minutes?")
        time_min = input()
        time_min = float(time_min)
    except:
        header = input("Title of reminder\n")
        text = input("Message of remindar\n")
        time_min = float(input("In how many minutes?\n"))
    time_min = time_min * 30
    print("Setting up reminder..")
    time.sleep(2)
    print("all set!")
    time.sleep(time_min)
    toaster.show_toast(f"{header}",
                       f"{text}",
                       None,
                       duration=10,
                       threaded=True)
    while toaster.notification_active(): time.sleep(0.005)


if __name__ == '__main__':
    toastWin()
