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

    fashion_mnist = keras.datasets.fashion_mnist
    (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

    print(X_train_full.shape)

    X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
    y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
    X_test = X_test[:1000] / 255.0

    # use training data for training and
    tData = X_train_full [:1000] / 255.0
    trainData = tData.tolist()

    #Convert output to fitting format
    outputIn = y_train_full.tolist()
    output = []

    for index in range(0,len(outputIn)):
        if index >= 1000:
            break
        outLine = [0,0,0,0,0,0,0,0,0,0]
        outLine[outputIn[index]] = 1
        output.append(outLine)

    #print(output[0])
    print(len(output))


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

    conv = CONVLayer(matrix=[[-1,-1,-1,-1],[-1,2,2,-1],[-1,2,2,-1],[-1,-1,-1,-1]], stride=1, padding=None)
    pol = PoolLayer(function=Functions.max, poolSize=4, stride=2)
    conv2 = CONVLayer(matrix=[[-1,-1,-1],[-1,2,-1],[-1,-1,-1]], stride=1, padding=None)
    pol2 = PoolLayer(function=Functions.max, poolSize=3, stride=2)
    flat = FlattenLayer()
    den1 = Layer(count=50, function=Functions.tanh)
    den2 = Layer(count=30, function=Functions.tanh)
    den3 = Layer(count=10, function=Functions.tanh, isOutput=True)
    soft = SoftMaxLayer()
    model = SeqModel([conv, pol, conv2, pol2, flat, den1, den2, den3, soft],False)




    model.train(input=trainData, output=output, errorFunc=Functions.halfsquareError, learningRate=0.1, epochs=5)


    #saveModel(model, "current_model.json")

    #print(model.getStructure())

    #test values
    xTest = X_test.tolist()

    #output
    outputTestIn = y_test.tolist()
    output = []

    for index in range(0,len(outputTestIn)):
        if index >= 1000:
            break
        outLine = [0,0,0,0,0,0,0,0,0,0]
        outLine[outputTestIn[index]] = 1
        output.append(outLine)

    errorCount= 0
    for ind in range(0, len(output)):
        print(f"Expected: {output[ind]}")
        result = model.act(xTest[ind])
        print(result)
        index = result.index(max(result))
        print(f"Output on Index: {output[ind][index]}")
        if output[ind][index] != 1:
            errorCount += 1

    print(errorCount)



main()