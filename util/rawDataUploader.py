from GJEMS.ephys.rawDataUpload import RawDataUploader
from easygui import fileopenbox, ynbox, msgbox
from time import asctime

try:
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
        print asctime() + ' : Reading Data.....'
        uploader.parseSpike2Data()
        uploader.uploadToGNode()

        msgbox(asctime() + ' : Finished. Data upload Completed.')
except Exception:
    a = raw_input('The program has encountered an error.' \
                   + 'If you can\'t figure out what when wrong, please take'\
                   + 'a screenshot if this window and send it to '\
                   + 'Ajayrama Kumaraswamy<ajayramak@bio.lmu.de>. Press any key to exit')



