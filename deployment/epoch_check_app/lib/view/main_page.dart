import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'package:epoch_check_app/view/result_view.dart';
import 'package:epoch_check_app/handler/modal_create.dart';
import 'package:epoch_check_app/handler/classifier.dart';

/// builds the session page
class MainPage extends StatefulWidget {
  const MainPage({Key? key}) : super(key: key);

  @override
  MainPageState createState() => MainPageState();
}

class MainPageState extends State<MainPage> {

  bool imageChange = false;
  Classifier clas = Classifier();

  void handleImage(BuildContext context, ImageSource source) async {
    // handle chosen image

    final pickedFile = await ImagePicker().pickImage(source: source);
    if (pickedFile == null) {return;}
    File image = File(pickedFile.path);
    imageChange = true;
    setState(() {});
    
    // classify image
    clas.classifyImage(image).then((value) {
      // show result when recieved
      imageChange = false;
      customModal(context: context, modal: ResultView(file: pickedFile, prediction: value,));
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
                onPressed: () => handleImage(context, ImageSource.gallery)
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
                    handleImage(context, ImageSource.camera);
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
