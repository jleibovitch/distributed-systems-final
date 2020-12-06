from server import app
import os


if os.path.isfile('server/site.db'):
	print ("Site.db exists")
else:
	from server import db
	from server.models import User, Cards, Transactions
	db.create_all()
	# If the below 2 lines gives an empty lists you did it correctly
	# User.query.all()
	# Cards.query.all()
	# now exit python commandline
	# exit()


# Allows us to run this program as a .py file
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
