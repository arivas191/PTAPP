# PTAPP
After cloning the repo and moving into its directory, I recommend using a Python virtual environment:
```
virtualenv venv
source venv/bin/activate
```
Now you can install all the packages and dependencies in requirements.txt:
```
pip3 install -r requirements.txt
```
You can also use `pip` instead of `pip3`, depending on your setup. If you ever install more packages, make sure to add them to the requirements.txt file by doing:
```
pip3 freeze > requirements.txt
```

You will need to create the DB file locally since it will not be included in the repository. Run the following commands to create it:
```
python3
from flaskapp import db
from flaskapp.models import *
db.create_all()
```

You can now query the DB to verify it was created properly (you should also see a site.db file created inside the flaskapp directory):
```
User.query.all()
```

And that should return an empty object [].

To seed the database with the exercises, exit the python command line `exit()` and then run the command:
```
python3 seeds.py
```
Run the app:
```
flask run
```
And access it on http://localhost:5000/
