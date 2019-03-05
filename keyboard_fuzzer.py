from ecoduck import eco
scancodes = ["null"]*256
shiftcodes = ["null"]*256
altcodes = ["null"]*256

print("Normal scancodes")
for i in range(256):
		hex_keycode=str("0x%02X" % i)[-2:]
		mods=b'\x00'
		bytes_keycode=bytes([i])
		null=bytes(5)
		packet=mods+bytes(1)+bytes_keycode+null
		eco.sendHIDpacket(packet)
		eco.sendHIDpacket(bytes(8))
		print(":".join("{:02x}".format(ord(c)) for c in packet.decode()))
		result=input(hex_keycode + " : ")
		scancodes[i]=result

print("Shift scancodes")
for i in range(256):
		hex_keycode=str("0x%02X" % i)[-2:]
		mods=b'\x02'
		bytes_keycode=bytes([i])
		null=bytes(5)
		packet=mods+bytes(1)+bytes_keycode+null
		eco.sendHIDpacket(packet)
		eco.sendHIDpacket(bytes(8))
		print(":".join("{:02x}".format(ord(c)) for c in packet.decode()))
		result=input(hex_keycode + " : " + scancodes[i] + " : ")
		shiftcodes[i]=result

print("Alt scancodes")
for i in range(256):
		hex_keycode=str("0x%02X" % i)[-2:]
		mods=b'\x04'
		bytes_keycode=bytes([i])
		null=bytes(5)
		packet=mods+bytes(1)+bytes_keycode+null
		eco.sendHIDpacket(packet)
		eco.sendHIDpacket(bytes(8))
		print(":".join("{:02x}".format(ord(c)) for c in packet.decode()))
		result=input(hex_keycode + " : " + scancodes[i] + " : ")
		altcodes[i]=result

for i in range(10):
	print("\n")

print("Scancode lookup table")
print("")
for i in range(256):
	if(scancodes[i] != ""):
		print("\"" + scancodes[i] + "\":\"\\x" + str("0x%02X" % i)[-2:] + "\",")
print("Shiftcode lookup table")
print("")
for i in range(256):
	if(shiftcodes[i] != ""):
		print("\""+shiftcodes[i]+"\":\""+scancodes[i]+"\",")
print("")
print("Altcode lookup table")
for i in range(256):
	if(altcodes[i] != ""):
		print("\""+altcodes[i]+"\":\""+scancodes[i]+"\",")
print("")