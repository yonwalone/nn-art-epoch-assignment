import base64
import io
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
from keras.models import load_model
import numpy as np
import tensorflow as tf

#Load model
model = load_model('deployment\\my_model.h5')

# Create the Flask application
app = Flask(__name__, static_folder='static')

#Show website
@app.route('/')
def index():
    return render_template('view.html')


if __name__ == '__main__':
    app.run()

# Define a route for the model prediction
@app.route('/predict', methods=['POST'])
def predict():

    file = request.files['file']
    image = Image.open(file.stream).convert('RGB')

    # Convert to expected input shape TODO: Adapt to our model
    image_array = np.array(image.resize((28, 28))) / 255.0
    image_array = np.dot(image_array[...,:3], [0.2989, 0.5870, 0.1140])  # Convert to grayscale
    image_array = np.expand_dims(image_array, axis=-1)  # Add channel dimension
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    prediction = model.predict(image_array)

    #list = prediction[0]
    #maxValue = max(list)
    #index = list.index(max(list))

    # List of class labels
    class_labels = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
        "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

    # Create a list of predicted classes with their corresponding probabilities
    predicted_classes = []
    for index in range(0, len(class_labels) -1):
        class_label = class_labels[index]
        probability = float(prediction[0][index])
        predicted_classes.append((class_label, probability))

    # Sort the list of predicted classes in decreasing order of probability
    predicted_classes = sorted(predicted_classes, key=lambda x: x[1], reverse=True)

    print(predicted_classes)
    result_text = ""

    for cla in predicted_classes:
        label, value = cla
        result_text += label + ": " + str(value) + "; "
    
    return jsonify(predicted_classes)