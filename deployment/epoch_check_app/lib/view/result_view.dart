import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';


///builds a widget to create a session to be shown as a ModalSheet
class ResultView extends StatefulWidget {
  const ResultView({Key? key, required this.file}) : super(key: key);

  final XFile file;

  @override
  _ResultViewState createState() => _ResultViewState();
}

class _ResultViewState extends State<ResultView> {

  @override
  Widget build(BuildContext context) {

    XFile file = widget.file;

    final List<List<String>> data = [    
      ['realism', '0.11'],
      ['impressionism', '0.11'],
      ['romanticism', '0.11'],
      ['expressionism', '0.11'],
      ['post-impressionism', '0.11'],
      ['baroque', '0.11'],
      ['art-nouveau-modern', '0.11'],
      ['surrealism', '0.11'],
      ['symbolism', '0.11'],
      ['abstract-expressionism', '0.11'],
    ];

    return SizedBox(
      height: 720,
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
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
                //mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
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
                  const SizedBox(
                    height: 15,
                  ),
                  SizedBox(
                    height: 200,
                    child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: DataTable(
                      columns: [
                        DataColumn(label: Text('Epoch')),
                        DataColumn(label: Text('Probability in %')),
                      ],
                      rows: List<DataRow>.generate(
                        data.length,
                        (index) => DataRow(
                          cells: List<DataCell>.generate(
                            data[index].length,
                            (index2) => DataCell(Text(data[index][index2])),
                          ),
                        ),
                      ),
                    ),
                                  ),
                  ),
                ]),
            ),
        ]),
      ),
    );
  }
}
