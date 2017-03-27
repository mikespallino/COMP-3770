import midi
import os
import sys
import ast
import random
from Markov import Markov

NOTE_VELOCITY = 50
NOTE_DURATION = [110, 220, 440]

def compose(pitchInputFileName, rhythmInputFileName, outputFileName, songLength):
    pitchTransitions = Markov(pitchInputFileName)
    pithOrder = pitchTransitions.order()
    rhythmTransitions = Markov(rhythmInputFileName)
    rhythmOrder = rhythmTransitions.order()

    # Build random beging of song
    chords = []
    for i in range(pithOrder):
        chords.append( [random.randint(50,60)] )
    # Build list of chords
    while( len(chords) < songLength):
        newChord = pitchTransitions.get( chords[-pithOrder:] )
        if newChord is not None:
            newChord = ast.literal_eval(newChord)
            chords.append( newChord )
        else:
            print "INFO: No possible pitch/chord found"
            del chords[-1]
            chords.append( [random.randint(50,60)] )
    # prettier endings
    chords[-1] = chords[-2]

    # Create begining of rhythm track
    rhythms = []
    for i in range(rhythmOrder):
        rhythms.append( 4 )
    # Build list of note lengths
    while( len(rhythms) < songLength):
        newLength = rhythmTransitions.get( rhythms[-rhythmOrder:] )
        if newLength is not None:
            newLength = int(newLength)
            rhythms.append( newLength )
        else:
            print "INFO: No possible rhythm found"
            del rhythms[-1]
    #SONG SHOULD END WITH HOLE NOTE
    rhythms[-1] = 16
    rhythms[-2] = 16


    print "Song Composed:"

    # Make patern into
    pattern = midi.Pattern()
    pattern.make_ticks_abs()
    track = midi.Track()
    pattern.append(track)

    currentTick = 0

    for i in range(songLength):
        length = int( (220 / 16 ) * rhythms[i])
        # for pitch in chords[i]:
        for pitch in chords[i]:
            on = midi.NoteOnEvent(tick=0, velocity=NOTE_VELOCITY, pitch=pitch)
            track.append(on)
        for pitch in chords[i]:
            off = midi.NoteOffEvent(tick=length, pitch=pitch)
            track.append(off)

        currentTick += length

    eot = midi.EndOfTrackEvent(tick=currentTick)
    track.append(eot)
    midi.write_midifile(outputFileName, pattern)

    print "Song written to file: %s" % outputFileName
