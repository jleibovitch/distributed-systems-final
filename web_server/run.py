"""
run.py
Author: Umar Qureshi

Main entry point for the flask web server
"""

from server import app
import os


if os.path.isfile('server/site.db'):
	print ("Site.db exists")
else:
	from server import db
	from server.models import User, Cards, Transactions
	db.create_all()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
