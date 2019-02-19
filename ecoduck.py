#!/usr/bin/env python3

import os,signal,io,array
from subprocess import Popen, PIPE, check_output


class eco:
	#if os == win:
	payload = open("win.txt", 'r')
	#elif os == lin:
	#	payload = open("lin.txt", 'r')
	#elif os == mac:
	#	payload = open("mac.txt", 'r')
	#else:
	#	print("Unable to detect OS!")
	def reader(lines):
		skiploc=-1
		for idx, line in enumerate(lines):
			#debug
			stripped = line.rstrip("\r\n")
			#print("Length: " + str(len(stripped)))
			#print(skiploc)
			#print("BEFORE FINDER")
			if skiploc == -1:
				#print(str(idx) + ": " + stripped)
				#print("In finder")
				if eco.commandFinder(stripped) == "TYPE":
					currentLine = stripped[5:]
					eco.typeText(currentLine)
				elif eco.commandFinder(stripped) == "CMT": 
					#do nothing
					x=1
				elif eco.commandFinder(stripped) == "DELAY":
					currentLine = stripped[6:]
					timeToWait = int(currentLine)
					eco.delay(timeToWait)
				elif eco.commandFinder(stripped) == "PRESS":
					currentLine = currentLine = stripped[6:]
					eco.press(currentLine)
				elif eco.commandFinder(stripped) == "REPEAT":
					reps = int(stripped[7:])
					counts=1
					end=-1
					for edx, line in enumerate(lines[idx+1:]):
						if (line[:6]== "REPEAT"):
							counts +=1
						if (line == "END"):
							counts -=1
							end=edx
						if (counts == 0):
							break
					if (counts != 0):
						raise ValueError('User Error - Unclosed Repeat')
					end=idx+1+end
					# print("Start: " + str(idx+1))
					# print("End: " + str(end-1))
					eco.repeat(reps, lines[idx+1:end])
					skiploc=end 
					#print("Skipping to: " + str(skiploc))
			else:
				print("Skipping Value: " + line)
				if idx == skiploc:
					print("Skipping stopped")
					skiploc=-1
			eco.payload.close()

	#Repeat function
	def repeat(reps, lines):
		for i in range(int(reps)):
			eco.reader(lines)

	#Press function
	def press (commandString):
		
		if commandString.find("++") != -1:
			print ("error")
		else:	
			commands = commandString.lower()
	
			CodeSplitter = commands.split("+")		
			ModifierList = []
			KeypressList = []
			for i in CodeSplitter:
				print("The current word for i is: " + i)

				if i == "rgui":
				#set modifier to true
					ModifierList.append("RGUI")
				elif i == "ralt":
				#set modifier to true
					ModifierList.append("RALT")
				elif i == "rshift":
				#set modifier to true
					ModifierList.append("RSHIFT")
				elif i == "rctrl":
				#set modifier to true
					ModifierList.append("RCTRL")
				elif i == "lgui":
				#set modifier to true
					ModifierList.append("LGUI")
				elif i == "lalt":
				#set modifier to true
					ModifierList.append("LALT")
				elif i == "lshift":
				#set modifier to true
					ModifierList.append("LSHIFT")
				elif i == "lctrl":
				#set modifier to true
					ModifierList.append("LCTRL")
				else:
					KeypressList.append(i)
			eco.sendHIDpack(eco.createHIDpack(KeypressList,ModifierList))
			eco.sendHIDpack(b'\x00\x00\x00\x00\x00\x00\x00\x00')

	def delay(seconds):
		from time import sleep
		sleep(seconds)
	
	def typeText(inputs):	
		emptyList = []
		for char in inputs:
			eco.sendHIDpack(eco.createHIDpack(char, emptyList))
			eco.sendHIDpack(b'\x00\x00\x00\x00\x00\x00\x00\x00')

	def commandFinder(line):	
		command = line.split(" ")[0]
		return command
	
	#Lookup table	
	LookUpTable = {

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

	LookUpTable2 = {

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
		")":"0"}

	#Pass a vector into the function for scancodes
	def createHIDpack(ScanCodes = [], modifiers = []):
		RGUI = False
		RALT = False
		RSHIFT = False
		RCTRL = False
		LGUI = False
		LALT = False
		LSHIFT = False
		LCTRL = False
		length = 0
		x = 0
		binarystring = ""
		HexValues = {}
		#Formulate a lookup table for the scan codes 
		for i in ScanCodes:
			x = x + 1
			if str(i) in eco.LookUpTable:
				HexValues["Value{0}".format(x)] = eco.LookUpTable[i] 
			elif str(i) in eco.LookUpTable2:
				LSHIFT = True
				HexValues["Value{0}".format(x)] = eco.LookUpTable[eco.LookUpTable2[i]]
		for i in modifiers:
			if i == "RGUI":
				RGUI = True
			if i == "RALT":
				RALT = True
			if i == "RSHIFT":
				RSHIFT = True
			if i == "RCTRL":
				RCTRL = True
			if i == "LGUI":
				LGUI = True
			if i == "LALT":
				LALT = TrueP
			if i == "LSHIFT":
				LSHIFT = True
			if i == "LCTRL":
				LCTRL = True

		#Create the first byte in binary
		FirstByte = eco.bitwise(RGUI,binarystring) + eco.bitwise(RALT,binarystring) + eco.bitwise(RSHIFT, binarystring) + eco.bitwise(RCTRL, binarystring) + eco.bitwise(LGUI, binarystring) + eco.bitwise(LALT, binarystring) + eco.bitwise(LSHIFT, binarystring) + eco.bitwise(LCTRL, binarystring) 
	
		print(FirstByte)

		#Converts the first byte into int
		FirstByte = int(FirstByte,2)
	
		#encodes the first byte to hex
		FirstByte = chr(FirstByte).encode()
	
		#The second byte is always set to null.
		NullByte = "\x00"
	
		#Start to build the hid packet
		HIDpack = FirstByte + NullByte.encode()
	
		#Add the remaining hex values to the hid packet
		for i in HexValues:
			HIDpack = HIDpack + HexValues[i].encode()
			
		length = len(HexValues) + 2
	
		#Add the remainder of bytes as null bytes
		while length != 8:
			HIDpack = HIDpack + NullByte.encode()
			length = length + 1

		print(":".join("{:02x}".format(ord(c)) for c in HIDpack.decode()))
		return HIDpack;

	#function to create the first byte of the packet
	def bitwise(modifier, binarystring):
		if modifier == True:
			binarystring = binarystring + "1"
		else:
			binarystring = binarystring + "0"
		return binarystring
	

	#Function to send code to The overlord
	def sendHIDpack(HIDpack):
		path=check_output("/bin/ls /dev/hidg*",shell=True).decode()[:-1]
		# Writes packet to given path
		fd = os.open(path, os.O_RDWR)
		os.write(fd, HIDpack)
		os.close(fd)

eco.reader(eco.payload.read().splitlines())	
