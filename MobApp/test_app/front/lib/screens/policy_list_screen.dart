import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PolicyListScreen extends StatefulWidget {
  final String customerId;
  const PolicyListScreen({super.key, required this.customerId});

  @override
  State<PolicyListScreen> createState() => _PolicyListScreenState();
}

class _PolicyListScreenState extends State<PolicyListScreen> {
  List<dynamic> _policies = [];
  bool _isLoading = true;

  Future<void> _fetchPolicies() async {
    try {
      final url = Uri.parse('http://10.0.2.2:8000/customers/${widget.customerId}/policies');
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _policies = data;
        });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Failed to load policies")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _fetchPolicies();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Your Policies')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _policies.isEmpty
          ? const Center(child: Text('No policies found.'))
          : ListView.builder(
        itemCount: _policies.length,
        itemBuilder: (context, index) {
          final policy = _policies[index];
          return ListTile(
            title: Text('Policy Name: ${policy['policy_type'] ?? 'N/A'}'),
            subtitle: Text('Policy ID: ${policy['policy_id'] ?? 'N/A'}'),
            trailing: const Icon(Icons.arrow_forward_ios),
            onTap: () {
              Navigator.pushNamed(
                context,
                '/policy_detail',
                arguments: policy['policy_number'],
              );
            },
          );
        },
      ),
    );
  }
}
