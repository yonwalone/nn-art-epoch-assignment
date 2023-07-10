import os
import cv2
import numpy as np
from config import PROJECT_ROOT, EPOCHS

from foundation.enums import Functions, PaddingType, TestTypes
from foundation.helper import printStatistics, preprocessImages
from model.model import SeqModel
from model.load_save_model import saveModel
from layer.layer import Layer
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from layer.flatten_layer import FlattenLayer
from layer.softmax_layer import SoftMaxLayer

# Problem: weight increase to much => no fitting result

class TrainData:
    def __init__(self, input, output) -> None:
        self.input = input,
        self.output = output

def getImages():
    # Valid not used because unsupported
    using_split = "only_resized_all_epochs"

    train_path = os.path.join(PROJECT_ROOT, "data", "splits", using_split, "train")
    test_path = os.path.join(PROJECT_ROOT, "data", "splits", using_split, "test")
    trainX, trainY = getImagesFromSplit(train_path)
    testX, testY = getImagesFromSplit(test_path)

    return trainX, trainY, testX, testY


def getImagesFromSplit(rootPath):
    data = []
    for epoch in EPOCHS:
        images_path = os.path.join(rootPath, epoch)
        image_files = os.listdir(images_path)
        count = 0
        for file_name in image_files:
            if count > 10:
                break
            count = count + 1
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                image_path = os.path.join(images_path, file_name)
                image = cv2.imread(image_path)
                imageRgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                transformImg = (np.transpose(imageRgb, (2, 0, 1)) / 255 * 2 - 0.5)

                # Make output
                expOutput = None
                if epoch == "realism":
                    expOutput = [1,0,0,0,0,0,0,0,0,0]
                elif epoch == "impressionism":
                    expOutput = [0,1,0,0,0,0,0,0,0,0]
                elif epoch == "romanticism":
                    expOutput = [0,0,1,0,0,0,0,0,0,0]
                elif epoch == "expressionism":
                    expOutput = [0,0,0,1,0,0,0,0,0,0]
                elif epoch == "post-impressionism":
                    expOutput = [0,0,0,0,1,0,0,0,0,0]
                elif epoch == "baroque":
                    expOutput = [0,0,0,0,0,1,0,0,0,0]
                elif epoch == "art-nouveau-modern":
                    expOutput = [0,0,0,0,0,0,1,0,0,0]
                elif epoch == "surrealism":
                    expOutput = [0,0,0,0,0,0,0,1,0,0]
                elif epoch == "symbolism":
                    expOutput = [0,0,0,0,0,0,0,0,1,0]
                elif epoch == "abstract-expressionism":
                    expOutput = [0,0,0,0,0,0,0,0,0,1]

                data.append(TrainData(transformImg, expOutput))

    # Shuffle elements
    np.random.shuffle(data)
    inputs = []
    expOutputs = []

    for imgIndex in range(0, len(data)):
        image = data[imgIndex]
        inputs.append(image.input[0].tolist())
        expOutputs.append(image.output)

    return inputs, expOutputs

trainX, trainY, testX, testY = getImages()


### Create Model

conv = CONVLayer(matrix= 3, stride=1, inputDepth=3, outputDepth=2, padding=PaddingType.valid)
pol = PoolLayer(function=Functions.avg, poolSize=3, stride=1)
flat = FlattenLayer()
den1 = Layer(count=100, function=Functions.tanh)
den3 = Layer(count=10, function=Functions.tanh, isOutput=True)
soft = SoftMaxLayer()
model = SeqModel([conv, pol, flat, den1, den3, soft])

### Train Model
model.train(input=trainX, output=trainY, errorFunc=Functions.halfsquareError, learningRate=0.0001, epochs=1)

saveModel(model, "tmp_model.json")

### Test model
accuracy, statistic = model.test(input=testX, output=testY, mode=TestTypes.biggestPredictionOn1Position)

### Analytics
printStatistics(statistic, EPOCHS)
   
print(f"Accuracy: {accuracy}")
                