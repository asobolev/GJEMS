import sys
import json


from GJEMS.morph.morph import BasicMorph


assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcfName = sys.argv[1]
testMorph = BasicMorph(swcfName)
print('startJSON' + json.dumps(testMorph.getTipUVOpenY()))