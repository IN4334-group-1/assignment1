import sh
from json import JSONDecoder
from os import listdir, path
from time import strptime, mktime
import csv

#TODO
#Save all filenames + versions in table
#Find commit(s) belonging to certain bugfix
#Save minor, major, total, ownership, (1 bug) in table for specific file
#Write down what choices we made and how we did everything :D

def isClosedResolved(issue):
    return issue['fields']['status']['name'] == "Closed" and issue['fields']['resolution']['name'] == "Fixed"

def isCorrectTimePeriod(issue):
    t = mktime(strptime(issue['fields']['resolutiondate'], TIMEFORMAT))
    return t >= START and t < END

def getAuthorsForFile(authors):
    """Returns a dictionary with the authors as keys and the number of commits
    per author as values
    authors: a list of authors"""
    contributors = dict()
    for author in authors:
        if author in contributors.keys():
            contributors[author] += 1
        else:
            contributors[author] = 1
    return (contributors, len(authors))

def computeStatsOnFile(contribTuple):
    "Computes the following tuple: (#minor, #major, #total, %ownership)"
    (contrib, total) = contribTuple
    maxPercentage = 0.0
    minors = 0
    majors = 0
    for author, commits in contrib.items():
        currentPercentage = commits/total
        if currentPercentage > maxPercentage:
            maxPercentage = currentPercentage
        if currentPercentage < 0.05:
            minors += 1
        else:
            majors += 1
    
    return (minors, majors, len(contrib.keys()), maxPercentage*100)

def linkBugFixNrToCommit(git, bugFixNr):
    """Given a bugfix nr (in the format: LUCENE-#NR#), this function returns the
    commit hash of this bugfix"""
    commits = git.log("--no-merges", "--pretty=%s:::%H", "--grep", bugFixNr + ":").strip("\n").split("\n")
    bugfixCommits = []
    for commit in commits:
        bugfixCommits.append(commit.split(":::")[1])
    return bugfixCommits

def linkCommitToFiles(commitHash):
    """Given a commit hash (small version), this functions finds the files that
    were changed in that specific commit"""
    changedFiles = git('diff-tree', '--no-commit-id', '--name-only', '-r', commitHash)
    changedFiles = changedFiles.split("\n")
    #Remove all files that do not end in .java
    filtered = [ f for f in changedFiles if f.endswith('.java') ]
    return filtered

def addTupleToTable(filename, metrics, table, nrOfBugs):
    """Adds the given tuple to the table, based on the filename. If the 
    filename was already present, the amount of bugs is increased by 1"""
    BUG_INDEX = 1;
    #table is: [filename] = [(metrics), # bugs]
    if filename in table:
        table[filename][BUG_INDEX] += nrOfBugs
    else:
        table[filename] = [metrics, nrOfBugs]

    return table #idk of dit moet of dat het bij reference is ;p

#def addBuglessFilesToTable(table):
    #checkout latest commit that we consider
    #get all files available
    #get different versions of the file

    #loop through all files in the repo (in specific folders, only ending in .java)
    #TODO:
    #then get the latest commit and loop through all the files that are currently available
    #for each file, check if it exists in the table: if not, add it with 0 bugs?
        #however, we use file versions, so use git hist and add every version of that file to the table?

def getListOfCommitsUptoCommit(git, commitHash, filePath): 
    """Given a git repository, a commithash and a filePath, this function returns a list 
    of commits upto (but excluding) this commit for this file"""
    # get commit hash in which this file was added
    addedCommitHash = git.log("--pretty=%H", "--diff-filter", "A", "--", filePath).split("\n")[0]
    
    # get a list of commits
    commitRange = addedCommitHash + "..." + commitHash
    commitList = git.rl("--pretty=%an", "--reverse", commitRange, 
            "--boundary", "--", filePath).split("\ncommit ")
    
    # unfortunately, this beast is pretty necessary
    # it does 3 things:
    # 1.    it checks if the commit is a 'boundary commit': if yes, it is only accepted
    #       if it is the 'addedCommitHash'
    # 2.    it removes the last commit, as this is the commit that is not wanted
    # 3.    it splits each hash\nauthorname in hash and authorname and selects the author
    if len(commitList) > 0 and commitList[0] != "":
       commits = [item.strip("\n").split("\n")[1] for item in commitList 
        if ((item.find("-") == -1 or item.find(addedCommitHash) != -1) 
            and item.find(commitHash) == -1)]
    else:
        commits = git.log("--pretty=%an", "-n", 1, commitHash, "--", filePath)
    return commits

def writeResultsToFile(results):
    """Writes the results to a .csv file, as follows:
    filename, minor, major, total, ownership, num_of_bugs"""
    listWriter = csv.writer(open('result.csv', 'w+'), 
                            delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for fileName, metrics in results.items():
        line = [fileName]
        line.extend(list(metrics[0]))
        line.append(metrics[1])
        listWriter.writerow(line)

def isBugFixCommit(commitMsg):
    return commitMsg.find("LUCENE-") != -1 or commitMsg.find("LUCENE_") != -1
        

########################################################################################################

if not path.isdir("lucene-solr"):
	sh.git.clone("https://github.com/apache/lucene-solr.git")

git = sh.git.bake("--no-pager", _cwd='lucene-solr')

# you cannot call git.rev-list, so add an alias: now we can call git.rl, which translates to git rev-list
git.config("alias.rl", "rev-list")

# load all files
decoder = JSONDecoder()
PATH = "issue_LUCENE"
TIMEFORMAT = "%Y-%m-%dT%H:%M:%S.000+0000"
START = mktime(strptime("2015-01-01T00:00:00.000+0000", TIMEFORMAT))
END = mktime(strptime("2015-07-01T00:00:00.000+0000", TIMEFORMAT))

issues = []

for f in ['12412224.json']:#listdir(PATH):
    jsonF = open(PATH + "/" + f)
    issue = decoder.decode(jsonF.read())
    if isClosedResolved(issue) and isCorrectTimePeriod(issue):
        issues.append(issue['key'])
        #break; #TODO: remove this


#print(issues)
#print(len(issues))

#a = linkBugFixNrToCommit(git, issues[0])

#print(a)
#linkCommitToFiles('b3a74d7')

#testFileName = 'java_b3a74d7'
#testTuple = (1,2,3,0.55)
#testTable = {testFileName: [testTuple, 2]}
#print(addTupleToTable(testFileName, testTuple, testTable))

results = {}


for issue in issues:
    commitHashes = linkBugFixNrToCommit(git, issue)
    for commitHash in commitHashes:
        for javaFile in linkCommitToFiles(commitHash):
            commits = getListOfCommitsUptoCommit(git, commitHash, javaFile)
            contribTuple = getAuthorsForFile(commits)
            fileStats = computeStatsOnFile(contribTuple)
            fileName = javaFile + "_" + commitHash
            results = addTupleToTable(fileName, fileStats, results, 1)

allCommitsInPeriod = git.log("--no-merges", "--pretty=%s:::%H", '--since={2015-01-01}', '--until={2015-07-01}').strip("\n").split("\n")
for commit in allCommitsInPeriod:
    print(commit)
    (msg,commitHash) = commit.split(":::")
    if not isBugFixCommit(msg):
        for javaFile in linkCommitToFiles(commitHash):
            commits = getListOfCommitsUptoCommit(git, commitHash, javaFile)
            contribTuple = getAuthorsForFile(commits)
            fileStats = computeStatsOnFile(contribTuple)
            fileName = javaFile + "_" + commitHash
            results = addTupleToTable(fileName, fileStats, results, 0)


writeResultsToFile(results)
    
    


