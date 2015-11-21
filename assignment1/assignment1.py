import sh
from json import JSONDecoder
from os import listdir, path
from time import strptime, mktime
from subprocess import Popen, PIPE


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

def getAuthorsForFile(git, filePath):
    """Returns a dictionary with the authors as keys and the number of commits
    per author as values
    git: an sh.git instance
    filePath: a filepath relative to the base directory of the git repo"""
    
    commits = git.log("--no-merges", "--pretty=%an", filePath).split("\n")
    contributors = dict()
    for author in commits[0:len(commits)-1]:
        if author in contributors.keys():
            contributors[author] += 1
        else:
            contributors[author] = 1
    return (contributors, len(commits)-1)

def computeStatsOnFile(contribTuple):
    "Computes the following tuple: (#minor, #major, #total, %ownership)"
    (contrib, total) = contribTuple
    maxPercentage = 0.0
    minors = 0
    majors = 0
    for author, commits in contrib.items():
        currentPercentage = commits/total
        print(commits, total, currentPercentage)
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
    commits = git.log("--no-merges", "--pretty=%s,%h").split("\n")
    bugfixCommits = []
    for commit in commits:
        if commit.find(bugFixNr) != -1:
            commitTuple = commit.strip(",").split(",")
            bugfixCommits.append(commitTuple)
    
    return bugfixCommits

def linkCommitToFiles(hash):
    """Given a commit hash (small version), this functions finds the files that
    were changed in that specific commit"""
    changedFiles = git('diff-tree', '--no-commit-id', '--name-only', '-r', hash)
    changedFiles = changedFiles.split("\n")
    #Remove all files that do not end in .java
    filtered = [ f for f in changedFiles if f.endswith('.java') ]
    return filtered

def addTupleToTable(filename, tuple, table):
    """Adds the given tuple to the table, based on the filename. If the 
    filename was already present, the amount of bugs is increased by 1"""
    BUG_INDEX = 1;
    #table is: [filename] = [(tuple), # bugs]

    if filename in table:
        table[filename][BUG_INDEX] += 1
    else:
        table[filename] = [tuple, 1]

    return table #idk of dit moet of dat het bij reference is ;p

#def addBuglessFilesToTable(table):
    #checkout latest commit that we consider

    #loop through all files in the repo (in specific folders, only ending in .java)
    #TODO:
    #first create table with the files containing 1 or more bugs
    #then get the latest commit and loop through all the files that are currently available
    #for each file, check if it exists in the table: if not, add it with 0 bugs?
        #however, we use file versions, so use git hist and add every version of that file to the table?
    
########################################################################################################

if not path.isdir("lucene-solr"):
	sh.git.clone("https://github.com/apache/lucene-solr.git")

git = sh.git.bake("--no-pager", _cwd='lucene-solr')

#print(getAuthorsForFile(git, "build.xml"))
#print(computeStatsOnFile(getAuthorsForFile(git, "build.xml")))

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

print(issues)
print(len(issues))

a = linkBugFixNrToCommit(git, issues[0])

print(a)
linkCommitToFiles('b3a74d7')

testFileName = 'java_b3a74d7'
testTuple = (1,2,3,0.55)
testTable = {testFileName: [testTuple, 2]}
print(addTupleToTable(testFileName, testTuple, testTable))

#b3a74d74d26640cf10da19b924860a932f99fa4a
