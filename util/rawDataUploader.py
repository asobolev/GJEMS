#!/usr/bin/env python


from GJMorphSim.ephys.rawDataUpload import RawDataUploader
from easygui import fileopenbox, ynbox, msgbox

smr = fileopenbox('Indicate the smr file to use', filetypes=['*.smr'])
csv = fileopenbox('Indicate the csv file to use', filetypes=['*.csv'])

uploader = RawDataUploader(smr, csv)
upload = True
if uploader.checkExistenceOnServer():
    upload = ynbox('This data already exists on the server. Replace the data?')
    if not upload:
        msgbox('Data on the server not replaced')
    else:
        print 'Deleting Existing Data....'
        uploader.deleteExistent()

if upload:
    print 'Reading Data.....'
    uploader.parseSpike2Data()
    uploader.uploadToGNode()

    msgbox('Finished. Data uploaded')




