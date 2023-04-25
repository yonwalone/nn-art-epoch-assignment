from layer.layer import Layer
from foundation.enums import Functions, PaddingType
from foundation.percepton import Percepton
from model import SeqModel
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from layer.softmax_layer import SoftMaxLayer
from load_save_model import saveModel, readModelFromStorage
import numpy as np


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
    return SeqModel([middleLayer, outputLayer])

def getXORModellSgn():
    middleLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[1,1,-1.5],[1,1,-0.5]], biasValue= 1)
    outputLayer = Layer(count=1, function=Functions.tanh, initialWeights=[[-1, 1, -0.5]], biasValue= 1, isOutput= True)
    return SeqModel([middleLayer, outputLayer])


def xOR(a,b):
    model = getXORModellSgn()
    print(model.act([a,b]))


def trainPercepton(model,input, output, errorFunc, learningRate, epochs):
    if len(input) != len(output):
        raise Exception("Len of inputs must equal the length of expected outputs")
    
    for epochIndex in range(0, epochs):
        for indexOutput in range(0, len(output)):
            model.react(input[indexOutput])
            model.handleErrorOutput(target=output[indexOutput], errorFunc=errorFunc, learningRate=learningRate)
            model.printWeights()

    return model


def main():

    conv1 = CONVLayer(matrix=[[-1,-1,-1],[-1, 2,-1],[-1,-1,-1]], stride=1, padding=PaddingType.same)
    pol1 = PoolLayer(poolSize=2, function=Functions.max, toList=False)
    conv = CONVLayer(matrix=[[-1,-1,-1],[-1, 2,-1],[-1,-1,-1]], stride=1, padding=PaddingType.same)
    pol = PoolLayer(poolSize=2, function=Functions.max, toList=True)
    middleLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[1,1,1,1,-1.5],[1,1,1,1, -0.5]])
    outputLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[1, 1, -0.5],[-1, -1, 0.5]], isOutput= True)
    exc = SoftMaxLayer()

    model =  SeqModel([conv1, pol1, conv, pol, middleLayer, outputLayer, exc], False)

    #model = readModelFromStorage("current_model.json")

    input = []
    output = []

    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                for l in [-1,1]:
                    for m in [-1,1]:
                        for n in [-1,1]:
                            for o in [-1,1]:
                                for p in [-1,1]:
                                    for q in [-1,1]:
                                        input.append( [[i, j, k, i], [l, m, n, i], [o, p, q, i], [j, k, i, l]] )
    
    for matrix in input:

        if matrix[0] == [1,1,1,1]:
            output.append([1,0])
        else:
            output.append([0,1])


    #input = [[[1,1,1,1],[1,1,-1,1],[-1,1,-1,1],[1,-1,-1,1]]]

    #output = [[1,0]]
    
    

    model.train(input=input, output=output, errorFunc=Functions.halfsquareError, learningRate=0.01, epochs=10)


    #print(conv.getWeights())

    errorCount = 0

    print("Test")
    print(output[511])
    print(model.act(input[511]))

    for index in range(0, len(input)):
        result = model.act(input[index])
        if ((output[index][0] < 0.5  and result[0] < 0.5) or \
           (output[index][0] > 0.5  and result[0] > 0.5) ) and \
           ((output[index][1] < 0.5  and result[1] < 0.5) or \
           (output[index][1] > 0.5  and result[1] > 0.5) ):
            pass
        else:
            #print(f"Expected Output: {output[index]}")
            #print(input[index])
            #print(result)
            errorCount +=1

    print(f"Wrong labled: {errorCount}")


    #saveModel(model, "current_model.json")


    return

    # Correct backpropagation of convolution

    conv = CONVLayer(matrix=[[-1,-1,-1],[-1, 2,-1],[-1,-1,-1]], stride=1, padding=PaddingType.same)
    pol = PoolLayer(poolSize=2, function=Functions.max, toList=True)
    middleLayer = Layer(count=4, function=Functions.tanh, initialWeights=[[1,1,1,1,-1.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5]])
    outputLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[1, 1, 1, 1, -0.5],[-1, -1, -1, -1, 0.5]], isOutput= True)
    exc = SoftMaxLayer()

    model =  SeqModel([conv, pol, middleLayer, outputLayer, exc], False)

    input = [[[1,1,1],[0,0,0],[0,0,0]]]

    output = [[1,-1]]

    model.train(input=input, output=output, errorFunc=Functions.halfsquareError, learningRate=0.01, epochs=1)
   


    #Problem verschwindener Gradient

    conv = CONVLayer(matrix=[[-1,-1,-1],[-1, 2,-1],[-1,-1,-1]], stride=1, padding=True)
    pol = PoolLayer(poolSize=2, function=Functions.max, toList=True)
    #middleLayer = Layer(count=4, function=Functions.tanh, initialWeights=[[1,1,1,1,-1.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5]])
    outputLayer = Layer(count=1, function=Functions.tanh, initialWeights=[[1, 1, 1, 1, -0.5]], isOutput= True)

    model =  SeqModel([conv, pol, outputLayer], False)

    input = [[[1,1,1],[0,0,0],[0,0,0]]]

    output = [[1,-1]]

    input = []
    output = []

    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                for l in [-1,1]:
                    for m in [-1,1]:
                        for n in [-1,1]:
                            for o in [-1,1]:
                                for p in [-1,1]:
                                    for q in [-1,1]:
                                        #if i == 0 and j == 1 and k == 0 and l == 1 and m == 1 and n == 1 and o == 0 and p == 1 and q == 0 :
                                        #    print("Index")
                                        #    print(len(output))
                                        #    output.append([1])
                                        #else:
                                        #    output.append([-1])

                                        input.append( [[i, j, k], [l, m, n], [o, p, q]] )

    for matrix in input:
        onesTouching = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    # Überprüfen der Nachbarelemente auf Eins
                    if (i > 0 and matrix[i-1][j] == 1) or \
                        (i < len(matrix)-1 and matrix[i+1][j] == 1) or \
                        (j > 0 and matrix[i][j-1] == 1) or \
                        (j < len(matrix[i])-1 and matrix[i][j+1] == 1):
                            onesTouching +=1

                            #break
            #break # beende alle Schleifen, wenn eine Berührung gefunden wird

        if onesTouching < 5:
            output.append([-1])
        else:
            output.append([1])

        #output.append([onesTouching/9])

    model = trainSeqModel(model=model,input=input, output=output, errorFunc=Functions.halfsquareError,learningRate=0.1, epochs=20)

    print(f"Conv Weights: {conv.getWeights()}")
    print(f"Percepton Weights: {outputLayer.getWeights()}")

    return

    for index in range(0, len(input)):
        print(input[index])
        print(output[index])
        print(model.act(input[index]))

    print(conv.getWeights())

    return

    conv = CONVLayer(matrix=[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]], stride=2, padding=True)
    pol = PoolLayer(function=Functions.max, toList=True)
    middleLayer = Layer(count=4, function=Functions.tanh, initialWeights=[[1,1,1,1,-1.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5],[1,1,1,1,-0.5]])
    outputLayer = Layer(count=2, function=Functions.tanh, initialWeights=[[-1, 1, 1, 1, -0.5],[-1, 1, 1, 1, -0.5]], isOutput= True)

    model =  SeqModel([conv, pol, middleLayer, outputLayer], False)

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
    model =  SeqModel([middleLayer1, middleLayer2, outputLayer])

    #Build in check if count of input values are correct!

    #Train MLP
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
    model = trainSeqModel(model=model, input=input, output=output, errorFunc=errorFunc, learningRate=lerningRate, epochs=epochs)

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


    model = trainSeqModel(model=model, input=input, output=output, errorFunc=errorFunc, learningRate=lerningRate, epochs=epochs)

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