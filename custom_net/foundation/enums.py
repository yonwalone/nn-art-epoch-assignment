from enum import Enum

class Functions(Enum):

    #Activation Functions
    heaviside = 0
    sgn = 1
    tanh = 2
    reLu = 3
    no = 4

    # Error Functions
    halfsquareError = 100

    # Pooling Functions
    max = 200
    avg = 201

class PaddingType(Enum):
    valid = 0
    same = 1
    full = 2