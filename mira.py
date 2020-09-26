#Sukhmani Choudhry
#Schoud9@emory.edu
# /*THIS  CODE  WAS MY OWN WORK , IT WAS  WRITTEN  WITHOUT  CONSULTING  ANY SOURCES  OUTSIDE  OF  THOSE  APPROVED  BY THE  INSTRUCTOR. _Sukhmani_Choudhry_*/


# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util

PRINT = True


class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter()  # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys()  # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        bestWeights = None
        bestAccuracy = -float("inf")
        bestC = float("inf")

        for C in Cgrid:
            # w is a temp set of weight that we're gonna test against the bestWeights/bestAccuracy using the validationData
            self.weights = util.Counter()
            w = self.weights

            # initialise to all zeros for all labels
            for label in self.legalLabels:
                w[label] = util.Counter()

            # training protocol
            for iteration in range(self.max_iterations):
                print "Starting iteration ", iteration + 1, " for C = ", C

                for i in range(len(trainingData)):
                    # we don't want to modify the actual training data
                    f = trainingData[i].copy()

                    bestScore = -float("inf")
                    bestLabel = None

                    for label in self.legalLabels:
                        score = f * w[label]

                        if score > bestScore:
                            bestScore = score
                            bestLabel = label

                    realLabel = trainingLabels[i]

                    # update w if guess was wrong
                    if realLabel != bestLabel:

                        tau = min(C, ((w[bestLabel] - w[realLabel]) * f + 1.0) / (f * f * 2))  # ((wy'-wy) * f + 1) / (2 * f * f)

                        f.divideAll(1 / tau)

                        w[realLabel] += f
                        w[bestLabel] -= f

                    # test w with validationData
            accuracy = 0
            guesses = self.classify(validationData)

            for i in range(len(guesses)):
                if validationLabels[i] == guesses[i]:
                    accuracy += 1

                # compare w with bestWeights
            if accuracy > bestAccuracy:
                bestWeights = w
                bestAccuracy = accuracy
                bestC = C
            if accuracy == bestAccuracy and C < bestC:
                bestC = C
                bestWeights = w

            # update self.weights to be the best one
        self.weights = bestWeights

    def classify(self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses




