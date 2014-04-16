from bbfreeze import Freezer




f = Freezer('neuronProfilerv0.1', includes= ['GJEMS.morph','LMIO.wrapper','neuronvisio', 'os','shutil','sys','json'])
f.addScript('basicMorphMetrics.py')
f()
