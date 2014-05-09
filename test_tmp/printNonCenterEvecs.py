from GJEMS.morph.morph import getPCADetails
import sys

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
testMorphFile = sys.argv[1]

evec1, stds = getPCADetails(testMorphFile, center=False)
print(evec1)