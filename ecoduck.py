#!/usr/bin/env python3

import os,signal,io,array
from subprocess import Popen, PIPE, check_output
from math import isnan
from time import sleep

class eco:
	debug=False
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
		def interprator(eds_lines):
			# Line number to skip to after repeat has finished
			skipdestination=-1
			for line_no, file_line in enumerate(eds_lines):
				# Getting rid of new line characters from input
				line = file_line.rstrip("\r\n")

				if(eco.debug):
					print("Line: " + str(line_no) + ", Command: " + line + ", Length: " + str(len(line)))

				# Checks for skips caused by repeat function
				if skipdestination == -1:
					if(eco.debug):
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
							if(eco.debug):
								print("User passed attempted to use invalid delay length")
								print("Argument: " + current_arg)
							raise ValueError('User Error - Invalid Delay Length')
						eco.basic.delay(timeToWait)
					elif current_command == "REPEAT":
						repetitions = int(current_arg)
						# Check for invalid repeat length
						if(isnan(timeToWait)):
							if(eco.debug):
								print("User passed attempted to use invalid repeat length ")
								print("Argument: " + current_arg)
							raise ValueError('User Error - Invalid Repeat Length')
						repeat_depth=1
						repeat_length=-1

						if(eco.debug):
							print("Repeat open on line: " + str(line_no))

						# Looking for outer repeat end
						for cur_length, line_check in enumerate(eds_lines[line_no+1:]):
							if "REPEAT" in line_check:
								if(eco.debug):
									print("Repeat open on line: " + str(cur_length+line_no+1))
								repeat_depth +=1
							if "END" in line_check:
								if(eco.debug):
									print("Repeat close on line: " + str(cur_length+line_no+1))
								repeat_depth -=1
								repeat_end=repeat_length
							if (counts == 0):
								print("Outer repeat found")
								break

						# Error checking number of repeats
						if (counts != 0):
							if(eco.debug):
								print("User did not close repeat correctly")
								print("Repeat location: " + str(line_no))
							raise ValueError('User Error - Unclosed Repeat')

						repeat_end=line_no+1+repeat_end
						if(eco.debug):
							print("Repeat Code Start: " + str(line_no+1))
							print("Repeat Code End: " + str(repeat_end-1))

						eco.basic.repeat(reps, lines[line_no+1:repeat_end-1])
						skipdestination=repeat_end

						if(eco.debug): 
							print("Skipping to: " + str(skipdestination))
					elif current_command == "CMT": 
						if(eco.debug):
							print("User Comment: " + current_arg)
					else:
						if(eco.debug):
							print("User did not give valid command")
							print("Command: " + current_command)
						raise ValueError('User Error - Invalid command')
				else:
					if(eco.debug):
						print("Skipping Command: " + str(line_no))

					if line_no == skipdestination:
						if(eco.debug):
							print("Skipping stopped")
						skipdestination=-1

		# Repeat Function
		def repeat(reps, eds_lines):
			for i in range(int(reps)):
				eco.reader(lines)
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
				if(eco.debug):
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
		NoModifiers = [
				["LCTRL", False],
				["LSHIFT", False],
				["LALT", False],
				["LGUI", False],
				["RCTRL", False],
				["RSHIFT", False],
				["RALT", False],
				["RGUI", False],
			]
		for key in textString:
			eco.sendHIDpacket(eco.createHIDpacket(key, NoModifiers))
			eco.sendHIDpacket(b'\x00\x00\x00\x00\x00\x00\x00\x00')

	#Pass a vector into the function for scancodes
	def createHIDpacket(KeyList = [], ModifierList = []):
		packet_length = 0
		binarystring = ""
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
			if(eco.debug):
				print(modifier + ":"+str(state))
			if(state):
				ModifierStr += "1"
			else:
				ModifierStr += "0"
			
		if(eco.debug):
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
		if(eco.debug):
			print(":".join("{:02x}".format(ord(c)) for c in HIDpacket.decode()))
		return HIDpacket;

	#Function to send code to The overlord
	def sendHIDpacket(HIDpacket):
		path=check_output("/bin/ls /dev/hidg*",shell=True).decode()[:-1]
		# Writes packet to given path
		fd = os.open(path, os.O_RDWR)
		os.write(fd, HIDpacket)
		os.close(fd)
	# Loops till connection tests fails
	def wait_for_disconnect():
		print("Waiting for device removal")
		while(eco.test_connection("/dev/hidg0",1)):
			sleep(3)
		print("Disconnected!")


	def timeout_handler():
		# Helper function for electrical_test
		raise Execption("Timeout")

	def test_connection(path, timeout):
		# Checks for a led HID packet from the host - proves target is connected, then resets capslock if it is on
		signal.signal(signal.SIGALRM, eco.timeout_handler)
		signal.alarm(timeout)
		try:
			eco.sendHIDpacket(b'\x00\x00\x39\x00\x00\x00\x00\x00')
			eco.sendHIDpacket(b'\x00\x00\x00\x00\x00\x00\x00\x00')
			fd = os.open(path, os.O_RDWR)
			state=os.read(fd,4)
			os.close(fd)
			if(state == b'\x02'):
				eco.sendHIDpacket(b'\x00\x00\x39\x00\x00\x00\x00\x00')
				eco.sendHIDpacket(b'\x00\x00\x00\x00\x00\x00\x00\x00')
				fd = os.open(path, os.O_RDWR)
				state=os.read(fd,4)
				os.close(fd)
		except:
			return False
		signal.alarm(0)
		return True

	def get_target_ip():
		fd = io.open("/var/lib/misc/dnsmasq.leases", "r")
		firstline = fd.readline()
		columns=firstline.split(" ")
		print("Found target IP: " + columns[2])
		return columns[2]

	def get_target_os():
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
			return "Unknown"
		if(counter == 0):
			return "MacOS"
		elif(counter == total):
			return "Linux"
		else:
			return "Windows"

		return "Unknown"

