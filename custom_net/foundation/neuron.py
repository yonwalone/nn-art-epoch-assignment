from foundation.functions import Functions
import numpy as np

class Percepton:

    def __init__(self, func, weights) -> None:
        self.func = func
        self.weights = weights

        self.sum = 0
        self.out = None
        return
    
    def react(self, inputs):
        if len(self.weights) != len(inputs):
            raise Exception("Length of weights must be equal to length of inputs")
        
        self.inputs = inputs

        # Get Sum of inputs
        self.sum = 0
        for index in range(0, len(self.weights)):
            self.sum += inputs[index] * self.weights[index]


        # Activation Function
        if self.func == Functions.heaviside:
            if self.sum < 0:
                self.out = 0
                return 0
            else:
                self.out = 1
                return 1
    
        if self.func == Functions.sgn:
            if self.sum < 0:
                self.out = -1
                return -1
            if self.sum == 0:
                self.out = 0
                return 0
            
            self.out = 1
            return 1
        
        if self.func == Functions.tanh:
            self.out = np.tanh(self.sum)
            return self.out   
        
        if self.func == Functions.reLu:
            if self.sum > 0:
                self.out = self.sum
                return self.out
            self.out = 0
            return 0
        
        raise Exception("Use valid activation function")
        
    def handleErrorOutput(self, target, errorFunc, learningRate):
        # Get error per output
        if errorFunc == Functions.halfsquareError:
            errorFromOut = -(target -self.out)

        return self.handleGeneralError(learningRate=learningRate, errorOut=errorFromOut)
         
    
    def handleError(self, errors, learningRate):
        #d E (total) / d out (of current percepton)
        errorOut = 0
        for index in range(0, len(errors)):
            errorOut += errors[index]
        
        return self.handleGeneralError(learningRate=learningRate, errorOut=errorOut)
    
    def handleGeneralError(self, learningRate, errorOut):
        # Get error from sum
        if self.func == Functions.tanh:
            # out = tanh(sum)
            # d out / d net = 1 - tanh(sum)^2
            errorFromNet = 1- (np.tanh(self.sum) * np.tanh(self.sum))

        #d Error / d Net
        errorPerNet = errorOut * errorFromNet

        listOfErrorPerPerceptron = []

        for index in range(0, len(self.weights)):
            netPerWeight = self.inputs[index]

            #d Error / d Weight = errorFromOut * errorFromNet * netPerWeight
            errorFromWeight = errorOut * errorFromNet * netPerWeight
            
            # Change weights based on learning rate and error
            self.weights[index] -= learningRate * errorFromWeight

            listOfErrorPerPerceptron.append(errorPerNet * self.weights[index])

        return listOfErrorPerPerceptron

    def getWeights(self):
        return self.weights


        


