import os
import sys

# temp workaround to launch scripts from the root
sys.path.append(os.getcwd())

from GJEMS.ephys.rawDataUpload import RawDataUploader
from easygui import fileopenbox, ynbox, msgbox
from time import asctime

smr = fileopenbox('Indicate the smr file to use', filetypes=['*.smr'])
csv = fileopenbox('Indicate the csv file to use', filetypes=['*.csv'])

location = "http://localhost:8000"
uploader = RawDataUploader(smr, csv, "bob", "pass", location=location)

upload = True
if uploader.checkExistenceOnServer():
    upload = ynbox('This data already exists on the server. Replace the data?')
    if not upload:
        msgbox('Data on the server not replaced')
    else:
        print 'Deleting Existing Data....'
        uploader.deleteExistent()

if upload:
    print asctime() + ' : Reading Data.....'
    uploader.parseSpike2Data()
    uploader.uploadToGNode()

    msgbox(asctime() + ' : Finished. Data upload Completed.')