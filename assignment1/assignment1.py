import sh
from json import JSONDecoder
from os import listdir, path
from time import strptime, mktime
from subprocess import Popen, PIPE

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
    commits = git.log("--no-merges", "--pretty=%s,%H").split("\n")
    bugfixCommits = []
    for commit in commits:
        if commit.find(bugFixNr) != -1:
            commitTuple = commit.strip(",").split(",")
            bugfixCommits.append(commitTuple)
    
    return bugfixCommits
    
########################################################################################################

if not path.isdir("lucene-solr"):
	sh.git.clone("https://github.com/apache/lucene-solr.git")

git = sh.git.bake("--no-pager", _cwd='lucene-solr')

print(getAuthorsForFile(git, "build.xml"))

print(computeStatsOnFile(getAuthorsForFile(git, "build.xml")))

# load all files
decoder = JSONDecoder()
PATH = "issue_LUCENE"
TIMEFORMAT = "%Y-%m-%dT%H:%M:%S.000+0000"
START = mktime(strptime("2015-01-01T00:00:00.000+0000", TIMEFORMAT))
END = mktime(strptime("2015-07-01T00:00:00.000+0000", TIMEFORMAT))

issues = []

for f in listdir(PATH):
    jsonF = open(PATH + "/" + f)
    issue = decoder.decode(jsonF.read())
    if isClosedResolved(issue) and isCorrectTimePeriod(issue):
        issues.append(issue['key'])

print(issues)
print(len(issues))

print(linkBugFixNrToCommit(git, issues[0]))
