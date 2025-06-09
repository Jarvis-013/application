import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CustomerOtpVerificationScreen extends StatefulWidget {
  final String customerId;
  final String otp;

  const CustomerOtpVerificationScreen({
    super.key,
    required this.customerId,
    required this.otp,
  });

  @override
  State<CustomerOtpVerificationScreen> createState() => _CustomerOtpVerificationScreenState();
}

class _CustomerOtpVerificationScreenState extends State<CustomerOtpVerificationScreen> {
  final _otpController = TextEditingController();

  Future<void> _verifyOtp() async {
    final enteredOtp = _otpController.text.trim();

    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/verify-otp'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': widget.customerId,
        'otp': enteredOtp,
        'user_type': 'customer',
      }),
    );

    if (response.statusCode == 200) {
      Navigator.pushNamed(context, '/policy_list', arguments: {
        'customer_id': widget.customerId,
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('OTP verification failed')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Verify OTP")),
      body: Column(
        children: [
          TextFormField(controller: _otpController, decoration: const InputDecoration(labelText: "Enter OTP")),
          ElevatedButton(onPressed: _verifyOtp, child: const Text("Verify")),
        ],
      ),
    );
  }
}
