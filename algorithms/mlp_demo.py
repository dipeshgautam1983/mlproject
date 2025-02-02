from math import exp
from random import seed
from random import random


# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    #hidden_layer = [{'weights': [random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]

    hidden_layer = [{'weights':[0.13436424411240122, 0.8474337369372327,0.763774618976614]},{'weights':[0.2550690257394217, 0.49543508709194095, 0.4494910647887381]}]

    # print("H_layer: ",hidden_layer)
    network.append(hidden_layer)
    #output_layer = [{'weights': [random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    output_layer = [{'weights':[0.651592972722763, 0.7887233511355132,0.0938595867742349]},{'weights':[0.02834747652200631, 0.8357651039198697, 0.43276706790505337]}]
    # print("OP_layer: ", output_layer)
    network.append(output_layer)
    return network


# Calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation


# Transfer neuron activation
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))


# Forward propagate input to a network output
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs


# Calculate the derivative of an neuron output
def transfer_derivative(output):
    return output * (1.0 - output)

#print layers info
import numpy as np
def print_layer(layer,id):
    print("======Layer: {} ===========".format(id+1))
    wt= list()
    bias = list()
    deltas = list()
    activations = list()
    for neuron in layer:

        wt.append(neuron['weights'][:-1])

        bias.append(neuron["weights"][-1:])

        activations.append(neuron["output"])

        deltas.append(neuron['delta'])

    # print weights
    print("---weights---")
    print(np.array(wt))
    # print bias
    print("---bias---")
    print(np.array(bias).ravel())
    # print activations
    print("---activations---")
    print(np.array(activations))
    # print deltas
    print("---deltas---")
    print(np.array(deltas))

# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

        #print layer info
        print_layer(layer,i)


# Update network weights with error
def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
            neuron['weights'][-1] += l_rate * neuron['delta']


# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        print("+++++++++++++++++EPOCH++++++++++++++++++++++++++++")
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            #print("row[-1]: {} value: {}".format(row[-1],expected[row[-1]]))
            sum_error += sum([(expected[i] - outputs[i]) ** 2 for i in range(len(expected))])
            print("--------------------row-------------------")
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        # print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))


# Test training backprop algorithm
seed(1)
dataset = [[2.7810836, 2.550537003, 0],
           [1.465489372, 2.362125076, 0],
           [3.396561688, 4.400293529, 0],
           [1.38807019, 1.850220317, 0],
           [3.06407232, 3.005305973, 0],
           [7.627531214, 2.759262235, 1],
           [5.332441248, 2.088626775, 1],
           [6.922596716, 1.77106367, 1],
           [8.675418651, -0.242068655, 1],
           [7.673756466, 3.508563011, 1]]
n_inputs = len(dataset[0]) - 1
n_outputs = len(set([row[-1] for row in dataset]))
network = initialize_network(n_inputs, 2, n_outputs)
train_network(network, dataset, 0.5, 20, n_outputs)
for layer in network:
    print(layer)
