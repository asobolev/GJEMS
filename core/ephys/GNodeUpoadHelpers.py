import gnodeclient
import numpy as np
import quantities as qu

#***********************************************************************************************************************
def checkIfExistsBlock(GNodeSession, blockName):
    """
    :GNodeSession: a gnode client session object
    :blockName: string specifying the name of the block
    :Gyan: Returns True if a block with name 'blockName' exists on the GNode Server to which 'GNodeSession' is connected
    """
    presentBlocks = GNodeSession.select(gnodeclient.Model.BLOCK, {"name": blockName})
    if len(presentBlocks):
        return True
    else:
        return False

#***********************************************************************************************************************

def checkIfExistsSection(GNodeSession, secName):
    """
    :GNodeSession: a gnode client session object
    :secName: string specifying the name of the section
    :Gyan: Returns True if a section with name 'secName' exists on the GNode Server to which 'GNodeSession' is connected
    """

    presentSecs = GNodeSession.select(gnodeclient.Model.SECTION, {"name": secName})
    if len(presentSecs):
        return True
    else:
        return False

#***********************************************************************************************************************

def deleteExistentBlock(GNodeSession, blockName):
    """
    :GNodeSession: a gnode client session object
    :blockName: string specifying the name of the block
    :Gyan: Deletes a block with the exact name 'blockName' on the GNode Server to which 'GNodeSession' is connected
    """

    assert blockName is not None, 'Parameter blockName cannot be None'

    block = GNodeSession.select(gnodeclient.Model.BLOCK, {"name": blockName})
    if len(block):
        blck = block[0]
        print 'Deleting Existing block named ' + blockName
        for segment in blck.segments:

            for child in segment.analogsignals:
                GNodeSession.delete(child)

            for child in segment.analogsignalarrays:
                GNodeSession.delete(child)

            for child in segment.eventarrays:
                GNodeSession.delete(child)

            for child in segment.events:
                GNodeSession.delete(child)

            for child in segment.spikes:
                GNodeSession.delete(child)

            for child in segment.spiketrains:
                GNodeSession.delete(child)

            for child in segment.epochs:
                GNodeSession.delete(child)

            for child in segment.epocharrays:
                GNodeSession.delete(child)

            for child in segment.irregularlysampledsignals:
                GNodeSession.delete(child)

            GNodeSession.delete(segment)
        GNodeSession.delete(blck)

        print 'Deleting Done'

    else:
        print 'Block ' + blockName + ' does not exist on the server'

#***********************************************************************************************************************

def deleteSection(GNodeSession, sec):
    """
    :GNodeSession: a gnode client session object
    :sec: a odml_adapted section object
    :Gyan: Deletes the section and all it's children  on the GNode Server to which 'GNodeSession' is connected
    """

    print 'Deleting Existing Section named ' + sec.name
    sec = GNodeSession.get(sec.location, refresh=True)
    for prop in sec.properties:
        for val in prop.values:
            GNodeSession.delete(val)
        GNodeSession.delete(prop)

    for s in sec.sections:
        deleteSection(GNodeSession, s)
    GNodeSession.delete(sec)

#***********************************************************************************************************************
def deleteExistentSection(GNodeSession, secName):
    """
    :GNodeSession: a gnode client session object
    :secName: string specifying the name of the section
    :Gyan: Deletes a section with the exact name 'secName' along with all its children on the GNode Server to which 'GNodeSession' is connected
    """

    assert secName is not None, 'Parameter secName cannot be None'

    sec = GNodeSession.select(gnodeclient.Model.SECTION, {"name": secName})

    print 'Deleting Existing Section named ' + sec[0].name
    if len(sec):
        deleteSection(GNodeSession, sec[0])

    else:
        print 'Section ' + secName + ' does not exist on the server'

#***********************************************************************************************************************


def cleanup(GNodeSession):
    """Closes 'GNodeSession'"""
    GNodeSession.close()

#***********************************************************************************************************************


