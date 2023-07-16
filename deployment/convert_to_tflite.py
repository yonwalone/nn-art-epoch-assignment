import os
import tensorflow as tf
from tensorflow import keras

def convertToTFLITE(path, outputPath):
    myTfLiteModel = tf.keras.models.load_model(path)
    converter = tf.lite.TFLiteConverter.from_keras_model(myTfLiteModel)
    tflite_model = converter.convert()
    open(outputPath, "wb").write(tflite_model)


convertToTFLITE("my_model.h5", "lite_model.tflite")