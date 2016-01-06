from csv import DictReader, DictWriter


#fileList = ["avg-followers-per-project", "max-followers-per-project", "forks-per-project", 
 #   "nr-of-pull-requests-per-project", "number-of-commits-per-project", "stars-per-project"]

fileList = ["country-per-project", "languages-per-project"]

for fileName in fileList:
    with open('exports/!' + fileName + '.csv') as csvfile:
        reader = DictReader(csvfile)
        
        f = open("samples/comma-samples-combined.csv")
        finalDict = []
        badIds = f.read().split(", ")
        ids = []
        for i in badIds:
            ids.append(i.replace('"', ""))
        
        for row in reader:
            currentId = row[reader.fieldnames[0]]
            currentVal = row[reader.fieldnames[1]]
            if currentVal != "":
                print currentId
                finalDict.append({reader.fieldnames[0]: currentId, reader.fieldnames[1]: currentVal})
                ids.remove(currentId)
        
        for i in ids:
            finalDict.append({reader.fieldnames[0]: i, reader.fieldnames[1]: "unknown"})
        
        with open('exports/' + fileName + '.csv', 'w') as csvfile:
            fieldnames = reader.fieldnames
            writer = DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for finalD in finalDict:
                writer.writerow(finalD)