def uploadNewBlockRecursive(GNodeSession, block):
    """
    :NOTE: RecordingChannel, RecordingChannelGroup and Unit have been left out from this implementation of recursive uploader
    :GNodeSession: a gnode client session object
    :block: a neo block(need not be one fetched from a GNode Server)
    :Gyan: Uploads 'block' with all its segments and all the SpikeTrains, Spikes, IrregularlySampledSignals, AnalogSignals, AnalogSignalArrays, Events, EventArrays, Epochs and EpochArrays of all the segments of 'block' to the GNode server to which 'GNodeSession' is connected. Also establishes the relationships between the uploaded objects as in 'block'.
    :Returns: location of the uploaded block on the server. One may run 'GNodeSession.get(location, refresh=True, recursive=True)' to get a block exactly similar in structure to 'block' but with all objects being returned from the server.

    """
    blk = GNodeSession.set(block)

    for segment in block.segments:

        seg = GNodeSession.set(segment)
        seg.block = blk
        seg = GNodeSession.set(seg)

        for spiketrain in segment.spiketrains:

            spt = GNodeSession.set(spiketrain)
            spt.segment = seg
            spt = GNodeSession.set(spt)

        for spike in segment.spikes:

            sp = GNodeSession.set(spike)
            sp.segment = seg
            sp = GNodeSession.set(sp)

        for irss in segment.irregularlysampledsignals:

            iss = GNodeSession.set(irss)
            iss.segment = seg
            iss = GNodeSession.set(iss)

        for analogSignal in segment.analogsignals:

            analog = GNodeSession.set(analogSignal)
            analog.segment = seg
            analog = GNodeSession.set(analog)

        for analogSignalArray in segment.analogsignalarrays:

            analogA = GNodeSession.set(analogSignalArray)
            analogA.segment = seg
            analogA = GNodeSession.set(analogA)

        for event in segment.events:

            ev = GNodeSession.set(event)
            ev.segment = seg
            ev = GNodeSession.set(ev)

        for eventarray in segment.eventarrays:

            eva = GNodeSession.set(eventarray)
            eva.segment = seg
            eva = GNodeSession.set(eva)

        for epoch in segment.epochs:

            ep = GNodeSession.set(epoch)
            ep.segment = seg
            ep = GNodeSession.set(ep)

        for epocharray in segment.epocharrays:

            epa = GNodeSession.set(epocharray)
            epa.segment = seg
            epa = GNodeSession.set(epa)

    return blk.location

#***********************************************************************************************************************

def setPropertyOfSection(GNodeSession, section, propert):
    """
    :section: A section fetched from a GNode Server
    :propert: An odml property(need not be fetched from a Gnode Server)
    :Gyan: This function recursively uploads the property 'propert' and all it's values as children and grandchildren of 'section'.
    """
    section.append(propert)
    prope = GNodeSession.set(propert)
    vals = propert.values
    prope.values = vals
    for val in vals:
        val = GNodeSession.set(val)

    return prope.location

#***********************************************************************************************************************


def uploadNewSectionRecursive(GNodeSession, s):
    """
    :GNodeSession: A gnode client session object
    :section: An OdML section(need not be one fetched from a GNode Server)
    :Gyan: Uploads 'section' with its entire children-tree to the GNode Server to which 'GNodeSession' is connected. Also establishes the relationships between the uploaded objects as in 'section'.
    :Returns: location of the uploaded section on the server. One may run 'GNodeSession.get(location, refresh=True, recursive=True)' to get a section exactly similar in structure to 'section' but with all objects being returned from the server.
    """
    sect = GNodeSession.set(s)

    for prop in s.properties:
        setPropertyOfSection(GNodeSession, sect, prop)

    for se in s.sections:
        sect.append(se)
        uploadNewSectionRecursive(GNodeSession, se)

    return sect.location

#***********************************************************************************************************************

getValuesOfProperty = lambda properti: qu.Quantity(np.array([float(x.value.split(' ')[0]) for x in properti.values]),\
                                           units=properti.values[0].value.split(' ')[1])

#***********************************************************************************************************************

unicode2quantities = lambda unicodeStr : qu.Quantity(np.array(unicodeStr.split(' ')[0],'float'),
                                                     units = unicodeStr.split(' ')[1])

#***********************************************************************************************************************

find_nearest_Id = lambda array,value: (np.abs(array-value)).argmin()

#***********************************************************************************************************************

#***********************************************************************************************************************