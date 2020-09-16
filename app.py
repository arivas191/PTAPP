from flask import Flask, render_template
app = Flask(__name__)

#endpoint for the home page
@app.route('/')
def home():
    return render_template('index.html')

#endpoint for the login page
@app.route('/login')
def login():
    return render_template('login.html')

#endpoint for the register page
@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
