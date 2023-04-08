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
            #print("Added value")
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
        
        self.out = self.sum
        return self.out
        
    def handleError(self,target, errorFunc, learningRate):
        c = 9

        # Get error per output
        if errorFunc == Functions.halfsquareError:
            errorFromOut = -(target -self.out)
        
        # Get error from sum
        if self.func == Functions.tanh:
            # out = tanh(sum)
            # d out / d net = 1 - tanh(sum)^2
            errorFromNet = 1- (np.tanh(self.sum) * np.tanh(self.sum))

        #print("Fehler:")
        #print(errorFromOut)
        #print(errorFromNet)

        for index in range(0, len(self.weights)):
            #print("Weight geändert")
            netPerWeight = self.inputs[index]
            #print(netPerWeight)

            #d Error / d Weight = errorFromOut * errorFromNet * netPerWeight
            errorFromWeight = errorFromOut * errorFromNet * netPerWeight
            #print(f"ErrorFromWeight of index {index}: {errorFromWeight}")
            self.weights[index] -= learningRate * errorFromWeight
            #print(f"ResultingWeight: {self.weights[index]}")

    def printWeights(self):
        print(f"Weights: {self.weights}")


        


