# HoneyPot Project Summary
 Overview:
The Honeypot project is a low interaction honeypot designed to mimic an IoT device, specifically a Smart Fridge. It logs all HTTP and SSH interactions to capture potential malicious activity. 

Purpose:
The main objective of the project is to serve as a decoy to attract and diver potential attackers away from the actual production systems. 

By logging interactions, the honeypot provides valuable insights into common attack vectors and techniques used by malicious actors targeting IoT devices.

Key Features:
HTTP and SSH Logging: The honeypot logs all HTTP and SSH interactions, enabling the analysis of attempted attacks and unauthorized access attempts.

Authentication Simulation: The project simulates a login/authentication mechanism for HTTP and SSH connections, logging failed login attempts for analysis.

Command Simulation: Upon successful SSH connection, the honeypot presents a command interface simulating Smart Fridge functionalities, logging executed commands for further investigation.

How It Works:

The Project is implemented using Python, leveraging libraries such as Paramiko for SSH server implementation and Flash for HTTP server functionality.

Upon initialization, the honeypot listens for incoming SSH connections on port 2222 and HTTP requests on port 80

Incoming SSH connections are authenticated and logged, while HTTP requests are processed to simulate Smart Fridge functionalities, with all interactions logged for analysis.
