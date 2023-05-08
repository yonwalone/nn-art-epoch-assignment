import cv2
from tensorflow import keras

from foundation.enums import Functions, PaddingType, TestTypes
from foundation.helper import preprocessImages, printStatistics
from model.model import SeqModel
from model.load_save_model import saveModel, readModelFromStorage
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from layer.flatten_layer import FlattenLayer
from layer.layer import Layer
from layer.softmax_layer import SoftMaxLayer

(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

trainAnalyze = [0,0,0,0,0,0,0,0,0,0]
testAnalyze = [0,0,0,0,0,0,0,0,0,0]

### Prepare training data
numberOfTrainigData = 50000
input = (x_train[:numberOfTrainigData] /255 * 2 -1).tolist()
input = preprocessImages(input)

# Prepare training outputs
outputIn = y_train.tolist()
output = []
for index in range(0,len(outputIn)):
    if index >= numberOfTrainigData:
        break
    if outputIn[index][0] <  10:
        outLine = []
        for nullIndex in range(0, 10):
            outLine.append(0)
        outLine[outputIn[index][0]] = 1
        trainAnalyze[outputIn[index][0]] += 1
        output.append(outLine)

### Create Model

conv = CONVLayer(matrix= 2, stride=2, inputDepth=3, depth=2, padding=PaddingType.valid)
pol = PoolLayer(function=Functions.avg, poolSize=2, stride=2)
flat = FlattenLayer()
den1 = Layer(count=10, function=Functions.tanh)
den3 = Layer(count=10, function=Functions.tanh, isOutput=True)
soft = SoftMaxLayer()
model = SeqModel([conv, pol, flat, den1, den3, soft])

### Train Model

model.train(input=input, output=output, errorFunc=Functions.halfsquareError, learningRate=0.0005, epochs=1)

#model = readModelFromStorage("tmp_model.json")

saveModel(model, "tmp_model.json")

### Prepare test data
numberOfTestData=10000
input = (x_test[:numberOfTestData] /255 * 2 -1).tolist()
input = preprocessImages(input)

# Prepare test outputs
outputIn = y_test.tolist()
output = []
for index in range(0,len(outputIn)):
    if index >= numberOfTestData:
        break
    if outputIn[index][0] <  10:
        outLine = []
        for nullIndex in range(0, 10):
            outLine.append(0)
        outLine[outputIn[index][0]] = 1
        testAnalyze[outputIn[index][0]] += 1
        output.append(outLine)

### Test model
accuracy, statistic = model.test(input=input, output=output, mode=TestTypes.biggestPredictionOn1Position)

### Analytics
printStatistics(statistic, ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"])

print(f"TrainData: Distribution Expected Outputs: {trainAnalyze}")

print(f"TestData: Distribution Expected Outputs: {testAnalyze}")
   
print(f"Accuracy: {accuracy}")