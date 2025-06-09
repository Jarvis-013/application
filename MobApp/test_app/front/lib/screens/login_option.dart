import 'package:flutter/material.dart';

class LoginOptionScreen extends StatelessWidget {
  const LoginOptionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center( // Centers the entire Column in the screen
        child: Column(
          mainAxisSize: MainAxisSize.min, // Minimizes height to just fit content
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(
                  context,
                  '/login_employee',
                  arguments: {'user_type': 'employee'},
                );
              },
              child: const Text("Employee Login"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(
                  context,
                  '/customer_login',
                  arguments: {'user_type': 'customer'},
                );
              },
              child: const Text("Customer Login"),
            ),
          ],
        ),
      ),
    );
  }
}
