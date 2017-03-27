import sys
from trackParser import parseMidis
from composer import compose

def init():
    command = sys.argv[1]

    if command == "parse":
        inputFolder = "./"
        outputFile = "output"
        markovOrder = 1
        parseFor = "pitch"
        for i in range(2, len(sys.argv)):
            if "input" in sys.argv[i]:
                inputFolder = sys.argv[i].split("=")[1]
            elif "output" in sys.argv[i]:
                outputFile = sys.argv[i].split("=")[1]
            elif "order" in sys.argv[i]:
                markovOrder = sys.argv[i].split("=")[1]
            elif "parse" in sys.argv[i]:
                parseFor = sys.argv[i].split("=")[1]
            else:
                print "ERROR: %s isn't a argument" % sys.argv[i].split("=")[0]
        parseMidis( inputFolder, outputFile, markovOrder, parseFor )

    elif command == "compose":
        rhythmInputFileName = "./input.mid"
        pitchInputFileName = "./input.mid"
        outputFileName = "output.mid"
        length = 120
        for i in range(2, len(sys.argv)):
            if "rInput" in sys.argv[i]:
                rhythmInputFileName = sys.argv[i].split("=")[1]
            elif "pInput" in sys.argv[i]:
                pitchInputFileName = sys.argv[i].split("=")[1]
            elif "output" in sys.argv[i]:
                outputFileName = sys.argv[i].split("=")[1]
            elif "length" in sys.argv[i]:
                length = sys.argv[i].split("=")[1]
            else:
                print "ERROR: %s isn't a argument" % sys.argv[i].split("=")[0]
        compose(pitchInputFileName, rhythmInputFileName, outputFileName, length)

    else:
        print "ERROR: %s isn't a command" % command

init()
