from munkres import Munkres, print_matrix
import numpy, sys

# Given a column number for augmented matrix, find its seminar number.
def getSeminar(index, q):
    s = 0
    for i in xrange(len(q)):
        s += q[i]
        if index < s:
            return i + 1
    return -1   # Shouldn't happen!

# Get command-line parameter.
if len(sys.argv) <= 1:
    csvPath = "data/Uniform0.csv"   # Default
else:
    csvPath = sys.argv[1]

# Load selection from CSV file. Load parameters.
A = numpy.genfromtxt(csvPath, delimiter=",")
# Special case when k=1
if len(A.shape) == 1:
    A = numpy.reshape(A, (A.shape[0], 1))
n = len(A)
k = len(A[0])
m = int(max(numpy.ndarray.flatten(A)))
mm = raw_input("Enter number of seminars [%d]: " % m)
if mm != "":
    m = int(mm)
qq = raw_input("Enter quotas for %d seminars: " % m)
if len(qq.split()) == 1:
    q = [int(qq.split()[0]) for i in xrange(m)]
elif len(qq.split()) == m:
    q = [int(qq.split()[i]) for i in xrange(m)]
else:
    print "Invalid quota input!"
    sys.exit(1)
if sum(q) < n:
    print "Quota cannot fit all students!"
    sys.exit(1)

# Transfer array to Student-Seminar.
B = []
MCOST = 50
for i in xrange(n):
    B.append([A[i].tolist().index(j+1) if j+1 in A[i] else 50 for j in xrange(m)])
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
print C.shape

# Save the resulting augmented matrix as csv
numpy.savetxt("foo.csv", C, delimiter=",", fmt="%d")

# Apply Munkres library to calculate Hungarian.
C = C.tolist()
m = Munkres()
indexes = m.compute(C)
#print_matrix(matrix, msg='Lowest cost through this matrix:')
total = 0
for row, column in indexes:
    value = C[row][column]
    total += value
    print '(%d, %d) -> %d' % (row, getSeminar(column, q), value)
print 'total cost: %d' % total

