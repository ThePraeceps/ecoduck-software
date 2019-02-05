#!/usr/bin/env python3
import re
def reader(lines):
	skiploc=-1
	for idx, line in enumerate(lines): # 0 Based Indexing
		if skiploc == -1:
			print(str(idx) + ": " + line)
			# print("Length: " + str(len(line)))
			if line[:6]== "REPEAT": 
				reps = line.lstrip("REPEAT ")
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
				repeat(reps, lines[idx+1:end])
				skiploc=end 
				# print("Skipping to: " + str(skiploc))
		else:
			# print("Skipping Value: " + line)
			if idx == skiploc:
				# print("Skipping stopped")
				skiploc=-1


def repeat(reps, lines):
	for i in range(int(reps)):
		# print("Repeat: " + str(i+1))
		reader(lines)

with open("cmd.txt", "r") as fd:
	lines = fd.read().splitlines()

for idx, line in enumerate(lines):
	lines[idx] = line.lstrip("\t")
reader(lines)
fd.close()