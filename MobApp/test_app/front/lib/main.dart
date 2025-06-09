import 'package:flutter/material.dart';
import 'screens/welcome_screen.dart';
import 'screens/login_option.dart';
import 'screens/login_screen_employee.dart';
import 'screens/otp_verify_screen.dart';
import 'screens/login_screen_customer.dart';
import 'screens/customer_otp_verification.dart';
import 'screens/policy_list_screen.dart';
import 'screens/policy_detail_screen.dart';
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Policy App',
      debugShowCheckedModeBanner: false,
      initialRoute: '/',
      onGenerateRoute: (settings) {
        switch (settings.name) {
          case '/':
            return MaterialPageRoute(builder: (_) => const WelcomeScreen());

          case '/login_option':
            return MaterialPageRoute(builder: (_) => const LoginOptionScreen());

          case '/login_employee':
            final args = settings.arguments as Map<String, dynamic>?;
            return MaterialPageRoute(
              builder: (_) => SignInScreen1(userType: args?['user_type'] ?? 'employee'),
            );

          case '/otp_verification':
            final args = settings.arguments as Map<String, dynamic>?;
            return MaterialPageRoute(
              builder: (_) => OtpVerificationScreen(
                otp: args?['otp'],
                employeeId: args?['employee_id'],
              ),
            );

          case '/customer_login':
            return MaterialPageRoute(builder: (_) => const CustomerLoginScreen());

          case '/customer_otp_verification':
            final args = settings.arguments as Map<String, dynamic>;
            return MaterialPageRoute(
              builder: (_) => CustomerOtpVerificationScreen(
                customerId: args['customer_id'],
                otp: args['otp'],
              ),
            );

          case '/policy_list':
            final args = settings.arguments as Map<String, dynamic>;
            return MaterialPageRoute(
              builder: (_) => PolicyListScreen(customerId: args['customer_id']),
            );

            case '/policy_detail':
              final policyNo = settings.arguments.toString(); // this is just a string/int
              return MaterialPageRoute(
                builder: (context) => PolicyDetailScreen(policyNo: policyNo),
              );

              default:
            return MaterialPageRoute(
              builder: (_) => const Scaffold(body: Center(child: Text('Route not found'))),
            );
        }
      },
    );
  }
}
