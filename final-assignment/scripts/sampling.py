import csv
import random

with open("all_ids.csv", "rb") as f:
	lines = [line for line in f]
	random_choice = random.sample(lines, 1000)
	with open("random_temp.csv", "wb") as f2:
		f2.write("\n".join(random_choice))


with open("random_temp.csv") as f, open("10-100.csv") as f2:
	header = next(f)
	st = set(f)
	with open("temp1.csv", "w") as out:
		out.writelines((line for line in st if line not in f2))

with open("temp1.csv") as f, open("100-1000.csv") as f2:
	header = next(f)
	st = set(f)
	with open("temp2.csv", "w") as out:
		out.writelines((line for line in st if line not in f2))

with open("temp2.csv") as f, open("1000+.csv") as f2:
	header = next(f)
	st = set(f)
	with open("0-10.csv", "w") as out:
		out.writelines((line for line in st if line not in f2))