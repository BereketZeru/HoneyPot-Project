import paramiko
import socket
import threading
import logging
from flask import Flask, request, render_template, redirect, url_for, flash, session

# Flask app setup & Config
app = Flask(__name__)
app.secret_key = 'rstfegouipheg9rpuh9guier87954vbs98u7hvb0t7y7gtb8fbh087456gvhw87ygv087styh78u9gh502484yhgq4598h78uyrth0987wrhbv89eyt78gh549uh87fds087'


logging.basicConfig(filename='HTTP_login_attempts.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/', methods=['GET', 'POST'])

def login():
    if 'tries' not in session:
        session['tries'] = 0
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # "authentication check"
        if username == 'admin' and password == 'password' or session['tries'] > 1000:
            # successful
            session['tries'] = 0
            return render_template('dashboard.html')
        else:
            # failed
            flash('Invalid username/password', 'error')
            logging.info(f'Failed login attempt - Username: {username} Password: {password}')
            session['tries'] += 1
            
    # login page
    return render_template('login.html')

def run_flask_app():
    host = '0.0.0.0'
    port = 80
    print(f"Flask app hosting on port {port}")
    app.run(debug=False, host=host, port=port, use_reloader=False)

# rsa key
host_key = paramiko.RSAKey(filename="C:/Users/berek/OneDrive/Desktop/Honeypot Folder/HP_RSA/RSA")

class Server(paramiko.ServerInterface):
    def __init__(self, log_file):
        self.log_file = log_file

    def check_auth_password(self, username, password):
        # Log every login attempt
        with open(self.log_file, "a") as log:
            log.write(f"Login attempt: {username} with password {password}\n")
        
        # credentials
        if username == "admin" and password == "password":
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'
    
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        # open a shell
        return True

def start_honeypot(log_file, port=2222):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen(100)
    print(f"Listening for connection on port {port}...")

    while True:
        client, addr = server.accept()
        print(f"Connection attempt from {addr}")
        t = threading.Thread(target=handle_connection, args=(client, log_file))
        t.start()

def handle_connection(client_socket, log_file):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(host_key)
        server = Server(log_file)
        
        transport.start_server(server=server)
        
        channel = transport.accept(20)
        if channel is None:
            print("No channel.")
            return
        
        # command prompt
        channel.send("\nWelcome to the Pegasus Smart Fridge command interface! | Version 5.3e.12 | Type help for a list of commands | Press enter to start | --> ")
        while True:  # Keep the shell session open
            command = channel.recv(1024).decode('utf-8').strip()
            
            # Log the command for analysis
            with open(log_file, "a") as log:
                log.write(f"Executed command: {command}\n")
            
            # Basic command simulation
            if command == "help":
                channel.send("Available commands:\n- help: Displays this help message.\n- internet status: Checks if the internet connection is active.\n- model: Displays the model number of the device.\n- make: Displays the make of the device.\n- eco mode: Checks if eco mode is active.\n- filter status: Checks the status of the filter.\n"
)
            elif command == "internet status":
                channel.send("true\n")
            elif command == "model":
                channel.send("RF23BB890012AA / RF23BB890012AA\n")
            elif command == "make":
                channel.send("Pegasus Bespoke Counter Depth 4-Door French Door Refrigerator\n")
            elif command == "eco":
                channel.send("true\n")
            elif command == "filter status":
                channel.send("true\n")
            else:
                channel.send(f"{command}: command not found. Type help for a list of commands\n")
            channel.send("$ ") 
            
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__": 