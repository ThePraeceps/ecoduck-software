import os, io, shutil, importlib.util
from ecoduck import eco
from time import sleep

advanced=False
infinite=True

os_payload_detection=True
os_gadget_detection=True

wait_for_disconnect=True

default_gadget="simple"
default_script="default"

payload_dir = os.path.abspath("/usr/ecoduck/")
payloads=["win.txt", "macos.txt", "linux.txt", default_script + ".txt", "win.py", "macos.py", "linux.py", default_script + ".py"]

conf_file=os.path.abspath("/boot/ecoduck.conf")

def get_state(line):
	state=line.split("=")[1]
	if "true" in state.lower():
		return True
	return False

if(os.path.exists(conf_file)):
	conf_reader = open(conf_file, "r", encoding="utf-8")
	conf_lines=conf_reader.readlines()
	conf_reader.close()
	for line in conf_lines:
		line=line.rstrip("\r\n")
		if "#" not in line[:1] or not(len(line) == 0) :
			if "enabled" in line[:7]:
				enabled=get_state(line)
				if not enabled:
					exit()
			if "advanced" in line[:8]:
				advanced=get_state(line)
				print("Set advanced to: " + str(advanced))
			elif "infinite" in line[:8]:
				infinite=get_state(line)
				print("Set infinite to: " + str(infinite))
			elif "os_payload_detection" in line[:20]:
				os_payload_detection=get_state(line)
				print("Set os_payload_detection to: " + str(os_payload_detection))
			elif "os_gadget_detection" in line[:19]:
				os_gadget_detection=get_state(line)
				print("Set os_gadget_detection to: " + str(os_gadget_detection))
			elif "wait_for_disconnect" in line[:19]:
				wait_for_disconnect=get_state(line)
				print("Set wait_for_disconnect to: " + str(wait_for_disconnect))
			elif "default_gadget" in line[:14]:
				default_gadget=line.split("=")[1]
				print("Set default_gadget to: " + str(default_gadget))
			elif "default_script" in line[:14]:
				default_script=line.split("=")[1]
				print("Set default_script to: " + str(default_script))

print("Loading payloads from /boot/")
# move payloads to payload directory
for payload_type in payloads:
	src=os.path.abspath(os.path.join("/boot/", payload_type))
	if(os.path.exists(src)):
		print("Moved: " + src)
		dest=os.path.abspath(os.path.join(payload_dir, payload_type))
		shutil.move(src, dest)

eco.set_gadget_mode(default_gadget)
print("Payloads loaded, waiting for connection")
while(True):
	if(eco.is_hid_connected(1)):
		print("Gadget connected, getting OS")
		detected_os=eco.get_os()
		print("Found OS: " + detected_os)
		if(advanced):
			print("Selecting advanced payload")
			payload_ext=".py"
		else:
			print("Selecting basic payload")
			payload_ext=".txt"
		payload=""
		if(os_payload_detection==True):
			print("Running payload detection")
			if(detected_os=="windows"):
				print("Using windows payload")
				payload = os.path.abspath(os.path.join(payload_dir, "win" + payload_ext))
			elif(detected_os=="macos"):
				print("Using macos payload")
				payload = os.path.abspath(os.path.join(payload_dir, "macos" + payload_ext))
			elif(detected_os=="linux"):
				print("Using linux payload")
				payload = os.path.abspath(os.path.join(payload_dir, "linux" + payload_ext))
			else:
				print("Using default payload")
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
			

		print("Using gadget: " + eco.get_gadget_mode())
		sleep(2)
		if(os.path.exists(payload)):
			sleep(2)
			if(advanced):
				print("Running payload in advanced mode")
				spec = importlib.util.spec_from_file_location("payload", payload)
				foo = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(foo)
			else:
				print("Running payload in basic mode")
				payload_reader = open(payload, "r", encoding="utf-8")
				eco.basic.interpreter(payload_reader.readlines())
				payload_reader.close()
		if(infinite==False):
			print("Infinite payload running disabled, stopping")
			break
		if(wait_for_disconnect):
			print("Waiting for disconnect")
			print("Path: " + eco.path)
			eco.wait_for_keyboard_state(False)
			print("Disconnected!")
		eco.set_gadget_mode("simple")

