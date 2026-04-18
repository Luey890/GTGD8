from flask import Flask, redirect, render_template, request, session
import db

app = Flask(__name__)
app.secret_key = "gtg"

@app.route("/")
def Home():
    guessData = db.GetAllGuesses() # Note: the new line
    return render_template("index1.html", guesses=guessData) #Note: passing data
@app.route("/login", methods=["GET", "POST"])
def Login():
    if session.get('username'):
        return redirect("/")

##################################
### New code starts here
##################################

    # They sent us data, get the username and password
    # then check if their details are correct.
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Did they provide good details
        if not username or not password:
            return render_template("login.html", error="Fields cannot be empty")

        user = db.CheckLogin(username, password)
        if user:
            # Yes! Save their username and id then
            session.clear()
            session['id'] = user['id']
            session['username'] = username
            return redirect("/")
        if session.get('username'):
            return redirect("/")


##################################
### New code ends here
##################################

    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def Register():

    # If they click the submit button, let's register
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            # Success! Let's go to the homepage
            return redirect("/")
        if session.get('username'):
            return redirect("/")
        
    return render_template("register.html")
@app.route("/add", methods=["GET","POST"])
def Add():

    if session.get('username') == None:
        return redirect("/")


    # Did they click submit?
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        game = request.form['game']
        score = request.form['score']

        # Send the data to add our new guess to the db
        db.AddGuess(user_id, date, game, score)

    return render_template("add.html")


app.run(debug=True, port=5000)

