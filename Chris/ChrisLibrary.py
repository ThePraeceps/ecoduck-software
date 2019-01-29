#!/usr/bin/env python3

class eco:
	#if os == win:
	payload = open("win.txt", 'r')
	#elif os == lin:
	#	payload = open("lin.txt", 'r')
	#elif os == mac:
	#	payload = open("mac.txt", 'r')
	#else:
	#	print("Unable to detect OS!")
	def interpreter():
		
	def reader():
		toRead = 1
		lines = eco.payload.readlines()
		for line in lines:
			#debug
			stripped = line.rstrip("\r\n")
			print(len(currentLine))
			print(currentLine)
			print("BEFORE FINDER")
			if eco.commandFinder(stripped) == "TYPE":
				currentLine = stripped.lstrip("TYPE ")
				eco.type(currentLine)
			elif eco.commandFinder(stripped) == "COM": #do nothing
			elif eco.commandFinder(stripped) == "DELAY":
				currentLine = stripped.lstrip("DELAY ")
				timeToWait = int(currentLine)
				eco.delay(timeToWait)
			elif eco.commandFinder(stripped) == "PRESS":
				currentLine = currentLine = stripped.lstrip("PRESS ")
				eco.press()
			elif eco.commandFinder(stripped) == "REPEAT":
				currentLine = stripped.lstrip("REPEAT ")
				eco.repeat()
		payload.close()
	def repeat(commandString):
		
	def press(keyCommand):
	def delay(timeToWait):
		return
	def type(toType):
		return
	def commandFinder(line):	
		command = line.split(" ")[0]
		
		#print(len(command))
		#print(command)
		return command
eco.reader()
	
