Programs for running a simulation in Neuron using Python.

sim.py
	class BasicSim
    - import morphology; initialize biophysics, inputs and variables to record.
    - run simulation and visualize results.

morphImport.py
	class MorphImport
    - import morphology
    - create pointers to root section and terminal sections
    - read region demarkers and initialize region_ind.index for each section. This indicates the region to which sections belong.
	
	class SWCTreeWriter
	- writes the subtree attached to the argument section into a separate swc file.
	
morph.py
	-morphometric analysis functions
	
ephys/rawDataUpload.py 
	
	class RawDataUploader
	-handles the uploading of data from JAPAN
	
	extractCSVMetaData:
	-extracts CSV metadata
	
ephys/rawDataProcess.py

	class RawDataProcessor
	-handles extraction of regions of interest in vibration and voltage traces
	
ephys/simParamExtract.py

	class SimulationParameterExtracter
	-handles import to Current clamp data from smr files
	-extracts the ROIs and annotates with current injection particulars
	-saves using NEOHDF5 format
	-loads the above and processes it to extract time constants and input resistances.
	