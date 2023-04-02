from flask import Flask, request, jsonify, render_template
from keras.models import load_model
import tensorflow as tf

#tf.saved_model.LoadOptions = '/job:localhost'

# Load the Keras model
#options = tf.saved_model.LoadOptions(experimental_io_device='/job:localhost')
#model = load_model('deployment\\test_model', options=options)
#model = load_model(filepath='deployment/test_model')
#model = tf.keras.models.load_model('deployment\\test_model')

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
    # Get the data from the request
    data = request.get_json()

    # Make a prediction using the loaded model
    #prediction = model.predict(data)

    # Return the prediction as a JSON response
    #return jsonify(prediction.tolist())
    epoch_list = ["expressionism", "realsim"]
    return jsonify(epoch_list)