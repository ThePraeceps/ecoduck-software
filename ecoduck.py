#!/usr/bin/env python3

import os,signal,io,array,platform,inspect
from subprocess import Popen, PIPE, check_output, call
from math import isnan
from time import sleep

class eco:
	debug=0
	onPi=True
	gadget_mode="null"
	path=""
	## LOOKUP TABLE START ##	
	LookUpScanCode = {
		"a":"\x04",
		"b":"\x05",
		"c":"\x06",
		"d":"\x07",
		"e":"\x08",
		"f":"\x09",
		"g":"\x0a",
		"h":"\x0b",
		"i":"\x0c",
		"j":"\x0d",
		"k":"\x0e",
		"l":"\x0f",
		"m":"\x10",
		"n":"\x11",
		"o":"\x12",
		"p":"\x13",
		"q":"\x14",
		"r":"\x15",
		"s":"\x16",
		"t":"\x17",
		"u":"\x18",
		"v":"\x19",
		"w":"\x1a",
		"x":"\x1b",
		"y":"\x1c",
		"z":"\x1d",

		"f1":"\x3a",
		"f2":"\x3b",
		"f3":"\x3c",
		"f4":"\x3d",
		"f5":"\x3e",
		"f6":"\x3f",
		"f7":"\x40",
		"f8":"\x41",
		"f9":"\x42",
		"f10":"\x43",
		"f11":"\x44",
		"f12":"\x45",

		"1":"\x1e",
		"2":"\x1f",
		"3":"\x20",
		"4":"\x21",
		"5":"\x22",
		"6":"\x23",
		"7":"\x24",
		"8":"\x25",
		"9":"\x26",
		"0":"\x27",
		"enter":"\x28",
		"esc":"\x29",
		"backspace":"\x2a",
		"tab":"\x2b",
		"space":"\x2c",
		" ":"\x2c",
		"-":"\x2d",
		"=":"\x2e",
		"[":"\x2f",
		"]":"\x30",
		"\\":"\x31",
		"#":"\x32",
		";":"\x33",
		"'":"\x34",
		"`":"\x35",
		",":"\x36",
		".":"\x37",
		"/":"\x38",
		"caps_lock":"\x39",
		"print_screen":"\x46",
		"scroll_lock":"\x47",
		"pause":"\x48",
		"insert":"\x49",
		"home":"\x4a",
		"page_up":"\x4b",
		"delete":"\x4c",
		"end":"\x4d",
		"page_down":"\x4e",
		"right_arrow":"\x4f",
		"left_arrow":"\x50",
		"down_arrow":"\x51",
		"up_arrow":"\x52",
		"keypad_numlock":"\x53",
		"keypad_/":"\x54",
		"keypad_*":"\x55",
		"keypad_-":"\x56",
		"keypad_+":"\x57",
		"keypad_enter":"\x58",
		"keypad_1":"\x59",
		"keypad_2":"\x5a",
		"keypad_3":"\x5b",
		"keypad_4":"\x5c",
		"keypad_5":"\x5d",
		"keypad_6":"\x5e",
		"keypad_7":"\x5f",
		"keypad_8":"\x60",
		"keypad_8":"\x61",
		"keypad_0":"\x62",
		"keypad_.":"\x63"
	}

	LookUpShiftLayer = {

		"A":"a",
		"B":"b",
		"C":"c",
		"D":"d",
		"E":"e",
		"F":"f",
		"G":"g",
		"H":"h",
		"I":"i",
		"J":"j",
		"K":"k",
		"L":"l",
		"M":"m",
		"N":"n",
		"O":"o",
		"P":"p",
		"Q":"q",
		"R":"r",
		"S":"s",
		"T":"t",
		"U":"u",
		"V":"v",
		"W":"w",
		"X":"x",
		"Y":"y",
		"Z":"z",

		"_":"-",
		"plus":"=",
		"+":"=",
		"{":"[",
		"}":"]",
		":":";",
		"@":"'",
		"~":"#",
		"<":",",
		">":".",
		"?":"/",
		"|":"\\",
	

		"shift_backspace":"backspace",
		"shift_keypad_delete":"keypad_.",
		"shift_keypad_0":"keypad_0",
		"shift_keypad_1":"keypad_1",
		"shift_keypad_2":"keypad_2",
		"shift_keypad_3":"keypad_3",
		"shift_keypad_4":"keypad_4",
		"shift_keypad_6":"keypad_6",
		"shift_keypad_7":"keypad_7",
		"shift_keypad_8":"keypad_8",
		"shift_keypad_9":"keypad_9",

		"!":"1",
		"\"":"2",
		"¬":"`", 
		"£":"3", 	
		"$":"4",
		"%":"5",
		"^":"6",
		"&":"7",
		"*":"8",
		"(":"9",
		")":"0"
	}
	## LOOKUP TABLES FINISHED ##
	## START BASIC ##
	class basic:
		def interpreter(eds_lines):
			# Line number to skip to after repeat has finished
			skipdestination=-1
			for line_no, file_line in enumerate(eds_lines):
				# Getting rid of new line characters from input
				line = file_line.rstrip("\r\n")

				if(eco.debug >=2):
					print("Line: " + str(line_no) + ", Command: " + line + ", Length: " + str(len(line)))

				# Checks for skips caused by repeat function
				if skipdestination == -1:
					if(eco.debug >=3):
						print("Command being interporated")

					# Splitting line into command and command argument
					current_command=eco.basic.getCommand(line)
					current_arg=eco.basic.getArg(line)

					if current_command == "TYPE":
						eco.type(current_arg)
					elif current_command == "PRESS":
						eco.press(current_arg)
					elif current_command == "DELAY":
						timeToWait = float(current_arg)
						# Check for invalid delay length
						if(isnan(timeToWait)):
							if(eco.debug >=1):
								print("User passed attempted to use invalid delay length")
								print("Argument: " + current_arg)
							raise ValueError('User Error - Invalid Delay Length')
						eco.basic.delay(timeToWait)
					elif current_command == "REPEAT":
						repetitions = int(current_arg)
						# Check for invalid repeat length
						if(isnan(timeToWait)):
							if(eco.debug >=1):
								print("User passed attempted to use invalid repeat length ")
								print("Argument: " + current_arg)
							raise ValueError('User Error - Invalid Repeat Length')
						repeat_depth=1
						repeat_length=-1

						if(eco.debug >=3):
							print("Repeat open on line: " + str(line_no))

						# Looking for outer repeat end
						for cur_length, line_check in enumerate(eds_lines[line_no+1:]):
							if "REPEAT" in line_check:
								if(eco.debug>=3):
									print("Repeat open on line: " + str(cur_length+line_no+2))
								repeat_depth +=1
							if "END" in line_check:
								if(eco.debug>=3):
									print("Repeat close on line: " + str(cur_length+line_no+2))
								repeat_depth -=1
								repeat_end=cur_length+line_no+1
							if (repeat_depth == 0):
								if(eco.debug>=3):
									print("Outer repeat found")
								break

						# Error checking number of repeats
						if (repeat_depth != 0):
							if(eco.debug>=1):
								print("User did not close repeat correctly")
								print("Repeat location: " + str(line_no))
							raise ValueError('User Error - Unclosed Repeat')

						if(eco.debug>=2):
							print("Repeat Code Start: " + str(line_no+1))
							print("Repeat Code End: " + str(repeat_end-1))

						eco.basic.repeat(repetitions, eds_lines[line_no+1:repeat_end])
						skipdestination=repeat_end

						if(eco.debug>=2): 
							print("Skipping to: " + str(skipdestination))
					elif current_command == "CMT": 
						if(eco.debug>=1):
							print("User Comment: " + current_arg)
					else:
						if(eco.debug>=1):
							print("User did not give valid command")
							print("Command: " + current_command)
						raise Exception('User Error - Invalid command')
				else:
					if(eco.debug>=3):
						print("Skipping Command: " + str(line_no))

					if line_no == skipdestination:
						if(eco.debug>=3):
							print("Skipping stopped")
						skipdestination=-1

		# Repeat Function
		def repeat(reps, eds_lines):
			for i in range(int(reps)):
				eco.basic.interprator(eds_lines)
		# Delay Function
		def delay(seconds):
			sleep(seconds)

		# Gets command from line
		def getCommand(line):	
			command = line.split(" ")[0]
			return command

		# gets argument from line
		def getArg(line):	
			arg = line[line.find(" ")+1:];
			return arg
	## END BASIC ##
	# Press function
	def press (commandString):
		if commandString.find("++") != -1:
			print ("error")
		else:	
			commands = commandString.lower()
	
			commandlist = commands.split("+")		
			ModifierList = [
				["LCTRL", False],
				["LSHIFT", False],
				["LALT", False],
				["LGUI", False],
				["RCTRL", False],
				["RSHIFT", False],
				["RALT", False],
				["RGUI", False],
			]
			KeyList = []
			for command in commandlist:
				if(eco.debug >=2):
					print("Key found in press function: " + command)

				if command == "lctrl":
					ModifierList[7] = ["LCTRL", True]
				elif command == "lshift":
					ModifierList[6] = ["LSHIFT", True]
				elif command == "lalt":
					ModifierList[5] = ["LALT", True]
				elif command == "lgui":
					ModifierList[4] = ["LGUI", True]
				elif command == "rctrl":
					ModifierList[3] = ["RCTRL", True]
				elif command == "rshift":
					ModifierList[2] = ["RSHIFT", True]
				elif command == "ralt":
					ModifierList[1] = ["RALT", True]
				elif command == "rgui":
					ModifierList[0] = ["RGUI", True]
				else:
					KeyList.append(command)

			eco.sendHIDpacket(eco.createHIDpacket(KeyList,ModifierList))
			eco.sendHIDpacket(b'\x00\x00\x00\x00\x00\x00\x00\x00')
	
	def type(textString):	
		for key in textString:
			eco.sendHIDpacket(eco.createHIDpacket(key, [
				["LCTRL", False],
				["LSHIFT", False],
				["LALT", False],
				["LGUI", False],
				["RCTRL", False],
				["RSHIFT", False],
				["RALT", False],
				["RGUI", False],
			]))
			eco.sendHIDpacket(b'\x00\x00\x00\x00\x00\x00\x00\x00')
			sleep(0.01)

	def set_gadget_mode(gadget_mode):
		if(eco.onPi):
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-win/UDC 2>/dev/null")
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-other/UDC 2>/dev/null")
			os.system("echo \"\" > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC 2>/dev/null")
			if(gadget_mode == "simple"):
				os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-simple/UDC")
			elif(gadget_mode == "windows"):
				os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-win/UDC")
			elif(gadget_mode == "macos"):
				os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-other/UDC")
			elif(gadget_mode == "linux"):
				os.system("ls /sys/class/udc > /sys/kernel/config/usb_gadget/ecoduck-other/UDC")
			else:
				raise Exception("Invalid gadget mode selected")
			sleep(2)
		eco.gadget_mode=gadget_mode
		eco.update_hid_path()

	def get_gadget_mode():
		return eco.gadget_mode


	def update_hid_path():
		if(eco.onPi):
			eco.path=check_output("/bin/ls /dev/hidg*",shell=True).decode()[:-1]


	def loop_timeout_handler(signum, stackframe):
		# Helper function for connection functions
		raise Exception("Loop timeout")

	def test_timeout_handler(signum, stackframe):
		# Helper function for connection functions
		raise Exception("Test timeout")

	def send_timeout_handler(signum, stackframe):
		# Helper function for connection functions
		raise Exception("Send timeout")

	# Loops till connection tests fails
	def wait_for_keyboard_state(state, timeout=0):
		if(not timeout >= 0):
			raise Exception("Invaid HID timeout")
		if(timeout > 0):
			signal.signal(signal.SIGALRM, eco.loop_timeout_handler)
			signal.alarm(timeout)
		try:
			while(eco.is_hid_connected(2) != state):
				sleep(3)
		except Exception as e:
			if "Loop timeout" in str(e):
				return False
			raise e
		if(timeout > 0):
			signal.alarm(0)
		return True

	def wait_for_network_state(state, timeout=0):
		if(not timeout >= 0):
			raise Exception("Invaid Network timeout")
		if(timeout > 0):
			signal.signal(signal.SIGALRM, eco.loop_timeout_handler)
			signal.alarm(timeout)
		if(eco.gadget_mode == "simple"):
			raise Exception("Networking attempted on simple gadget mode")
		try:
			while(eco.is_network_connected() != state):
				sleep(3)
		except:
			# Time out has occured
			return False
		if(timeout > 0):
			signal.alarm(0)
		return True


	def is_network_connected():
		if(not eco.onPi):
			return True
		if(eco.gadget_mode == "simple"):
			raise Exception("Networking attempted on simple gadget mode")
		if(not eco.is_hid_connected()):
			return False
		ip=eco.get_ip()
		if(ip != "n/a"):
			response = os.system("ping -W 1 -c 1 " + ip)
			if(response == 0):
				return True
		return False

	def is_hid_connected(timeout=2):
		# Checks for a led HID packet from the host - proves target is connected, then resets capslock if it is on
		if(not timeout >= 0):
			raise Exception("Invaid HID timeout")
		if(not eco.onPi):
			return True
		fd=os.open(eco.path, os.O_NONBLOCK)
		while(1):
			try:
				os.read(fd,4)
			except:
				break
				
		signal.signal(signal.SIGALRM, eco.test_timeout_handler)
		signal.alarm(timeout)
		try:
			eco.sendHIDpacket(b'\x00\x00\x39\x00\x00\x00\x00\x00', 0)
			eco.sendHIDpacket(b'\x00\x00\x00\x00\x00\x00\x00\x00', 0)
			fd = os.open(eco.path, os.O_RDWR)
			state=os.read(fd,4)
			os.close(fd)
			if(state == b'\x02'):
				eco.sendHIDpacket(b'\x00\x00\x39\x00\x00\x00\x00\x00', 0)
				eco.sendHIDpacket(b'\x00\x00\x00\x00\x00\x00\x00\x00', 0)
				fd = os.open(eco.path, os.O_RDWR)
				state=os.read(fd,4)
				os.close(fd)
		except Exception as e:
			if "Test timeout" in str(e):
				return False
			raise e
		signal.alarm(0)
		return True

		#Pass a vector into the function for scancodes
	def createHIDpacket(KeyList, ModifierList):
		packet_length = 0
		binarystring = ""
		ModifierByte = 0
		ScanCodes = []
		# Gets hexs values for keys 
		for key in KeyList:
			if str(key) in eco.LookUpScanCode:
				ScanCodes.append(eco.LookUpScanCode[key])
			elif str(key) in eco.LookUpShiftLayer:
				ModifierList[6] = ["LSHIFT", True]
				ScanCodes.append(eco.LookUpScanCode[eco.LookUpShiftLayer[key]])

		ModifierStr = ""
		for modifier, state in ModifierList:
			if(eco.debug>=3):
				print(modifier + ":"+str(state))
			if(state):
				ModifierStr += "1"
			else:
				ModifierStr += "0"
			
		if(eco.debug>=2):
			print(ModifierStr)

		# Converts the first byte into int
		ModifierByte = int(ModifierStr,2)
	
		# Encodes the first byte to binary literal
		ModifierByte = chr(ModifierByte).encode()
	
		# The second byte is always set to null.
		NullByte = b'\x00'
	
		# Start to build the hid packet
		HIDpacket = ModifierByte + NullByte
		packet_length = 2
	
		# Add the remaining hex values to the hid packet
		for HexValue in ScanCodes:
			HIDpacket = HIDpacket + HexValue.encode()
			packet_length += 1

		# Fill reset of packet with null bytes
		while packet_length != 8:
			HIDpacket = HIDpacket + NullByte
			packet_length = packet_length + 1
		if(eco.debug>=3):
			print(":".join("{:02x}".format(ord(c)) for c in HIDpacket.decode()))
		return HIDpacket;

	#Function to send code to the hardware
	def sendHIDpacket(HIDpacket, timeout=4):
		# Writes packet to given path
		if(not os.path.exists(eco.path)):
			raise Exception("Gadget no longer exists")
		if(not timeout >= 0):
			raise Exception("Invalid send timeout")
		try:
			if(timeout > 0):
				signal.signal(signal.SIGALRM, eco.send_timeout_handler)
				signal.alarm(timeout)
			if(eco.onPi):
				fd = os.open(eco.path, os.O_RDWR)
				os.write(fd, HIDpacket)
				os.close(fd)
			else:
				print(":".join("{:02x}".format(ord(c)) for c in HIDpacket.decode()))
		except Exception as e:
			if "Send timeout" in str(e):
				return False
			raise e
		if(timeout > 0):
			signal.alarm(0)
		return True

	def get_ip():
		if(not eco.onPi):
			return "192.168.10.101"
		if(eco.gadget_mode == "simple"):
			raise Exception("Networking not available on simple gadget")
		if(not eco.is_hid_connected()):
			return "n/a"

		neighbors=check_output("ip neighbor", shell=True).decode()[:-1].split("\n")
		for entries in neighbors:
			data = entries.split(" ")
			if("bridge" == data[2]):
				if("192.168.10" == data[0][:10]):
					if("reachable" == data[-1]):
						return data[0]
					else:
						response = os.system("ping -W 1 -c 1 " + data[0])
						if(response == 0):
							return data[0]
		return "n/a"

	def get_os():
		if(not eco.onPi):
			return "n/a"
		if(not eco.is_hid_connected()):
			return "n/a"
		usbrequests=check_output("dmesg | tac | sed '/^.*new device is high-speed/q' | tac | grep \"USB DWC2 REQ 80 06 03\"",shell=True).decode()[:-1]
		lines=usbrequests.split("\n")
		fingerprints=[]
		total=0
		counter=0
		for line in lines:
			usbdata=line.split(" ")
			if(usbdata[-2] != "0000"):
				fingerprints.append(usbdata[-1])
		for data in fingerprints:
			if(data == "00ff"):
				counter += 1
			total +=1
		if(total == 0 ):
			raise Exception("Could not identify OS")
			return "n/a"
		if(counter == 0):
			return "macos"
		elif(counter == total):
			return "linux"
		else:
			return "windows"
		raise Exception("Could not identify OS")
		return "n/a"

	def setup_gadgets():
		if(os.path.exists("/sys/kernel/config/usb_gadget/ecoduck-simple")):
			print("Gadgets already configured")
			return
		script_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"gadget-configure.sh")
		call(script_path, shell=True)


	def __init__():
		# Making sure device is a raspberry
		if(platform.system() != "Linux"):
			eco.onPi=False
		if(platform.machine() != 'armv6l'):
			eco.onPi=False
		if(os.geteuid() != 0):
			raise Exception("Script not ran as root")
		if(eco.onPi):
			if(not os.path.exists("/sys/kernel/config/usb_gadget")):
				raise Exception("Device does not appear to have been configured to run ecoduck software")
			else:
				eco.setup_gadgets()
				eco.set_gadget_mode("simple")
		else:
			print("!!!! WARNING !!!!")
			print("Device appears NOT to be a raspberry pi")
			print("Running in testing mode")
			eco.gadget_mode="simple"
eco.__init__()
