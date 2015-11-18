import sh
from json import JSONDecoder
from os import listdir, path
from time import strptime, mktime

if not path.isdir("/lucene-solr"):
    print('yay')
else:
    sh.git.clone("https://github.com/apache/lucene-solr.git")

git = sh.git.bake(_cwd='lucene-solr')

### read a json file

# load all files
maxIssueNr = -1

closed = 0

decoder = JSONDecoder()
PATH = "issue_LUCENE"
TIMEFORMAT = "%Y-%m-%dT%H:%M:%S.000+0000"
START = mktime(strptime("2015-01-01T00:00:00.000+0000", TIMEFORMAT))
END = mktime(strptime("2015-07-01T00:00:00.000+0000", TIMEFORMAT))


issues = []

jsonF = open(PATH + "/12314162.json")
decodedJson = decoder.decode(jsonF.read())

#print(decodedJson['fields']['resolutiondate'])#.keys())

def isClosedResolved(issue):
    return issue['fields']['status']['name'] == "Closed" and issue['fields']['resolution']['name'] == "Fixed"

def isCorrectTimePeriod(issue):
    t = mktime(strptime(decodedJson['fields']['resolutiondate'], TIMEFORMAT))
    return t >= START and t < END

for f in listdir(PATH):
    jsonF = open(PATH + "/" + f)
    decodedJson = decoder.decode(jsonF.read())
    if isClosedResolved(decodedJson) and isCorrectTimePeriod(decodedJson):
        issues.append(decodedJson['key'])

print(issues)
print(len(issues))

