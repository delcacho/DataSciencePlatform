import sdnotify, time

n = sdnotify.SystemdNotifier()
print("Gonna start")
time.sleep(2)
print("Started!")

n.notify("READY=1")
i=0
while True:
    print(i)
    time.sleep(1)
    n.notify("WATCHDOG=1")
    i+=1
