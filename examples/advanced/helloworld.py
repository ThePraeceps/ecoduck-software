import ecoduck.py
from time import sleep

eco.press("LGUI+R")
sleep(1)
eco.type("cmd")
eco.press("ENTER")
sleep(1)
for i in range(3):
	eco.type("echo Hello World")
	eco.press("ENTER")
eco.type("echo Done!")