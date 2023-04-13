from layer.layer import Layer
from foundation.functions import Functions
from foundation.neuron import Percepton
from layer.inputLayer import InputLayer
from model import SequentialModel
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from load_save_model import saveModel, readModelFromStorage


def getInclusiveOrModel():
    # Layer(count=1, function=Functions.sgn, initialWeights=[[1,1]], biasValue=0, isOutput=True)
     Percepton(Functions.tanh, [0.6,1.4,1])

def inclusiveOr(a,b):
    outputLayer = getInclusiveOrModel()
    print(outputLayer.act([a,b]))

def myAnd(a,b):
    biasIn = -2
    outputLayer = Layer(count=1, function=Functions.heaviside, initialWeights=[[1, 1, 1]], biasValue=1, isOutput=True)
    print(outputLayer.act([a,b,biasIn]))

def getXORModell():
    middleLayer = Layer(count=2, function=Functions.heaviside, initialWeights=[[1,1,-1.5],[1,1,-0.5]], biasValue= 1)
    outputLayer = Layer(count=1, function=Functions.heaviside, initialWeights=[[-1, 1, -0.5]], biasValue= 1, isOutput= True)
    return SequentialModel([middleLayer, outputLayer])

def getXORModellSgn():
    middleLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[1,1,-1.5],[1,1,-0.5]], biasValue= 1)
    outputLayer = Layer(count=1, function=Functions.tanh, initialWeights=[[-1, 1, -0.5]], biasValue= 1, isOutput= True)
    return SequentialModel([middleLayer, outputLayer])


def xOR(a,b):
    bias = 1
    inputLayer = InputLayer([a,b], bias)
    model = getXORModellSgn()
    print(model.act(inputLayer.act()))


def trainPercepton(model,input, output, errorFunc, learningRate, epochs):
    if len(input) != len(output):
        raise Exception("Len of inputs must equal the length of expected outputs")
    
    for epochIndex in range(0, epochs):
        for indexOutput in range(0, len(output)):
            model.react(input[indexOutput])
            model.handleErrorOutput(target=output[indexOutput], errorFunc=errorFunc, learningRate=learningRate)
            model.printWeights()

    return model

def trainSequentialModel(model, input, output, errorFunc, learningRate, epochs):
    if len(input) != len(output):
        raise Exception("Len of inputs must equal the length of expected outputs")
    
    for epochIndex in range(0, epochs):
        for indexOutput in range(0, len(output)):
            #print(f"Ergebnis des Netz Ausfuhrens: {model.act(input[indexOutput])}")
            model.act(input[indexOutput])
            model.handleError(targets=output[indexOutput], errorFunc=errorFunc, learningRate=learningRate)
            #print(f"Gewichte: {model.getWeights()}")

    print(f"Gewichte: {model.getWeights()}")
    return model 

