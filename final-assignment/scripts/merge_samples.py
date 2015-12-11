
import csv
#first merge all the csv files
fout=open("sample-combined.csv","a")

# now the rest:    
for sample in ["0-10", "10-100", "100-1000", "1000+"]:
    f = open("sample-"+ sample +".csv")
    f.next() # skip the header
    for line in f:
         fout.write(line)
    f.close() # not really needed
fout.close()