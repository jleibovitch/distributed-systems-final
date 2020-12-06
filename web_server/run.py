from server import app

# Allows us to run this program as a .py file
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
