import easygui
import numpy as npy

"""
Does the following
  a. Converts root into a three point soma. Implementation taken from:  http://neuromorpho.org/neuroMorpho/SomaFormat.html
      1 1 xs ys zs rs -1
      2 1 xs (ys-rs) zs rs 1
      3 1 xs (ys+rs) zs rs 1
      
  b. labels all other points as type '3'
"""


fName = easygui.fileopenbox(msg='SWC file with single point soma', filetypes=['*.swc'])
inFile = npy.loadtxt(fName)

outFile = npy.zeros([inFile.shape[0]+2,inFile.shape[1]])

outFile[0,:] = inFile[0,:].copy()
outFile[0,1] = 1

rs = inFile[0,5] #radius of one-point soma


outFile[1,:] = npy.array([2, 1, inFile[0,2], inFile[0,3]-rs, inFile[0,4], rs, 1])
outFile[2,:] = npy.array([3, 1, inFile[0,2], inFile[0,3]+rs, inFile[0,4], rs, 1])

inParentVals = inFile[:,6]



for lineId in range(1,inFile.shape[0]):
  presLine = inFile[lineId,:].copy()
  
  if not presLine[6] == 1:	#points connected to the original single-point soma remains connected to same original point.
    presLine[6] += 2
  
  if not (presLine[1] == 3):
    presLine[1] = 3
  
  presLine[0] += 2
  outFile[lineId+2,:] = presLine
  
npy.savetxt(fName[:fName.index('.')]+'_3ptSoma.swc',outFile,'%d %d %0.12f %0.12f %0.12f %0.12f %d')  