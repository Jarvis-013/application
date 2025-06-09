import 'package:flutter/material.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ElevatedButton(
          child: const Text("Get Started"),
          onPressed: () {
            Navigator.pushNamed(context, '/login_option');
          },
        ),
      ),
    );
  }
}
