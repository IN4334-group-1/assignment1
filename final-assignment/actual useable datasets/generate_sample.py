import csv
import random

fileName = "0-10-project-ids"
with open(fileName + ".csv", "rb") as f:
	lines = [line for line in f]
	random_choice = random.sample(lines, 500)
	with open("sample-" + fileName + ".csv", "wb") as f2:
		f2.write("".join(random_choice))