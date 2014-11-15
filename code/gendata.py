import csv, sys
from scipy import stats
import numpy

# Getting user input data
NDATA = int(raw_input("Number of datasets to generate: "))
n = int(raw_input("Number of students: "))
m = int(raw_input("Number of seminars: "))
k = int(raw_input("Number of selections per student: "))
if k > m:
    print "Invalid input!"
    sys.exit(1)
pref = int(raw_input("Student preference distribution [1) Uniform; 2) Slightly skewed; 3) Srongly skewed]: "))
if pref < 1 or pref > 3:
    print "Invalid distribution!"
    sys.exit(1)

# Generate random data
print "Generating random data..."
MODE = ["", "./data/Uniform", "./data/Skewed", "./data/VerySkewed"]
for i in xrange(NDATA):
    count = [0] * (m + 1)
    seminars = numpy.arange(1, m+1)
    if pref == 1:
        weights = (10,) * m
    elif pref == 2:
        weights = (12,) * (m / 3) + (10,) * (m / 3) + (8,) * (m - m / 3 - m / 3)
    else:   # pref=3
        weights = (18,) * (m / 4) + (10,) * (m / 2) + (6,) * (m - m / 2 - m / 4)
    weights = tuple(( x * 1.0 / sum(weights) for x in weights ))
    weights = list(numpy.random.permutation(weights))
    generator = stats.rv_discrete(name='custm', values=(seminars, weights))
    with open(MODE[pref] + str(i) + ".csv", 'wb') as csvfile:
        csvreader = csv.writer(csvfile)
        for i in xrange(n):
            selection = generator.rvs(size = k)
            # Retry until unique
            while (len(selection) != len(set(selection))):
                selection = generator.rvs(size = k)
            csvreader.writerow(selection)
            for s in selection:
                count[s] += 1
    print "Done! Selection statistics:", count


