from model import SeqModel
from layer.layer import Layer
from layer.conv_layer import CONVLayer
from layer.pooling_layer import PoolLayer
from layer.softmax_layer import SoftMaxLayer
import json
from foundation.enums import Functions, LayerType, PaddingType

#currently only working with SeqModel and only "normal" layers

def saveModel(model, file):
    """
    Save model to file

    Params:
        - model: Model that should be saved
        - file: json file to be saved to
    """
    structure = model.getStructure()
    data = {}
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
    structure = data['structure']

    layer = []
    for layerIndex, currLayer in enumerate(structure):
        type = LayerType(currLayer[0])
        
        if type == LayerType.dense:
            value = currLayer[1]
            layer.append(Layer(count=value[0], function=Functions(value[1]), initialWeights=value[2], isOutput=value[3]))
        elif type == LayerType.conv:
            value = currLayer[1]
            layer.append(CONVLayer(matrix=value[0], stride=value[1], padding=PaddingType(value[2])))
        elif type == LayerType.pool:
            value = currLayer[1]
            layer.append(PoolLayer(function = Functions(value[0]), poolSize= value[1], stride=value[2], toList=value[3]))
        elif type == LayerType.softmax:
            layer.append(SoftMaxLayer())
        else:
            raise Exception("Not valid LayerType")

    f.close()
    return SeqModel(layer, False) # might adapt for only MLP (bias topic)

