import midi
import os
import sys
import random
from Markov import Markov

def parseMidis(sourcefolderName, outputFileName, markovOrder, parseFor):
    print "Begining parse"

    folderName = os.path.abspath(sourcefolderName)
    files = getFiles(folderName)
    print str(len(files)) + " files found"

    #parse each file and push to markovDS
    transitions = Markov()
    for fileName in files:
        parseFile(fileName, transitions, markovOrder, parseFor)

    print "Files parsed"

    #write as json to file
    transitions.writeToFile(outputFileName)
    print "Markov written to file"

def parseFile(fileName, transitions, markovOrder, parseFor):
    """
    parse each file and add data to markob object
    """
    try:
        tracks = midi.read_midifile(fileName)
    except:
        print "Bad File: %s" % fileName
        # os.remove(fileName)
        return

    markovOrder = int(markovOrder)

    resolution = tracks.resolution
    beat = float(resolution / 16)

    # Get each track
    while len(tracks):
        individual_track = tracks.pop()
        individual_track.make_ticks_abs()
        #Get each note in the track
        previousNotes = []
        previousNoteOnTime = None
        currentChord = []
        pitch = None
        length = None

        for event in individual_track:

            if type(event) is midi.NoteOnEvent and event.data[1] != 0: # noteOffs are ocasionaly notesOn with velocity of 0
                noteOnTime = event.tick
                pitch = event.data[0]

            elif type(event) is midi.NoteOffEvent or (type(event) is midi.NoteOnEvent and event.data[1] == 0):
                noteOffTime = event.tick
                length = noteOffTime - noteOnTime
                length = int( (length + float(beat / 2)) / beat )

            if pitch != None and ( type(event) is midi.NoteOnEvent and event.data[1] != 0 ):
                if noteOnTime == previousNoteOnTime:
                    currentChord.append(pitch)
                else:
                    print "Chord: %s" % currentChord
                    if parseFor == "pitch":
                        if len(previousNotes) >= markovOrder:
                            transitions.push( previousNotes[-markovOrder:] , str(currentChord) )
                        previousNotes.append(currentChord)
                    elif parseFor == "rhythm":
                        if len(previousNotes) >= markovOrder:
                            transitions.push( previousNotes[-markovOrder:] , length)
                        previousNotes.append(length)

                    currentChord = [pitch]
                    previousNoteOnTime = noteOnTime


def getFiles(folderName):
    """
    Look in each folder of the current directory for files ending in .mid
    """
    allFiles = []
    files = os.listdir( folderName )
    for item in files:
        item = os.path.join(folderName, item)
        if os.path.isdir(item):
            allFiles += getFiles( item )
        else:
            if item.endswith('.mid'):
                allFiles.append(item)

    return allFiles

if __name__ == '__main__':
    folderName= sys.argv[1]
    print "Parsing %s" % folderName
    folders(folderName)
    i = 0;
    for num in range(0,10000):
        if markov.get( (46,64) ) == 67:
            i += 1
