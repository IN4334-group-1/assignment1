import csv
#first merge all the csv files
fout=open("all_ids.csv","a")
# first file:
for line in open("all_project_ids/ghtorrent-3.csv"):
    fout.write(line)
# now the rest:    
for num in range(4,19):
    f = open("all_project_ids/ghtorrent-"+str(num)+".csv")
    f.next() # skip the header
    for line in f:
         fout.write(line)
    f.close() # not really needed
fout.close()