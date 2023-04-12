from enum import Enum

class Functions(Enum):

    #Activation Functions
    heaviside = 0
    sgn = 1
    tanh = 2
    reLu = 3

    # Error Functions
    halfsquareError = 100

    # Pooling Functions
    max = 200
    avg = 201