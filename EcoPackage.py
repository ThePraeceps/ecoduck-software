#Press function
def press (commandString):
	
	if commandString.find("++") != -1:
		print ("error")
	else:	
		commands = commandString.lower()

		CodeSplitter = commands.split("+")		
		ModifierList = []
		StringList = []
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
				StringList.append(i)
		sendHIDpack(createHIDpack(StringList,ModifierList))

def DELAY(seconds):
	from time import sleep
	sleep(seconds)

def TYPE(inputs):	
	emptyList = []
	for char in inputs:
		anotherEmptyList = []
		anotherEmptyList.append(char)
		sendHIDpack(createHIDpack(char, emptyList))

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
		if str(i) in LookUpTable:
			HexValues["Value{0}".format(x)] = LookUpTable[i] 
		elif str(i) in LookUpTable2:
			LSHIFT = True
			HexValues["Value{0}".format(x)] = LookUpTable[LookUpTable2[i]]
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
			LALT = True
		if i == "LSHIFT":
			LSHIFT = True
		if i == "LCTRL":
			LCTRL = True

	#Create the first byte in binary
	FirstByte = bitwise(RGUI,binarystring) + bitwise(RALT,binarystring) + bitwise(RSHIFT, binarystring) + bitwise(RCTRL, binarystring) + bitwise(LGUI, binarystring) + bitwise(LALT, binarystring) + bitwise(LSHIFT, binarystring) + bitwise(LCTRL, binarystring) 

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
	os.write(fd, report)
	os.close(fd)