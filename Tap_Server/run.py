from app import app
from app import models
import sys

# Allows us to run this program as a .py file
if __name__ == '__main__':
    port_number = 5000
    terminal_location = 12345
    if (len(sys.argv) == 2):
        port_number = int(sys.argv[1])
    if (len(sys.argv) == 3):
            terminal_location = int(sys.argv[2])
    
    models.terminal_location = terminal_location
    app.run(debug=True, host="0.0.0.0", port=port_number)