import numpy, sys
import re
import copy

def getCost(tier):
    return 2 * tier * tier

# Parse an input line to (seminar, tier) pairs
def parseLine(line):
    tierStrings = re.split(':|;', line)
    splitTier = [x.split(",") for x in tierStrings]
    splitTierResult = list()
    for tier in xrange(len(splitTier)):
        splitTierResult.append(list())
        for selection in splitTier[tier]:
            sanitizedSelection = re.sub("\D", "", selection)
            if re.sub("\D", "", sanitizedSelection) != "":
                splitTierResult[tier].append(int(sanitizedSelection))
    result = dict()
    for i in xrange(len(splitTierResult)):
        for s in splitTierResult[i]:
            if not(1 <= s and s <= m):
                print "Warning: Student entered out-of-bound Seminar ID: %s" % line
            elif s in result:
                print "Warning: Student has multiple entry for %d on line %s" % (s, line)
            else:
                result[s] = getCost(i)

    return result

# Main function for running randomized assignment.
def randomAsgn(quotaRatio):
    return (0, [])

# Getting random sublist of a list
def randomSub(L):
    return []

#
# !-- Entry point --!
#
# Specify input file name. 
inputPath = "data/Fall2014"

# Ask for parameters from user
m = int(raw_input("Enter number of seminars (Seminar ID starts from 1): "))
qq = raw_input("Enter quotas for %d seminars: " % m)
if len(qq.split()) == 1:
    q = [int(qq.split()[0]) for i in xrange(m)]
elif len(qq.split()) == m:
    q = [int(qq.split()[i]) for i in xrange(m)]
else:
    print "Invalid quota input!"
    sys.exit(1)
iters = int(raw_input("Enter number of iterations to run randomized assignment: "))

# Load student selections from input file.
print "Parsing input file `%s`..." % inputPath
with open(inputPath, 'r') as f:
    userInput = f.readlines()
if userInput[-1].startswith("END"):
    userInput = userInput[:-1]
else:
    raise Exception("Last line of file must be END!")
    sys.exit(1)
A = [parseLine(line) for line in userInput] # Parse input lines
n = len(A)
print "Number of students: %s" % n
if sum(q) < n:
    print "Quota cannot fit all students!"
    sys.exit(1)

# Transfer input to (student,seminar) -> ranking mapping.
# Initialize (seminar, ranking) -> student mapping.
B = []
R = []
MCOST = 100000
for i in xrange(n):
    B.append([A[i][j] if j in A[i] else MCOST for j in xrange(1, m+1)])
for i in xrange(1, m+1):
    rankedFirst = list()
    rankedSecond = list()
    for s in xrange(n):
        if i in A[s] and A[s][i] == getCost(0):
            rankedFirst.append(s)
        elif i in A[s] and A[s][i] == getCost(1):
            rankedSecond.append(s)
    R.append((rankedFirst, rankedSecond))

# Mainloop for iterations
bestCost = sys.maxint
bestAsgn = list()
for i in xrange(iters):
    for j in xrange(1, max(q)+1):
        (currCost, currAsgn) = randomAsgn(j * 1.0 / max(q))
        if currCost < bestCost:
            bestCost = currCost
            bestAsgn = copy.deepcopy(currAsgn)
print "Best Cost: %d" % currCost
print "Assignment as follows:"
for i in xrange(len(bestAsgn)):
    print "%d -> %d" % (i, bestAsgn)
print "--------------------------------"

