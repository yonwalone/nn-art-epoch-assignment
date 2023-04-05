import 'package:flutter/material.dart';

///opens a [ModalBottomSheet] with some preferences to simplify the call
void customModal({required BuildContext context, required Widget modal}) {
  showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return SingleChildScrollView(
            padding: EdgeInsets.only(
                bottom: MediaQuery.of(context).viewInsets.bottom),
            child: modal);
      });
}
