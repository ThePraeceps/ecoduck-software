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
	##def start(fromRepeat=None):
	##	if fromRepeat!=None:
	##		eco.reader(payload.fromRepeat)
	##	else:
	##		eco.reader(eco.payload.readlines())
	def reader(lines):
		skiploc=-1
		for idx, line in enumerate(lines):
			#debug
			stripped = line.rstrip("\r\n")
			#print(str(idx) + ": " + stripped)
			#print("Length: " + str(len(stripped)))
			#print(skiploc)
			#print("BEFORE FINDER")
			if skiploc == -1:
				print("In finder")
				if eco.commandFinder(stripped) == "TYPE":
					currentLine = stripped.lstrip("TYPE ")
					eco.type(currentLine)
				elif eco.commandFinder(stripped) == "CMT": 
					#do nothing
					x=1
				elif eco.commandFinder(stripped) == "DELAY":
					currentLine = stripped.lstrip("DELAY ")
					timeToWait = int(currentLine)
					eco.delay(timeToWait)
				elif eco.commandFinder(stripped) == "PRESS":
					currentLine = currentLine = stripped.lstrip("PRESS ")
					eco.press()
				elif eco.commandFinder(stripped) == "REPEAT":
					reps = stripped.lstrip("REPEAT ")
					end=lines.index("END",idx)
					eco.repeat(reps, lines[idx+1:end])
					print("Skipping started")
					skiploc=end
					print("Skip value: "+str(skiploc))
			else:
				print("Skipping Line")
				if idx == skiploc:
					print("Skipping stopped")
					skiploc=-1				
					#eco.interpreter()
			eco.payload.close()
	#def interpreter():
	def repeat(reps, lines):
		for i in range(int(reps)):
			eco.reader(lines)
	#def press(keyCommand):
	def delay(timeToWait):
		return
	def type(toType):
		return
	def commandFinder(line):	
		command = line.split(" ")[0]
		#print(len(command))
		#print(command)
		return command
#eco.start()
eco.reader(eco.payload.read().splitlines())	
