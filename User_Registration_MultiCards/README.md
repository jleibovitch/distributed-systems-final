# README_userRegistration2 - MultiCards

This flask implementation allows users to register and have multiple cards

-----------------------------------------------------

To installl all dependencies like flask_sqlalchemy, flask_login, wtforms etc.
run the below command in the terminal where requirements.txt is located

$    pip3 install -r requirements.txt



You may need to create/initialize the database and tables, here are the commands to do so:

(sidenote: try running User.query.all() in python3 commandline and if it returns a list then i do not think u need to do below)

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

To run simple run the following in the terminal where run.py is located: $   python3 run.py