def main():

    

    conv = CONVLayer(matrix=[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]], stride=2, padding=True)
    pol = PoolLayer(function=Functions.max, toList=True)
    middleLayer = Layer(count=4, function=Functions.tanh, initialWeights=[[1,1,1,1,-1.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5]])
    #middleLayer2 = Layer(count=3, function=Functions.tanh, initialWeights=[[1,1,1,1,-1.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5]])
    #middleLayer = Layer(count=4, function=Functions.tanh, initialWeights=[[1,1,1,-1.5],[1,1,1,-0.5],[1,1,1,-0.5],[1,1,1,-0.5]])
    #outputLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[-1, 1, 1, -0.5],[-1, 1, 1, -0.5]], isOutput= True)
    outputLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[-1, 1, 1, 1, -0.5],[-1, 1, 1, 1, -0.5]], isOutput= True)

    model =  SequentialModel([conv, pol, middleLayer, outputLayer], False)

    #print(model.act([[1,1,1],[1,1,1],[0,0,0]]))
    print(model.act([[1,1,1],[0,0,0],[0,0,0]]))

    input = [[[1,1,1],[0,0,0],[0,0,0]],
             [[1,1,1],[1,1,1],[0,0,0]],
             [[1,1,1],[1,1,1],[1,1,1]],
             [[0,0,0],[1,1,1],[1,1,1]],
             [[0,0,0],[0,0,0],[1,1,1]],
             [[1,1,1],[0,0,1],[0,0,0]],
             [[0,0,0],[0,0,1],[1,1,1]],
             ]
    
    output = [[1,-1],
              [1,-1],
              [1,1],
              [-1,1],
              [-1,1],
              [1,-1],
              [-1,1],
              ]

    for index in range(0, len(input)):
        print(model.act(input[index]))

    model = trainSequentialModel(model=model,input=input, output=output, errorFunc=Functions.halfsquareError,learningRate=0.1, epochs=1)

    for index in range(0, len(input)):
        print(model.act(input[index]))

    return
    output = [[1,0],
              [1,0],
              [1,1],
              [0,1],
              [0,1],
              [1,0],
              [0,1],
              ]

    layer = CONVLayer([])
    layer.act(image=[[1,1,1],[1,1,1],[1,1,1]], padding=True, stride=2)

    pol = PoolLayer(function=Functions.avg)
    print(pol.act([[-1, -3, -1], [-3, 0, -3], [-1, -3, -1]]))

    middleLayer1 = Layer(count=3, function=Functions.tanh, initialWeights=[[1,1,1,-1.5],[1,1,1,-0.5],[1,1,1,-0.5]])
    middleLayer2 = Layer(count=2, function=Functions.tanh, initialWeights=[[1,1,1,-1.5],[1,1,1,-0.5]])
    outputLayer = Layer(count=1, function=Functions.tanh, initialWeights=[[-1, 1, -0.5]], isOutput= True)
    model =  SequentialModel([middleLayer1, middleLayer2, outputLayer])

    #Build in check if count of input values are correct!

    print(model.act([0,0,0]))
    print(model.act([0,0,1]))
    print(model.act([0,1,0]))
    print(model.act([0,1,1]))
    print(model.act([1,0,0]))
    print(model.act([1,0,1]))
    print(model.act([1,1,0]))
    print(model.act([1,1,1]))

    epochs = 60
    # Ziel A u. (B o. C)
    input = [[0,0,0], [0,0,1], [0,1,0], [0,1,1],
             [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
    output = [[0],[0],[0],[0],
              [0],[1],[1],[1]]
    errorFunc = Functions.halfsquareError
    lerningRate = 0.1
    print(f"First values: {input[0]}")
    model = trainSequentialModel(model=model, input=input, output=output, errorFunc=errorFunc, learningRate=lerningRate, epochs=epochs)

    saveModel(model,'current_model.json')

    print(model.act([0,0,0]))
    print(model.act([0,0,1]))
    print(model.act([0,1,0]))
    print(model.act([0,1,1]))
    print(model.act([1,0,0]))
    print(model.act([1,0,1]))
    print(model.act([1,1,0]))
    print(model.act([1,1,1]))

    model = readModelFromStorage('current_model.json')

    print(model.act([0,0,0]))
    print(model.act([0,0,1]))
    print(model.act([0,1,0]))
    print(model.act([0,1,1]))
    print(model.act([1,0,0]))
    print(model.act([1,0,1]))
    print(model.act([1,1,0]))
    print(model.act([1,1,1]))


    return
    epochs = 100
    input = [[0,0,1], [1,0,1], [0,1,1], [1,1,1]]
    output = [[0],[0],[0],[1]]
    errorFunc = Functions.halfsquareError
    lerningRate = 0.1
    model = getXORModellSgn()
    print("Result:")
    print(model.act([0,0,1]))
    print(model.act([1,0,1]))
    print(model.act([0,1,1]))
    print(model.act([1,1,1]))


    model = trainSequentialModel(model=model, input=input, output=output, errorFunc=errorFunc, learningRate=lerningRate, epochs=epochs)

    print("Result:")
    print(model.act([0,0,1]))
    print(model.act([1,0,1]))
    print(model.act([0,1,1]))
    print(model.act([1,1,1]))


    return

    # Get errors for one layer
    model = Layer(count=2, function=Functions.tanh, initialWeights=[[1,1,0],[1,0,0]], biasValue=1, isOutput=True)
    model.act([0,1,1])
    model.handleError([1,1], Functions.halfsquareError, 0.1)


    return
    model = Percepton(func=Functions.tanh, weights=[1,1,0])

    epochs = 40
    input = [[0,0,1], [1,0,1], [0,1,1], [1,1,1]]
    output = [0,0,0,1]
    errorFunc = Functions.halfsquareError
    lerningRate = 0.1

    model = trainPercepton(model=model, input=input, output=output, errorFunc=errorFunc, learningRate=lerningRate, epochs=epochs)

    print("Result:")
    print(model.react([0,0,1]))
    print(model.react([1,0,1]))
    print(model.react([0,1,1]))
    print(model.react([1,1,1]))

    
    return
    for index in range(0,epochs):
        print("Start Run")
        print(model.react([0,0,1]))
        model.handleError(target=0, errorFunc=Functions.halfsquareError, learningRate=0.1)
        model.printWeights()
        print(model.react([1,0,1]))
        model.handleError(target=0, errorFunc=Functions.halfsquareError, learningRate=0.1)
        model.printWeights()
        print(model.react([0,1,1]))
        model.handleError(target=0, errorFunc=Functions.halfsquareError, learningRate=0.1)
        model.printWeights()
        print(model.react([1,1,1]))
        model.handleError(target=1, errorFunc=Functions.halfsquareError, learningRate=0.1)
        model.printWeights()

    print("Result:")
    print(model.react([0,0,1]))
    print(model.react([1,0,1]))
    print(model.react([0,1,1]))
    print(model.react([1,1,1]))


    return
    xOR(0,0)
    xOR(1,0)
    xOR(0,1)
    xOR(1,1)


    #Versuch: XOR Modell -> And
    model = getXORModell()
    bias = 1
    for index in range(0,1):
        inputLayer = InputLayer([0,0], bias)
        result = model.act(inputLayer.act())
        print(getError(result[0], 0))

        inputLayer = InputLayer([0,1], bias)
        result = model.act(inputLayer.act())
        print(getError(result[0], 0))

        inputLayer = InputLayer([1,0], bias)
        result = model.act(inputLayer.act())
        print(getError(result[0], 0))

        inputLayer = InputLayer([1,1], bias)
        result = model.act(inputLayer.act())
        print(getError(result[0], 1))

        

    #inclusiveOr(0,0)
    #inclusiveOr(0,1)
    #inclusiveOr(1,0)
    #inclusiveOr(1,1)

main()


def old_train_percepton():
    model = Percepton(func=Functions.tanh, weights=[1,1,0])
    
    epochs = 40
    input = [[0,0,1], [1,0,1], [0,1,1], [1,1,1]]
    output = [0,0,0,1]
    errorFunc = Functions.halfsquareError
    lerningRate = 0.1

    model = trainPercepton(model=model, input=input, output=output, errorFunc=errorFunc, learningRate=lerningRate, epochs=epochs)

    print("Result:")
    print(model.react([0,0,1]))
    print(model.react([1,0,1]))
    print(model.react([0,1,1]))
    print(model.react([1,1,1]))