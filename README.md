# PTAPP
I'm writing here the commands I had to run to set it up. I'm using a mac, so keep that in mind as they may differ from you.

First, you need to have python and pip installed. I already had them installed from before so I didn't need to run anything. Once you have these, you need to install flask:

`pip3 install flask`

Then do:

`export FLASK_APP=app.py`

Now, you can it in two ways (inside the project directory):

`flask run`

Or:

`python3 app.py`

I'm using the second option since this one has the Debug option turned on and you can just refresh the page when you make a code change, so you don't have to re-run Flask.

You should be able to access it on http://localhost:5000/
