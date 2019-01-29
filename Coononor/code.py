import os,signal,io
from subprocess import Popen, PIPE, check_output



LookUpTable = {

	"a":\x04
	"b":\x05
	"c":\x06
	"d":\x07
	"e":\x08
	"f":\x09
	"g":\x0a
	"h":\x0b
	"i":\x0c
	"j":\x0d
	"k":\x0e
	"l":\x0f
	"m":\x10
	"n":\x11
	"o":\x12
	"p":\x13
	"q":\x14
	"r":\x15
	"s":\x16
	"t":\x17
	"u":\x18
	"v":\x19
	"w":\x1a
	"x":\x1b
	"y":\x1c
	"z":\x1d

	"f1":\x3a
	"f2":\x3b
	"f3":\x3c
	"f4":\x3d
	"f5":\x3e
	"f6":\x3f
	"f7":\x40
	"f8":\x41
	"f9":\x42
	"f10":\x43
	"f11":\x44
	"f12":\x45

	"1":\x1e
	"2":\x1f
	"3":\x20
	"4":\x21
	"5":\x22
	"6":\x23
	"7":\x24
	"8":\x25
	"9":\x26
	"0":\x27
	"enter":\x28
	"esc":\x29
	"backspace":\x2a
	"tab":\x2b
	"space":\x2c
	"-":\x2d
	"=":\x2e
	"[":\x2f
	"]":\x30
	"\\":\x31
	"#":\x32
	";":\x33
	"'":\x34
	"`":\x35
	",":\x36
	".":\x37
	"/":\x38
	"caps_lock":\x39
	"print_screen":\x46
	"scroll_lock":\x47
	"pause":\x48
	"insert":\x49
	"home":\x4a
	"page_up":\x4b
	"delete":\x4c
	"end":\x4d
	"page_down":\x4e
	"right_arrow":\x4f
	"left_arrow":\x50
	"down_arrow":\x51
	"up_arrow":\x52
	"keypad_numlock":\x53
	"keypad_/":\x54
	"keypad_*":\x55
	"keypad_-":\x56
	"keypad_+":\x57
	"keypad_enter":\x58
	"keypad_1":\x59
	"keypad_2":\x5a
	"keypad_3":\x5b
	"keypad_4":\x5c
	"keypad_5":\x5d
	"keypad_6":\x5e
	"keypad_7":\x5f
	"keypad_8":\x60
	"keypad_8":\x61
	"keypad_0":\x62
	"keypad_.":\x63
}

LookUpTable2 = {
	"A":"a"
	"B":"b"
	"C":"c"
	"D":"d"
	"E":"e"
	"F":"f"
	"G":"g"
	"H":"h"
	"I":"i"
	"J":"j"
	"K":"k"
	"L":"l"
	"M":"m"
	"N":"n"
	"O":"o"
	"P":"p"
	"Q":"q"
	"R":"r"
	"S":"s"
	"T":"t"
	"U":"u"
	"V":"v"
	"W":"w"
	"X":"x"
	"Y":"y"
	"Z":"z"

	"_":"-"
	"+":"="
	"{":"["
	"}":"]"
	":":";"
	"@":"'"
	"~":"#"
	"<":","
	">":"."
	"?":"/"
	"|":"\\"
	"¬":"`"

	"shift_backspace":"backspace"
	"shift_keypad_delete":"keypad_."
	"shift_keypad_0":"keypad_0"
	"shift_keypad_1":"keypad_1"
	"shift_keypad_2":"keypad_2"
	"shift_keypad_3":"keypad_3"
	"shift_keypad_4":"keypad_4"
	"shift_keypad_6":"keypad_6"
	"shift_keypad_7":"keypad_7"
	"shift_keypad_8":"keypad_8"
	"shift_keypad_9":"keypad_9"

	"!":"1"
	"\"":"2"
	"£":"3"
	"$":"4"
	"%":"5"
	"^":"6"
	"&":"7"
	"*":"8"
	"(":"9"
	")":"0"

}
 
#Pass a vector into the function for scancodes
def createHex():

	#Creates and stores the first byte of the hid packet
	binarystring = bitwise(RGUI,binarystring) + bitwise(RALT,binarystring) + bitwise(RSHIFT, binarystring) + bitwise(RCTRL, binarystring) + bitwise(LGUI, binarystring) + bitwise(LALT, binarystring) + bitwise(LSHIFT, binarystring) + bitwise(LCTRL, binarystring) 

	binarystring = hex(int(binarystring,2))
	
	#Splits the binarystring so that the 0 at the start can be replaced with \
	a,b,c,d = binarystring
	
	#Format the new binarystring/first byte
	binarystring = "\\" + b + c + d
	binarystring = binarystring.encode()	

	#Stores the full hid packet
	string hex = binarystring + ;

	
	path=check_output("/bin/ls /dev/hidg*",shell=True).decode()[:-1]
	
	#Resets all the modifiers
	RGUI = False;
	RALT = False;
	RSHIFT = False;
	RCTRL = False;
	LGUI = False;
	LALT = False;
	LSHIFT = False;
	LCTRL = False;

#function to create the first byte of the packet
def bitwise(modifier, binarystring):
	if modifier == True:
		binarystring = binarystring + "1"
	else:
		binarystring = binarystring + "0"
	return binarystring
	
	
		
#Function to send code to The overlord
def write_report(report, path):
	# Writes packet to given path
	fd = os.open(path, os.O_RDWR)
	os.write(fd, report)
	os.close(fd)



#Main code

#global variables to declare what modifiers have been set.
#CreateHex function will reset them all to false after creating the hex packet 
bool RGUI = False;
bool RALT = False;
bool RSHIFT = False;
bool RCTRL = False;
bool LGUI = False;
bool LALT = False;
bool LSHIFT = False;
bool LCTRL = False;
binarystring = ""


createHex()







