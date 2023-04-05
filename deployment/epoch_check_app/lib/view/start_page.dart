import 'dart:async';
import 'dart:collection';
import 'dart:io';
import 'package:flutter/material.dart';

import 'package:image_picker/image_picker.dart';
//import 'package:tflite_flutter/tflite_flutter.dart';

import 'package:epoch_check_app/view/result_view.dart';
import 'package:epoch_check_app/handler/modal_create.dart';

/// builds the session page
class MainPage extends StatefulWidget {
  const MainPage({Key? key}) : super(key: key);

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {

  XFile? _image;
  bool imageChange = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  Future<void> pickImageFromGallery(BuildContext context) async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      print(pickedFile);
      imageChange = true;
      _image = pickedFile;
      handleImage(context, pickedFile);
    }
  }

  Future<void> pickImageFromCamera(BuildContext context) async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      print(pickedFile);
      imageChange = true;
      _image = pickedFile;
      handleImage(context, pickedFile);

    }
  }

  void handleImage(BuildContext context, XFile file) {
    customModal(context: context, modal: ResultView(file: file,));
  }

  @override
  Widget build(BuildContext context) {

    return Center(
      child: Column(
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
      ),
    );
  }
}
