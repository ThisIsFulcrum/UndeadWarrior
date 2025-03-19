import time
import random

def animate(string, char="@", duration=1):
	length = len(string)
	for i in range(1, length+1):
		print("\r" + char*i, end="")
		time.sleep(duration/length/4)
	print("\r" + string, end=" ")
	time.sleep(duration/2)
	for i in range(length, 0, -1):
		print("\r" + char*i, end=" ")
		time.sleep(duration/length/4)
	print("\r", end=" ")

def reveal(string, char="@", duration=0.5):
	length = len(string)
	for i in range(1, length+1):
		print("\r" + char*i, end="")
		time.sleep(duration/length)
	print("\r" + string)

def puzzle(string, char="@", duration=0.5):
	length = len(string)
	layer = char*length
	mask = [i for i in range(length)]
	random.shuffle(mask)
	print("\r"+layer, end="")
	time.sleep(duration/length)
	for i in mask:
		layer = layer[:i] + string[i] + layer[i+1:]
		print("\r"+layer, end=" ")
		time.sleep(duration/length)
	print()