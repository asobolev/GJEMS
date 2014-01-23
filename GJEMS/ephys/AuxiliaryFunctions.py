import gnodeclient

#***********************************************************************************************************************
def checkIfExistsBlock(GNodeSession, blockName):

    presentBlocks = GNodeSession.select(gnodeclient.Model.BLOCK, {"name": blockName})
    if len(presentBlocks):
        return True
    else:
        return False

#***********************************************************************************************************************

def checkIfExistsSection(GNodeSession, secName):

    presentSecs = GNodeSession.select(gnodeclient.Model.SECTION, {"name": secName})
    if len(presentSecs):
        return True
    else:
        return False

#***********************************************************************************************************************

def deleteExistentBlock(GNodeSession, blockName):

    assert blockName is not None, 'Parameter blockName cannot be None'

    block = GNodeSession.select(gnodeclient.Model.BLOCK, {"name": blockName})
    if len(block):
        block = block[0]
        print 'Deleting  Existing block named' + blockName
        for segment in block.segments:
            for analogsignal in segment.analogsignals:
                GNodeSession.delete(analogsignal)

            for event in segment.eventarrays:
                GNodeSession.delete(event)

            GNodeSession.delete(segment)
        GNodeSession.delete(block)

        print 'Deleting Done'

    else:
        print 'Block ' + blockName + ' does not exist on the server'

#***********************************************************************************************************************


def deleteExistentSection(GNodeSession, secName):

    assert secName is not None, 'Parameter secName cannot be None'

    sec = GNodeSession.select(gnodeclient.Model.SECTION, {"name": secName})
    if len(sec):
        sec = sec[0]
        print 'Deleting Existing Section named ' + sec.name
        for prop in sec.properties:
            for val in prop.values:
                GNodeSession.delete(val)
            GNodeSession.delete(prop)
        GNodeSession.delete(sec)
        print 'Deleting Done'
    else:
        print 'Section ' + secName + ' does not exist on the server'

#***********************************************************************************************************************


def cleanup(GNodeSession):

    GNodeSession.close()

#***********************************************************************************************************************


def setPropertyOfSection(GNodeSession, section, propert):
    """
    section must be something returned by a set command on a section.
    propert must be an odml property locally created(i.e. in the scope of the calling function).
    """
    section.append(propert)
    prop = GNodeSession.set(propert)
    vals = propert.values
    prop.values = vals
    for val in vals:
        val = GNodeSession.set(val)

#***********************************************************************************************************************
