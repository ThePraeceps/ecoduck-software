import os, io, shutil
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

print("Loading payloads from /boot/")
# move payloads to payload directory
for payload_type in payloads:
	src=os.path.abspath(os.path.join("/boot/", payload_type))
	if(os.path.exists(src)):
		print("Moved: " + src)
		dest=os.path.abspath(os.path.join(payload_dir, payload_type))
		shutil.move(src, dest)

print("Payloads loaded, waiting for connection")
while(True):
	if(eco.is_hid_connected(1)):
		print("Gadget connected, getting OS")
		detected_os=eco.get_os()
		print("Found OS: " + detected_os)
		if(advanced):
			payload_ext=".py"
		else:
			payload_ext=".txt"

		if(os_payload_detection==True):
			print("Running payload detection")
			if(os=="windows"):
				payload = os.path.abspath(os.path.join(payload_dir, "win" + payload_ext))
			elif(os=="macos"):
				payload = os.path.abspath(os.path.join(payload_dir, "macos" + payload_ext))
			elif(os=="linux"):
				payload = os.path.abspath(os.path.join(payload_dir, "linux" + payload_ext))
			else:
				payload = os.path.abspath(os.path.join(payload_dir, default_script + payload_ext))

		if(not os.path.exists(payload)):
			print("Using default payload")
			payload = os.path.abspath(os.path.join(payload_dir, default_script + payload_ext))
		print("Payload selected: " + payload)
		if(os_gadget_detection):
			print("Running gadget detection")
			if(os=="n/a"):
				eco.set_gadget_mode(default_gadget)
			elif(os_gadget_detection):
				eco.set_gadget_mode(detected_os)
		else:
			eco.set_gadget_mode(default_gadget)

		print("Using gadget: " + eco.set_gadget_mode)
		if(os.path.exists(payload)):
			if(advanced):
				print("Running payload in advanced mode")
				import payload
			else:
				print("Running payload in basic mode")
				payload_reader = open("myfile.txt", "r", encoding="utf-8")
				eco.basic.interprator(payload_reader.readlines())
				payload_reader.close()
		if(infinite==False):
			print("Infinite payload running disabled, stopping")
			break
		if(wait_for_disconnect):
			print("Waiting for disconnect")
			eco.wait_for_keyboard_state(False)
			print("Disconnected!")
		eco.set_gadget_mode("simple")

