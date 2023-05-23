import base64
import io
import os
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
from keras.models import load_model
import numpy as np
import tensorflow as tf

#Load model
model = load_model(os.path.join('deployment', 'big_model.h5'))

# Create the Flask application
app = Flask(__name__, static_folder='static')

#Show website
@app.route('/')
def index():
    return render_template('view.html')


if __name__ == '__main__':
    app.run(host="192.168.178.77")

# Define a route for the model prediction
@app.route('/predict', methods=['POST'])
def predict():

    # Read image from request
    file = request.files['file']
    image = Image.open(file.stream).convert('RGB')

    # Convert to expected input shape
    image_array = np.array(image.resize((224, 224))) / 255.0
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
   
    # Predict
    prediction = model.predict(image_array)

    # List of class labels
    class_labels = ["realism", 
    "impressionism",
    "romanticism",
    "expressionism",
    "post-impressionism",
    "baroque",  
    "art-nouveau-modern", 
    "surrealism",
    "symbolism",
    "abstract-expressionism"]

    # Create a list of predicted classes with their corresponding probabilities
    predicted_classes = []
    for index in range(0, len(prediction[0])):
        class_label = class_labels[index]
        probability = float(prediction[0][index])
        predicted_classes.append((class_label, probability))

    # Sort the list of predicted classes in decreasing order of probability
    predicted_classes = sorted(predicted_classes, key=lambda x: x[1], reverse=True)
    print(predicted_classes) 
    
    return jsonify(predicted_classes)