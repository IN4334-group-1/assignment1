import csv

with open("all_ids.csv") as f, open("10-100.csv") as f2:
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