import numpy as np
import tensorflow as tf
from tensorflow import keras

from layer.layer import Layer
from layer.flatten_layer import FlattenLayer
from layer.softmax_layer import SoftMaxLayer
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from foundation.enums import Functions
from model import SeqModel
from load_save_model import saveModel, readModelFromStorage

def main():

    #Notes:
    # eventuell macht ein Bias pro Output einen Unterschied?

    fashion_mnist = keras.datasets.fashion_mnist
    (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

    X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0 * 2 -0.5
    y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
    X_test = X_test[:2000] / 255.0 * 2 - 0.5

    # use training data for training and
    numberOfTrainigData = 10000
    tData = X_train_full [:numberOfTrainigData] / 255.0 *2 -0.5
    trainData = tData.tolist()

    #Convert output to fitting format
    outputIn = y_train_full.tolist()
    output = []

    supportedClasses = 2

    trainAnalyze = [0,0,0,0,0,0,0,0,0,0]
    testAnalyze = [0,0,0,0,0,0,0,0,0,0]

    removeArray = []
    for index in range(0,len(outputIn)):
        if index >= numberOfTrainigData:
            break
        if outputIn[index] <  supportedClasses:
            outLine = []
            for nullIndex in range(0, supportedClasses):
                outLine.append(0)
            outLine[outputIn[index]] = 1
            trainAnalyze[outputIn[index]] += 1
            output.append(outLine)
        else:
            removeArray.append(index)

    for index in range(0, len(removeArray)):
        trainData.pop(removeArray[index] - index)

    print(len(output))
    #print(output)
    print(len(trainData))

    

    #model = keras.models.Sequential()
    #model.add(keras.layers.Flatten(input_shape=[28,28]))
    #model.add(keras.layers.Dense(300, activation="relu"))
    #model.add(keras.layers.Dense(100, activation="relu"))
    #model.add(keras.layers.Dense(10, activation="softmax"))
    
    #flat = FlattenLayer()
    #middleLayer = Layer(count=300, function=Functions.reLu)
    #middle2Layer = Layer(count=100, function=Functions.reLu)
    #outputLayer = Layer(count=10, function=Functions.reLu, isOutput=True)
    #soft = SoftMaxLayer()
    #model = SeqModel([flat, middleLayer, middle2Layer, outputLayer, soft], False)

    #conv = CONVLayer(matrix=[[-1,-1,-1,-1],[-1,2,2,-1],[-1,2,2,-1],[-1,-1,-1,-1]], stride=1, padding=None)
    #pol = PoolLayer(function=Functions.max, poolSize=4, stride=2)
    #conv = CONVLayer(matrix=[[-1,-1,-1],[-1,2,-1],[-1,-1,-1]], stride=1, padding=None)
    #pol = PoolLayer(function=Functions.max, poolSize=3, stride=2)
    flat = FlattenLayer()
    den1 = Layer(count=10, function=Functions.tanh)
    #den2 = Layer(count=30, function=Functions.tanh)
    #den3 = Layer(count=10, function=Functions.tanh, isOutput=True)
    den3 = Layer(count=2, function=Functions.tanh, isOutput=True)
    soft = SoftMaxLayer()
    #model = SeqModel([conv, pol, flat, den1, den2, den3, soft],False)
    model = SeqModel([flat, den1, den3, soft],False)


    model.train(input=trainData, output=output, errorFunc=Functions.halfsquareError, learningRate=0.01, epochs=1)

    
    #print(f"Weights in Conv: {conv.getWeights()}")

    #saveModel(model, "current_model.json")

    #test values
    xTest = X_test.tolist()

    #output
    outputTestIn = y_test.tolist()
    output = []
    removeArray =[]

    for index in range(0,len(outputTestIn)):
        if index >= 2000:
            break
        if outputTestIn[index] < supportedClasses:
            outLine = []
            for nullIndex in range(0, supportedClasses):
                outLine.append(0)
            outLine[outputTestIn[index]] = 1
            testAnalyze[outputTestIn[index]] += 1
            output.append(outLine)
        else:
            removeArray.append(index)

    print(len(output))
    for index in range(0, len(removeArray)):
        xTest.pop(removeArray[index] - index)

    print(len(xTest))
    

    errorCount= 0
    firstIndex = 0
    secIndex = 0
    for ind in range(0, len(output)):
        print(f"Expected: {output[ind]}")
        result = model.act(xTest[ind])
        print(result)
        index = result.index(max(result))
        print(f"Output on Index: {output[ind][index]}")
        if index == 0:
            firstIndex +=1
        if index == 1:
            secIndex +=1
        
        if output[ind][index] != 1:
            errorCount += 1

    print(len(trainData))
    print(len(output))
    print(f"Errors: {errorCount}")
    print(f"FirstIndex: {firstIndex}")
    print(f"SecondIndex: {secIndex}")
    print(trainAnalyze)
    print(testAnalyze)
    return
    print(f"Weights in Conv: {conv.getWeights()}")


main()