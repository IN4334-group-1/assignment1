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
    #
    # TODO: AANPASSEN NAAR git.log --grep=bugfixNr + ":"
    #
    commits = git.log("--no-merges", "--pretty=%s,%H").split("\n")
    bugfixCommits = []
    for commit in commits:
        if commit.find(bugFixNr) != -1:
            commitTuple = tuple(commit.strip(",").split(","))
            bugfixCommits.append(commitTuple)
    
    return bugfixCommits

def getListOfCommitsUptoCommit(git, commitHash, filePath): 
    """Given a git repository, a commithash and a filePath, this function returns a list 
    of commits upto (but excluding) this commit for this file"""
    # get commit hash in which this file was added
    addedCommitHash = git.log("--pretty=%H", "--diff-filter", "A", "--", filePath).split("\n")[0]
    
    # get a list of commits
    commitRange = addedCommitHash + "..." + commitHash
    commitList = git.rl("--pretty=%an", "--reverse", commitRange, 
            "--boundary", filePath).split("\ncommit ")

    # unfortunately, this beast is pretty necessary
    # it does 3 things:
    # 1.    it checks if the commit is a 'boundary commit': if yes, it is only accepted
    #       if it is the 'addedCommitHash'
    # 2.    it removes the last commit, as this is the commit that is not wanted
    # 3.    it splits each hash\nauthorname in hash and authorname and selects the author
    commits = [item.strip("\n").split("\n")[1] for item in commitList 
        if ((item.find("-") == -1 or item.find(addedCommitHash) != -1) 
            and item.find(commitHash) == -1)]
    return commits

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

for f in listdir(PATH):
    jsonF = open(PATH + "/" + f)
    issue = decoder.decode(jsonF.read())
    if isClosedResolved(issue) and isCorrectTimePeriod(issue):
        issues.append(issue['key'])

print(issues)
print(len(issues))

print(linkBugFixNrToCommit(git, issues[0]))
