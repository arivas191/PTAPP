# PTAPP
I'm writing here the commands I had to run to set it up. I'm using a mac, so keep that in mind as they may differ from you.

First, you need to have python and pip installed. I already had them installed from before so I didn't need to run anything. Once you have these, you need to install flask:

`pip3 install flask`

Then do:

`export FLASK_APP=run.py`

Now, download all the external libraries the program uses:

`pip3 install flask-wtf`\n
`pip3 install flask-sqlalchemy`\n
`pip3 install flask-bcrypt`\n
`pip3 install flask-login`\n

You will need to create the DB file locally since it will not be included in the repository. Run the following commands to create it:

`python3`\n
`from flaskapp import db`\n
`from flaskapp.models import User`\n
`db.create_all()`\n

You can now query the DB to verify it was created properly (you should also see a site.db file created inside the flaskapp directory):

`User.query.all()`

And that should return an empty object [].

Now, you can it in two ways (inside the project directory):

`flask run`

Or:

`python3 run.py`

I'm using the second option since this one has the Debug option turned on and you can just refresh the page when you make a code change, so you don't have to re-run Flask.

You should be able to access it on http://localhost:5000/
