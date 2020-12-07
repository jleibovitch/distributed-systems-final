"""
run.py
Author: Umar Ehsan

The main entry point for the flask server for tap scanner and server. Initializes the app and starts the server
"""

from app import app
import sys

# Allows us to run this program as a .py file
if __name__ == '__main__':
    port_number = 5000
    terminal_location = 0
    if (len(sys.argv) > 1):
        port_number = int(sys.argv[1])
    
    app.run(debug=True, host="127.0.0.1", port=port_number)
