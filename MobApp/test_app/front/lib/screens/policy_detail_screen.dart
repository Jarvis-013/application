import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PolicyDetailScreen extends StatefulWidget {
  final String policyNo;

  const PolicyDetailScreen({super.key, required this.policyNo});
  @override
  State<PolicyDetailScreen> createState() => _PolicyDetailScreenState();
}

class _PolicyDetailScreenState extends State<PolicyDetailScreen> {
  Map<String, dynamic>? policyDetails;
  bool isLoading = true;

  Future<void> fetchPolicyDetails() async {
    final url = Uri.parse('http://10.0.2.2:8000/policies/${widget.policyNo}');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          policyDetails = data;
        });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to load policy details')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    fetchPolicyDetails();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Policy Details')),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : policyDetails == null
          ? const Center(child: Text("No details available"))
          : ListView(
        padding: const EdgeInsets.all(16.0),
        children: policyDetails!.entries.map((entry) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "${entry.key}: ",
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Expanded(child: Text("${entry.value}")),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }
}
