import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignInScreen1 extends StatefulWidget {
  final String userType;

  const SignInScreen1({super.key, required this.userType});

  @override
  State<SignInScreen1> createState() => _SignInScreen1State();
}

class _SignInScreen1State extends State<SignInScreen1> {
  final TextEditingController _empIdController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  Future<void> _login() async {
    final empId = _empIdController.text.trim();
    final password = _passwordController.text.trim();

    final url = Uri.parse('http://10.0.2.2:8000/login');

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'employee_id': empId, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final otp = data['otp'];
        final employeeId = data['emp_id'];

        print("Received OTP: $otp");

        Navigator.pushNamed(
          context,
          '/otp_verification',
          arguments: {
            'otp': otp,
            'employee_id': employeeId,
          },
        );
      } else {
        final msg = jsonDecode(response.body)['detail'] ?? "Login failed.";
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Employee Login")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: _empIdController, decoration: const InputDecoration(labelText: 'Employee ID')),
            TextField(controller: _passwordController, obscureText: true, decoration: const InputDecoration(labelText: 'Password')),
            const SizedBox(height: 20),
            ElevatedButton(onPressed: _login, child: const Text("Login")),
          ],
        ),
      ),
    );
  }
}
