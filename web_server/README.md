# README_userRegistration3 - Single Card

This flask implementation allows users to register with a single card

-----------------------------------------------------

To install all dependencies like flask_sqlalchemy, flask_login, wtforms etc.
run the below command in the terminal where requirements.txt is located

$    pip3 install -r requirements.txt



You may need to create/initialize the database and tables, here are the commands to do so:

(sidenote: try running User.query.all() after importing db and models (shown below) in python3 commandline and if it returns a list then i do not think u 
need to do all the commands below)

(if above sidenote does not work please delete site.db file before doing the belowsteps)

go into python3 commandline by running $ python3 in the terminal and enter te following commands line by line

```python3
from flaskblog import db
from flaskblog.models import User, Cards
db.create_all()
# If the below 2 lines gives an empty lists you did it correctly
User.query.all()
Cards.query.all()
# now exit python commandline
exit()
```

To run the program, simply run the following command in the terminal where run.py is located: $   python3 run.py
