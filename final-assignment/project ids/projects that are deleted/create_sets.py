import csv

with open("10-100.csv") as f, open("deleted_ids.csv") as f2:
	header = next(f)
	st = set(f)
	st2 = set(f2)

	with open("deleted-10-100.csv", "w") as out:
		for line in st:
			if line in st2:
				out.writelines(line)