import midi
import os

def create_separate_files(midi_file):
    """
    Create separate midi files for each track in the original file
    """
    original_pattern = midi.read_midifile(midi_file)

    track_count = 0
    while True:

        if len(original_pattern):
            individual_track = original_pattern.pop()
            pattern = midi.Pattern()
            pattern.make_ticks_abs()
            pattern.append(individual_track)

            midi.write_midifile("{0}_track{1}.mid".format(midi_file.replace(".mid",""), track_count), pattern)
            track_count += 1
        else:
            break


def folders():
    """
    Look in each folder of the current directory for files ending in .mid
    Call create_separate_files on each of those files.
    """
    files = os.listdir('.')
    for item in files:
        if os.path.isdir(item):
            midi_files = os.listdir(item)
            midi_files = [x for x in midi_files if x.endswith('.mid')]
            print(midi_files)
            for midi_file in midi_files:
                create_separate_files(os.path.join(os.path.abspath(item), midi_file))


if __name__ == '__main__':
    folders()