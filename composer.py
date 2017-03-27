import midi
import os
import sys
import random
from Markov import Markov

NOTE_VELOCITY = 50
NOTE_DURATION = [110, 220, 440]

def get_rand_duration():
    """
    This just randomly picks between eigth, quarter, and whole notes to add some
    variety
    """
    prob = random.randint(0, 100)
    if prob < 60:
        return 1
    elif prob < 90:
        return 2
    else:
        return 0

def compose(pitchInputFileName, rhythmInputFileName, outputFileName, songLength):
    pitchTransitions = Markov(pitchInputFileName)
    pithOrder = pitchTransitions.order()
    rhythmTransitions = Markov(rhythmInputFileName)
    rhythmOrder = rhythmTransitions.order()

    # Build random beging of song
    pitches = []
    for i in range(pithOrder):
        pitches.append( random.randint(50,60) )
    # Build list of pitches
    while( len(pitches) < songLength):
        newPitch = pitchTransitions.get( pitches[-pithOrder:] )
        if newPitch is not None:
            newPitch = int(newPitch)
            pitches.append( newPitch )
        else:
            print "INFO: No possible pitch found"
            del pitches[-1]
    # prettier endings
    pitches[-1] = pitches[-2]

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

    for i in range(songLength):
        length = int( (440 / 16 ) * rhythms[i] )
        pitch = pitches[i]

        on = midi.NoteOnEvent(tick=2, velocity=NOTE_VELOCITY, pitch=pitch)
        off = midi.NoteOffEvent(tick=length, pitch=pitch)
        track.append(on)
        track.append(off)

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)
    midi.write_midifile(outputFileName, pattern)

    print "Song written to file: %s" % outputFileName
