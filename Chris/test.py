#!/usr/bin/env python3
def reader(lines):
	skiploc=-1
	for idx, line in enumerate(lines): # 0 Based Indexing
		if skiploc == -1:
			stripped = line.lstrip("\t")
			print(str(idx) + ": " + stripped)
			print("Length: " + str(len(stripped)))
			if stripped[:6]== "REPEAT":
				reps = stripped.lstrip("REPEAT ")
				end=lines.index("END") # 0
				print("Repeat found")
				repeat(reps, lines[idx+1:end])
				print("Skipping started")
				skiploc=end
		else:
			if idx == skiploc:
				print("Skipping stopped")
				skiploc=-1


def repeat(reps, lines):
	for i in range(int(reps)):
		reader(lines)

with open("cmd.txt", "r") as fd:
	lines = fd.read().splitlines()
reader(lines)
fd.close()