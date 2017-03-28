import random
import json
import ast

class Markov:
    "Class to produce probabilties of next event given previous events"
    def __init__(self, inputFileName=None):
        self.sequenceCounts = {}
        if inputFileName is not None:
            self.readFromFile(inputFileName)

    def readFromFile(self, inputFileName):
        with open(inputFileName, 'r') as f:
            try:
                self.sequenceCounts = json.load(f)
            except ValueError:
                print "ERROR: Reading from file"

    def writeToFile(self, outputFileName):
        with open(outputFileName, 'w') as f:
            json.dump(self.sequenceCounts, f)

    def order(self):
        keys = self.sequenceCounts.keys()
        firstItem = ast.literal_eval(keys[0])
        return len(firstItem)

    def getSequences(self):
        return self.sequenceCounts.keys()

    def push(self, sequence, event):
        sequence = str(sequence)

        #make sure sequence is in ds
        if sequence not in self.sequenceCounts:
            self.sequenceCounts[sequence] = dict()

        #make sure current event for sequence in ds
        if event not in self.sequenceCounts[sequence]:
            self.sequenceCounts[sequence][event] = 1
        else:
            self.sequenceCounts[sequence][event] += 1

    def get(self, sequence):
        sequence = str(sequence)
        probability = self.getProb(sequence)
        if probability is not None:
            randomValue = random.randint(1,1000)
            i = -1
            while randomValue > 0 and i < len(probability)-1:
                i += 1
                randomValue -= probability[i][0] * 1000
            return probability[i][1]
        else:
            return None

    def getProb(self, sequence):
        sequence = str(sequence)
        #Return in format [(prob, event), (0.4, 69)]
        if sequence not in list( self.sequenceCounts.keys() ):
            print "ERROR. No data for that sequence:" + str(sequence)
            return None

        event = self.sequenceCounts[sequence]

        # Get total number of entries for sequence
        totalCount = 0
        for event in self.sequenceCounts[sequence].keys():
            totalCount += self.sequenceCounts[sequence][event]

        #get probabilities
        probabilities = []
        for event in self.sequenceCounts[sequence].keys():
            count = float( self.sequenceCounts[sequence][event] )
            probability = count / totalCount
            probabilities.append( (probability, event) )

        return probabilities
