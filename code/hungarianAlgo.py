from munkres import Munkres, print_matrix
import numpy, sys
import re

def getCost(tier):
    return 2 * tier * tier

# Given a column number for augmented matrix, find its seminar number.
def getSeminar(index, q):
    s = 0
    for i in xrange(len(q)):
        s += q[i]
        if index < s:
            return i + 1
    return -1   # Shouldn't happen!

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

# Transfer array to Student-Seminar.
B = []
MCOST = 100000
for i in xrange(n):
    B.append([A[i][j] if j in A[i] else MCOST for j in xrange(1, m+1)])
# Duplicate columns for hungarian
B = numpy.array(B, dtype='int32')
Slices = list()
for i in xrange(m):
    Slices.append(numpy.tile(numpy.transpose([B[:,i]]), q[i]))
C = numpy.concatenate(tuple(Slices), axis=1)
# Add zero rows for dummy students
for i in xrange(sum(q) - n):
    C = numpy.vstack([C, numpy.zeros(sum(q), dtype='int32')])
C = C.astype(int)

# Apply Munkres library to calculate Hungarian.
print "Running Hungarian algorithm on matrix of dimension", C.shape
C = C.tolist()
m = Munkres()
indexes = m.compute(C)
total = 0
print "Student ID, Assigned Seminar, Cost"
for row, column in indexes:
    if row >= n: continue # Skip dummy students
    value = C[row][column]
    total += value
    print '%d, %d, %d' % (row, getSeminar(column, q), value)
print 'Total Cost: %d' % total

