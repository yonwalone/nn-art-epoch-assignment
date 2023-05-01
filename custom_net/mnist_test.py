import numpy as np
from tensorflow import keras

from foundation.enums import Functions, TestTypes, PaddingType
from layer.layer import Layer
from layer.flatten_layer import FlattenLayer
from layer.softmax_layer import SoftMaxLayer
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from model import SeqModel
from load_save_model import saveModel, readModelFromStorage

def main():

    # Get Fashion Data
    fashion_mnist = keras.datasets.fashion_mnist
    (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

    # Settings and Analytics
    supportedClasses = 10
    trainAnalyze = [0,0,0,0,0,0,0,0,0,0]
    testAnalyze = [0,0,0,0,0,0,0,0,0,0]

  
    ### Prepare Test Data

    numberOfTrainigData = 40000
    tData = X_train_full [:numberOfTrainigData] / 255.0 *2 -0.5
    trainData = tData.tolist()

    #Convert output to fitting format
    outputIn = y_train_full.tolist()

    # Filter in and output for supportedClasses
    output = []
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


    ### Create Model

    #conv = CONVLayer(matrix=[[-1,-1,-1,-1],[-1,2,2,-1],[-1,2,2,-1],[-1,-1,-1,-1]], stride=1, padding=None)
    conv1 = CONVLayer(matrix= 2, stride=2, padding=None)
    pol1 = PoolLayer(function=Functions.max, poolSize=2, stride=1)
    conv = CONVLayer(matrix= 2, stride=2, padding=PaddingType.valid)
    pol = PoolLayer(function=Functions.max, poolSize=2, stride=2)
    #conv = CONVLayer(matrix=[[-1,-1,-1],[-1,2,-1],[-1,-1,-1]], stride=1, padding=None)
    #pol = PoolLayer(function=Functions.max, poolSize=3, stride=2)
    flat = FlattenLayer()
    den1 = Layer(count=10, function=Functions.tanh)
    #den2 = Layer(count=30, function=Functions.tanh)
    #den3 = Layer(count=10, function=Functions.tanh, isOutput=True)
    den3 = Layer(count=supportedClasses, function=Functions.tanh, isOutput=True)
    soft = SoftMaxLayer()
    #model = SeqModel([conv, pol, flat, den1, den2, den3, soft],False)
    #model = SeqModel([conv1, pol1, conv, pol, flat, den1, den3, soft])
    model = SeqModel([conv, pol, flat, den1, den3, soft])
    #model = SeqModel([flat, den1, den3, soft])


    ### Train Model

    model.train(input=trainData, output=output, errorFunc=Functions.halfsquareError, learningRate=0.01, epochs=1)

    #saveModel(model, "current_model.json")

    ### Prepare Test values

    numberOfTestData = 10000
    X_test = X_test[:numberOfTestData] / 255.0 * 2 - 0.5
    xTest = X_test.tolist()

    #Convert output to fitting format
    outputTestIn = y_test.tolist()

    # Filter in and output for supportedClasses
    output = []
    removeArray =[]
    for index in range(0,len(outputTestIn)):
        if index >= numberOfTestData:
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

    for index in range(0, len(removeArray)):
        xTest.pop(removeArray[index] - index)
    

    ### Test Model with test Data

    accuracy = model.test(xTest, output, TestTypes.biggestPredictionOn1Position)

    # Print result and analytics
    print(f"Length Trainingvalues: {len(trainData)}")
    print(f"Distribution Expected Outputs: {trainAnalyze}")

    print(f"Length Testvalues: {len(xTest)}")
    print(f"Distribution Expected Outputs: {testAnalyze}")
   
    print(f"Accuracy: {accuracy}")

main()