# README_userRegistration1

You may need to creat/initialize the database and table, here are the commands to do so:

(sidenote: try running User.query.all() in python3 commandline and if it returns a list then i do not think u need to do below)

go into python3 commandline by running python3

```python3
from flaskblog import db
from flaskblog.models import User, Post
db.create_all()
# If the below line gives an empty list you did it correctly
User.query.all()
# now exit python commandline
exit()
```

Then you may need to pip3 install a bunch of things like:

flask_sqlalchemy
flask_bcrypt
flask_login
flask_wtf
wtforms

(i may have missed some)
