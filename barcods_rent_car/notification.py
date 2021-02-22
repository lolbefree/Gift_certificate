from win10toast import ToastNotifier


def my_notifier(x):
    toaster = ToastNotifier()
    toaster.show_toast(f"{x}", f"{x}",
                       threaded=True, icon_path=None, duration=5)
