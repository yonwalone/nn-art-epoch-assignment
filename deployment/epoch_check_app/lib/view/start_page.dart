import 'dart:async';
import 'dart:collection';
import 'dart:ffi';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image/image.dart' as IMG;
import 'dart:typed_data';
import 'package:flutter/services.dart' show rootBundle;

import 'package:image_picker/image_picker.dart';
import 'package:tflite_flutter/tflite_flutter.dart';
//import 'package:tflite_flutter_helper/tflite_flutter_helper.dart';

import 'package:epoch_check_app/view/result_view.dart';
import 'package:epoch_check_app/handler/modal_create.dart';
import 'package:epoch_check_app/handler/classifier.dart';

/// builds the session page
class MainPage extends StatefulWidget {
  const MainPage({Key? key}) : super(key: key);

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {

  File? _image;
  bool imageChange = false;
  Classifier clas = Classifier();

  Future<void> pickImageFromGallery(BuildContext context) async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      print(pickedFile);
      imageChange = true;
      _image = File(pickedFile.path);
      handleImage(context, pickedFile);
    }
  }

  Future<void> pickImageFromCamera(BuildContext context) async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      print(pickedFile);
      imageChange = true;
      _image = File(pickedFile.path);
      handleImage(context, pickedFile);

    }
  }

  void handleImage(BuildContext context, XFile file) async {
    setState(() {});
    await clas.classifyImage(_image).then((value) {
      imageChange = false;
      customModal(context: context, modal: ResultView(file: file, prediction: value,));
      clas.loadModel();
      setState(() {});
    },);
  }

  @override
  Widget build(BuildContext context) {

    return Center(
      child: !imageChange ? Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const SizedBox(
            height: 50,
          ),
          Column(
            children: [
              IconButton(
                iconSize: 170,
                icon: const Icon(
                  Icons.upload,
                ),
                onPressed: () => pickImageFromGallery(context)
                //customModal(context: context, modal: const ResultView()),
              ),
              Text(
                "Upload Image",
                style: Theme.of(context).textTheme.displayLarge,
              ),
            ],
          ),
          const SizedBox(
            height: 50,
          ),
          Column(
            children: [
              IconButton(
                  iconSize: 170,
                  icon: const Icon(
                    Icons.photo_camera,
                  ),
                  onPressed: () {
                    pickImageFromCamera(context);
                  }),
              Text(
                "Take a picture",
                style: Theme.of(context).textTheme.displayLarge,
              ),
            ],
          ),
          const SizedBox(
            height: 50,
          ),
        ],
      ): const CircularProgressIndicator(), 
    );
  }
}
