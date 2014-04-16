#***********************************Code for importing in Blender ******************************************************
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/python2.7/dist-packages')
with open('/home/ajay/repos/GJEMS/test_tmp/ImportSWCBlender.py', 'r') as f:
    code = f.read()
    exec(code)

abc = BlenderSWCImporter('/home/ajay/repos/GJEMS/test_tmp/swcFiles/HB060602_3ptSoma.swc')
# abc = BlenderSWCImporter('/home/ajay/repos/GJEMS/test_tmp/swcFiles/toyNeuron.swc')

abc.definePoints()
abc.drawInBlender()
abc.export2Obj()
# import code
# namespace = globals().copy()
# namespace.update(locals())
# code.interact(local=namespace)
#***********************************************************************************************************************