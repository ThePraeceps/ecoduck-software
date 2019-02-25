import os, io
from ecoduck import eco

advanced=False
infinite=True

os_payload_detection=True
os_gadget_detection=True

wait_for_disconnect=True

default_gadget="simple"
default_script="default"

payload_dir = os.path.abspath("/usr/ecoduck/")
payloads=["win.txt", "macos.txt", "linux.txt", default_script + ".txt", "win.py", "macos.py", "linux.py", default_script + ".py"]

if(os.path.exists("/boot/ecoduck.conf")):
	# Parse options file
	# Advanced Mode
		# Infinite Loop
		# Default payload
		# OS detection
	advanced=True

# move payloads to payload directory
for payload in payloads:
	src=os.path.abspath(os.path.join("/boot/", payloads))
	if(os.path.exists(src)):
		dest=os.path.abspath(os.path.join(payload_dir, payload))
		os.rename(src, dest)


while(True)
	if(eco.is_hid_connected(1)):
		os=eco.get_os()
		if(advanced):
			payload_ext=".py"
		else:
			payload_ext=".txt"

		payload=""
		if(os_payload_detection==True):
			if(os=="windows"):
				payload = os.path.abspath(os.path.join(payload_dir, "win" + payload_ext))
			elif(os=="macos"):
				payload = os.path.abspath(os.path.join(payload_dir, "macos" + payload_ext))
			elif(os=="linux"):
				payload = os.path.abspath(os.path.join(payload_dir, "linux" + payload_ext))
			else:
				payload = os.path.abspath(os.path.join(payload_dir, default_script + payload_ext))

		if(not os.path.exists(payload)):
			payload = os.path.abspath(os.path.join(payload_dir, default_script + payload_ext))
		if
		if(os_gadget_detection):
			if(os=="n/a"):
				eco.set_gadget_mode(default_gadget)
			elif(os_gadget_detection):
				eco.set_gadget_mode(os)
		else:
			eco.set_gadget_mode(default_gadget)
		if(os.path.exists(payload)):
			if(advanced):
				import payload
			else:
				payload_reader = open("myfile.txt", "r", encoding="utf-8")
				eco.basic.interprator(payload_reader.readlines())
				payload_reader.close()
		if(infinite==False):
			break
		if(wait_for_disconnect):
			eco.wait_for_keyboard_state(False)
		eco.set_gadget_mode("simple")

