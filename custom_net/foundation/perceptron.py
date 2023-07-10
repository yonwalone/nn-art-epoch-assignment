import random as rnd
import numpy as np
import math

from foundation.enums import Functions

class Perceptron:

    def __init__(self, func, weights = None) -> None:
        """
        Initialize perceptron.

        Args:
            - function (Functions): activation functions for percepton
            - weights (1dim Array): Initial weights for inputs of percepton
        """
        self.func = func
        self.weights = weights

        self.sum = 0
        self.out = None
        return
    
    def act(self, inputs):
        """
        Predict based on inputs and return responses

        Args:
            - inputs (Array): Input values for percepton

        Return:
            - outputs (Int): output of percepton
        """

        # Initally create weights if there are none
        if self.weights == None:
            self.weights = []
            for input in inputs:
                self.weights.append(rnd.random())
        
        if len(self.weights) != len(inputs):
            raise Exception("Length of weights must be equal to length of inputs")
        
        self.inputs = inputs

        # Get Sum of inputs
        self.sum = 0
        for index in range(0, len(self.weights)):
            self.sum += inputs[index] * self.weights[index]

        self.sum = self.sum / len(self.weights) # TODO: Might delete


        # Activation Function
        if self.func == Functions.heaviside:
            if self.sum < 0:
                self.out = 0
                return 0
            else:
                self.out = 1
                return 1
        elif self.func == Functions.sgn:
            if self.sum < 0:
                self.out = -1
                return -1
            if self.sum == 0:
                self.out = 0
                return 0
            self.out = 1
            return 1
        elif self.func == Functions.tanh:
            self.out = np.tanh(self.sum)
            return self.out   
        elif self.func == Functions.reLu:
            if self.sum > 0:
                self.out = self.sum
                return self.out
            self.out = 0
            return 0
        elif self.func == Functions.no:
            self.out = self.sum
            return self.out
        elif self.func == Functions.leakyReLU:
            if self.sum > 0:
                self.out = self.sum
                return self.out
            self.out = 0.2 * self.sum
            return self.out
        elif self.func == Functions.elu:
            if self.sum > 0:
                self.out = self.sum
                return self.out
            self.out = math.exp(self.sum) -1
            return self.out 
        else:
            raise Exception("Use valid activation function")
        
    def handleErrorOutput(self, target, errorFunc, learningRate):
        """
        Handle target, calculate output error, adapt weights, calculate and propagate error per input

        Params:
            -  target: expected output at last layer
            -  errorFunc: error function to calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - (1dim Array): error per input

        """
       
        # Get error per output
        if errorFunc == Functions.halfsquareError:
            errorFromOut = -(target -self.out)

        return self.handleGeneralError(learningRate=learningRate, errorOut=errorFromOut)
         
    
    def handleError(self, errors, learningRate):
        """
        Handle errors, adapt weights, calculate and propagate error per input

        Params:
            -  errors (1dim Array): errors from lower layer from this percepton
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - (1dim Array): error per input

        """
        
        #d E (total) / d out (of current percepton)
        errorOut = 0
        for error in errors:
            errorOut += error
        
        return self.handleGeneralError(learningRate=learningRate, errorOut=errorOut)
    
    def handleGeneralError(self, learningRate, errorOut):
        """
        Handle output error, adapt weights, calculate and propagate error per input

        Params:
            -  learningRate (Float): Factor how strong weights are changed based on error
            -  errorOut: Output error that should be handled

        Return:
            - errorListSorted (1dim Array): error per input

        """

        # Get error from activaton function
        if self.func == Functions.tanh:
            # out = tanh(sum)
            # d out / d net = 1 - tanh(sum)^2
            errorChangeThroughFunction = 1- (np.tanh(self.sum) * np.tanh(self.sum))
        elif self.func == Functions.reLu:
            if self.sum >= 0:
                errorChangeThroughFunction = 1
            else:
                errorChangeThroughFunction = 0
            
        elif self.func == Functions.no:
            errorChangeThroughFunction = 1
            
        elif self.func == Functions.leakyReLU:
            if self.sum >= 0:
                errorChangeThroughFunction = 1
            else:
                errorChangeThroughFunction = 0.2

        elif self.func == Functions.elu:
            if self.sum > 0:
                errorChangeThroughFunction = 1
            else:
                errorChangeThroughFunction = math.exp(self.sum)

        errorChangeThroughFunction *= len(self.weights) #TODO: Might delete

        #d Error / d Net = 
        errorAfterSum = errorOut * errorChangeThroughFunction

        listOfErrorPerPerceptron = []

        for index in range(0, len(self.weights)):
            inputOfWeight = self.inputs[index]

            #d Error / d Weight = errorFromOut * errorFromNet * inputOfWeight
            errorFromWeight = errorAfterSum * inputOfWeight
            
            # Change weights based on learning rate and error
            self.weights[index] -= learningRate * errorFromWeight

            listOfErrorPerPerceptron.append(errorAfterSum * self.weights[index])

        return listOfErrorPerPerceptron

    def getWeights(self):
        """
        Get weights of perceptons

        Returns:
        - weights
        """
        return self.weights
