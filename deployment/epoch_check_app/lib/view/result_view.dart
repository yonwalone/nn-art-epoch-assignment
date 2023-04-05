import 'dart:io';
import 'package:flutter/material.dart';


///builds a widget to create a session to be shown as a ModalSheet
class ResultView extends StatefulWidget {
  const ResultView({Key? key}) : super(key: key);

  @override
  _ResultViewState createState() => _ResultViewState();
}

class _ResultViewState extends State<ResultView> {

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 400,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(children: [
          Row(
            children: [
              Padding(
                padding: const EdgeInsets.only(left: 8.0),
                child: Text(
                  "Result",
                  style: Theme.of(context).textTheme.titleMedium,
                ),
              ),
              const Spacer(),
              IconButton(
                icon: Icon(
                  Icons.cancel,
                  color: Theme.of(context).primaryColor,
                  size: 30,
                ),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              )
            ],
          ),
          const SizedBox(
            height: 30.0,
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Text("Image"),
                      //Image.file(File('important_image.png')),
                      const SizedBox(
                        width: 100,
                      ),
                      const Text("ImageName")
                    ],
                  ),
                  const SizedBox(
                    height: 20,
                  ),
                  Column(
                    children: [
                      Row(
                        children: const [
                          Text("Epoch"),
                          SizedBox(
                            width: 100,
                          ),
                          Text("Probability")
                        ],
                      )
                    ],
                  )
                ]),
          )
        ]),
      ),
    );
  }
}
