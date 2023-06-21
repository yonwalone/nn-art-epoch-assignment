import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:typed_data';
import 'dart:io';

class Classifier{

  late Interpreter _interpreter;
  late List<String> _labels;

  Classifier(){
    loadModel();
  }

  Future<void> loadModel() async {
    // load model from assets
    _interpreter = await Interpreter.fromAsset('lite_model.tflite');
    final labelsData = await rootBundle.loadString('assets/labels.txt');
    _labels = labelsData.trim().split('\n');
  }

  Future<List<Map<String, dynamic>>> classifyImage(File? file) async {
    // classify image into labels
   
    // Prepare input data
    var imageBytes = await file!.readAsBytes();
    img.Image? decodedImage = img.decodeImage(imageBytes);
    int expectedWidth = 224;
    int expectedHeight = 224;
    img.Image resizedImg = img.copyResize(decodedImage!, width: expectedWidth, height: expectedHeight);
    var resizedBytes = resizedImg.getBytes(format: img.Format.rgb);

    //Convet List of bytes into input shape
    List<List<Float32List>> imageArray = [];
    for(int h = 0; h < expectedHeight; h++){
      List<Float32List> row = [];
      for(int w = 0; w < expectedWidth; w++){
        int ground = (h * expectedHeight + w) * 3;
        var red = resizedBytes[ground] / 255.0;
        var green = resizedBytes[ground +1] / 255.0;
        var blue = resizedBytes[ground + 2] / 255.0;
        List<double> pixel = [red, green, blue];
        row.add(Float32List.fromList(pixel));
      }
      imageArray.add(row);
    }

    var input = [imageArray]; // Add batch dimension

    // Prepare output buffer
    var supportedClasses = 1000;
    var outputShape = [1, supportedClasses];
    var output = List.filled(outputShape.reduce((a, b) => a * b), 0).reshape(outputShape);

    // Run interpreter
    _interpreter.run(input, output);

    // Create a list of predicted classes with their corresponding probabilities
    List<Map<String, dynamic>> predictedClasses = [];
    for (int index = 0; index < _labels.length; index++) {
      String classLabel = _labels[index];
      double probability = output[0][index].toDouble();
      predictedClasses.add({"class_label": classLabel, "probability": probability});
    }

    // Sort the list of predicted classes in decreasing order of probability
    predictedClasses.sort((a, b) => b["probability"].compareTo(a["probability"]));

    return predictedClasses;
  }
}