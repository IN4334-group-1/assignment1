import csv

with open("0-10-owner-ids.csv") as f, open("company-ids.csv") as f2:
	header = next(f)
	st = set(f)
	st2 = set(f2)
	with open("0-10-big-companies.csv", "w") as out:
		out.writelines((line for line in st if line not in st2))