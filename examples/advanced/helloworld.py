from ecoduck import eco
from time import sleep
eco.press("ESC")
sleep(1)
eco.press("LGUI+d")
sleep(1)
eco.press("LGUI+r")
sleep(1)
eco.type("cmd")
eco.press("ENTER")
sleep(1)
for i in range(3):
        eco.type("echo Hello World")
        eco.press("ENTER")
eco.type("echo Done!")
eco.press("ENTER")