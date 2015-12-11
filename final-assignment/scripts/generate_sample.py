import csv
import random

fileName = "1000+"
with open(fileName + ".csv", "rb") as f:
	lines = [line for line in f]
	random_choice = random.sample(lines, 501)
	with open("sample-" + fileName + ".csv", "wb") as f2:
		f2.write("\n".join(random_choice))