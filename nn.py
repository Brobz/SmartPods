import random, math, copy

class NN(object):

    """
    >> Layers:
    -- [ [0, 0, 0, 0], [4, 4, 4, -1], [4, 4, -1], [3, 3] ]
    >> Each array is a layer;
    >> Each number is the number of weights attached to this neuron;
    >> 0 means none, -1 means bias neuron (constant)
        -- Bias neurons must always be placed as the last neuron of a layer


    nn = NN([ [0, 0, 0, 0], [4, 4, 4, -1], [4, 4, -1], [3, 3] ])

    #print nn.neurons
    #print nn.weights

    print nn.feedForward([1, 1, 1, 1])

    """

    def __init__(self, layers):
        self.layers  = layers

        self.initNeurons()
        self.initWeights()

    def sigmoid(self, x):
        if x > 700:
            x = 700
        if x < -700:
            x = -700
        return 1 / (1 + math.exp(-x))

    def sigmoid_p(self, x):
        return sigmoid(x) * (1 - sigmoid(x))

    def initNeurons(self):
        self.neurons = []
        for l in xrange(len(self.layers)):
            self.neurons.append([])
            for n in self.layers[l]:
                self.neurons[l].append(0)

    def initWeights(self):
        self.weights = []
        for l in xrange(len(self.layers)):
            self.weights.append([])
            for n in xrange(len(self.layers[l])):
                if self.layers[l][n] == 0:
                    continue
                self.weights[l].append([])
                if self.layers[l][n] < 0:
                    continue
                for w in xrange(self.layers[l][n]):
                    self.weights[l][n].append(random.random())

        for l in self.weights:
            if not len(l):
                self.weights.remove(l)

    def feedForward(self, inputs):
        for i in xrange(len(inputs)):
            self.neurons[0][i] = inputs[i]

        for l in xrange(1, len(self.neurons)):
            for n in xrange(len(self.neurons[l])):
                value = 0
                for pn in xrange(len(self.neurons[l - 1])):
                    if not len(self.weights[l - 1][n]):
                        value += self.neurons[l - 1][len(self.neurons[l - 1]) - 1]
                        break

                    value += self.weights[l - 1][n][pn] * self.neurons[l - 1][pn]

                self.neurons[l][n] = self.sigmoid(value)
                #print self.neurons

        return self.neurons[len(self.neurons) - 1]
