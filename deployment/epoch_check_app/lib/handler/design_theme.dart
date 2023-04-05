import 'package:flutter/material.dart';

///global Theme to easily access Colors and TextStyles everywhere
final ThemeData darktheme = ThemeData(
  colorScheme: ColorScheme(
    background: const Color(0xFF0E1418), //Background Default - Page
    onBackground: const Color(0xFF0E1418), //Background Surface - For Tiles

    primary: const Color(0xFF4A4E51), //Neutral Contras Low
    onPrimary: const Color(0xFFB0B1B2), //Neutral Contras Medium

    secondary: Colors.blue.shade300,
    onSecondary: const Color(0x090E1418),

    onPrimaryContainer: Colors.blue.shade900,
    onSecondaryContainer: Colors.blue.shade400,
    onTertiaryContainer: Colors.blue.shade700,
    inversePrimary: Colors.blue.shade800,
    onTertiary: Colors.blue.shade500,
    primaryContainer: Colors.blue.shade600,
    surface: Colors.blue.shade300,
    onSurface: Colors.white,

    error: const Color(0xFF01BA1D), //Notification Error
    onError: const Color(0xFF7C7F81), //State Disabled

    brightness: Brightness.dark,
  ),
  scaffoldBackgroundColor: const Color(0xFF1A2023), //Page Background
  primaryColor: const Color(0xFFd5001c),

  textTheme: const TextTheme(
    displayLarge: TextStyle(
        fontSize: 30, color: Colors.white, fontWeight: FontWeight.bold),
    displayMedium: TextStyle(
      fontSize: 24, color: Colors.white, fontWeight: FontWeight.normal),
    displaySmall: TextStyle(
      fontSize: 15, color: Colors.white, fontWeight: FontWeight.normal),
  ),
);
