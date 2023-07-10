import numpy as np
from tensorflow import keras

from foundation.enums import Functions, TestTypes, PaddingType
from foundation.helper import preprocessImages
from layer.layer import Layer
from layer.flatten_layer import FlattenLayer
from layer.softmax_layer import SoftMaxLayer
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from model.model import SeqModel
from model.load_save_model import saveModel, readModelFromStorage

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
    
    trainData= preprocessImages(trainData)

    ### Create Model

    conv = CONVLayer(matrix= 2, stride=2, padding=PaddingType.valid)
    pol = PoolLayer(function=Functions.max, poolSize=2, stride=2)
    flat = FlattenLayer()
    den1 = Layer(count=10, function=Functions.tanh)
    den2 = Layer(count=supportedClasses, function=Functions.tanh, isOutput=True)
    soft = SoftMaxLayer()
   
    model = SeqModel([conv, pol, flat, den1, den2, soft])

    ### Train Model

    model.train(input=trainData, output=output, errorFunc=Functions.halfsquareError, learningRate=0.01, epochs=1)

    saveModel(model, "current_model.json")

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
    
    xTest = preprocessImages(xTest)

    ### Test Model with test Data

    accuracy, statistic = model.test(xTest, output, TestTypes.biggestPredictionOn1Position)

    # Print result and analytics
    print(f"Length Trainingvalues: {len(trainData)}")
    print(f"Distribution Expected Outputs: {trainAnalyze}")

    print(f"Length Testvalues: {len(xTest)}")
    print(f"Distribution Expected Outputs: {testAnalyze}")
   
    print(f"Accuracy: {accuracy}")

main()