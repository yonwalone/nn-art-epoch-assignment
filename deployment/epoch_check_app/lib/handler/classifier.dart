import 'package:image/image.dart' as IMG;
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:typed_data';
import 'dart:io';

class Classifier{
  File? _image;
  bool imageChange = false;

  late Interpreter _interpreter;
  late List<String> _labels;

  Classifier(){
    loadModel();
  }

  Future<void> loadModel() async {
    try {
      _interpreter = await Interpreter.fromAsset('lite_model.tflite');
      final labelsData = await rootBundle.loadString('assets/labels.txt');
      _labels = labelsData.trim().split('\n');
      print(_interpreter.address);
    } catch (e) {
      print('Failed to load model: $e');
    }
  }

  Future<List<Map<String, dynamic>>> classifyImage(File? file) async {
   // Prepare input data
    _image = file;
    final inputImage = _image!.readAsBytesSync();
    var k = await _image!.readAsBytes();
    IMG.Image? foo1 = IMG.decodeImage(k);
    IMG.Image resized = IMG.copyResize(foo1!, width: 28, height: 28);
    var resizedBytes = resized.getBytes();

    /*for (int i = 0; i < resizedBytes.length; i++) {
      for (int j = 0; j < resizedBytes[i].length; j++) {
        double grayscaleValue = 0.2989 * resizedBytes[i][j][0] + 0.5870 * resizedBytes[i][j][1] + 0.1140 * resizedBytes[i][j][2];
        resizedBytes[i][j] = [grayscaleValue];
      }
    }

    // Add channel and batch dimensions
    resizedBytes = [resizedBytes]; // Add batch dimension
    resizedBytes = resizedBytes.map((image) => image.map((row) => row.map((pixel) => [pixel]).toList()).toList()).toList(); // Add channel dimension*/
    
    final inputShape = _interpreter.getInputTensor(0).shape;
    final inputType = _interpreter.getInputTensor(0).type;
    final normalizedBytes = resizedBytes.map((value) => value / 255.0).toList();
    final inputBuffer = Float32List.fromList(normalizedBytes);

    _interpreter.getInputTensor(0).data = resizedBytes;

    // Prepare output buffer
    var outputShape = [4, 10];
    var output = List.filled(outputShape.reduce((a, b) => a * b), 0).reshape(outputShape);

    // Run inference
    _interpreter.run(inputBuffer, output);

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