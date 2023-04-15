from model import SeqModel
from layer.layer import Layer
import json
from foundation.functions import Functions

#currently only working with SeqModel and only "normal" layers

def saveModel(model, file):
    """
    Save model to file

    Params:
        - model: Model that should be saved
        - file: json file to be saved to
    """
    weights = model.getWeights()
    structure = model.getStructure()
    data = {}
    data['weights'] = weights
    data['structure'] = structure

    with open(file, 'w') as f:
        json.dump(data, f)


def readModelFromStorage(file):
    """
    Save model from file

    Params:
        - file: json file including model

    Returns:
        - Model read from file
    """

    f = open(file)
    data = json.load(f)
    weights = data['weights']
    structure = data['structure']

    layer = []
    for layerIndex in range(0, len(structure)):
        layer.append(Layer(count = structure[layerIndex][0], function=Functions(structure[layerIndex][1]), 
                initialWeights=weights[layerIndex], isOutput=structure[layerIndex][2]))

    f.close()
    return SeqModel(layer)

