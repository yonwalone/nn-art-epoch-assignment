import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

// show result in bottom sheet modal
class ResultView extends StatefulWidget {
  const ResultView({Key? key, required this.file, required this.prediction}) : super(key: key);

  final XFile file;
  final List<Map<String, dynamic>> prediction;

  @override
  ResultViewState createState() => ResultViewState();
}

 class ResultViewState extends State<ResultView> {

  @override
  Widget build(BuildContext context) {

    List<Map<String, dynamic>> data = widget.prediction;

    XFile file = widget.file;

    return SizedBox(
      height: 450, //720, TODO: Adapt to more results
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
            height: 5.0,
          ),
          Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(8.0, 8.0, 16.0, 8.0),
                  child: Row(
                    children: [
                      Container(
                        alignment: Alignment.topLeft,
                        width: 150.0,
                        height: 100.0,
                        child: Image.file(
                          File(file.path),
                          fit: BoxFit.contain,
                          width: double.infinity,
                          height: double.infinity,
                          )
                      ),
                      const SizedBox(
                        width: 20,
                      ),
                      Expanded(
                        child: Text(
                        file.name,
                        maxLines: 5,
                        overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(
                  height: 10,
                ),
                SizedBox(
                  height: 200,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: DataTable(
                          columns: const [
                            DataColumn(label: Text('Epoch')),
                            DataColumn(label: Text('Probability in %')),
                          ],
                          rows: List<DataRow>.generate(
                            data.length,
                            (index) => DataRow(
                              cells: [
                                DataCell(Text(data[index]["class_label"].toString())),
                                DataCell(Text((data[index]["probability"]*100).toString()))
                              ]
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ]),
        ]),
      ),
    );
  }
}
