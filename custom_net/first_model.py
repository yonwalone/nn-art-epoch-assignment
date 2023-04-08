from layer.layer import Layer
from foundation.functions import Functions
from layer.inputLayer import InputLayer
from model import SequentialModel


def inclusiveOr(a,b):
    outputLayer = Layer(count=1, function=Functions.sgn, initialWeights=[[1,1]], biasValue=0, isOutput=True)
    print(outputLayer.act([a,b]))

def myAnd(a,b):
    biasIn = -2
    outputLayer = Layer(count=1, function=Functions.heaviside, initialWeights=[[1, 1, 1]], biasValue=1, isOutput=True)
    print(outputLayer.act([a,b,biasIn]))

def xOR(a,b):
    bias = 1
    inputLayer = InputLayer([a,b], bias)
    middleLayer = Layer(count=2, function=Functions.heaviside, initialWeights=[[1,1,-1.5],[1,1,-0.5]], biasValue= 1)
    outputLayer = Layer(count=1, function=Functions.heaviside, initialWeights=[[-1, 1, -0.5]], biasValue= 1, isOutput= True)

    model = SequentialModel([middleLayer, outputLayer])
    print(model.act(inputLayer.act()))

xOR(0,0)
xOR(1,0)
xOR(0,1)
xOR(1,1)
    

#inclusiveOr(0,0)
#inclusiveOr(0,1)
#inclusiveOr(1,0)
#inclusiveOr(1,1)