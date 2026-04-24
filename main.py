import time
from urllib import response

from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)
app.secret_key = "gtg"
app.config.update(
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE=None, # IE11 handles None better than Lax on localhost
)

@app.after_request
def add_security_headers(response):
    # Standard security headers
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # THE IE CACHE KILLERS
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # This header tells IE: "If the session cookie changes, the page must change"
    response.headers["Vary"] = "Cookie"
    
    return response
@app.route("/")
def Home():
    guessData = db.GetAllGuesses() # Note: the new line
    return render_template("index1.html", guesses=guessData) #Note: passing data
@app.route("/login", methods=["GET", "POST"])
def Login():

##################################
### New code starts here
##################################

    # They sent us data, get the username and password
    # then check if their details are correct.
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Did they provide good details
        user = db.CheckLogin(username, password)
        if user:
            # Yes! Save their username and id then
            session['id'] = user['id']
            session['username'] = username
            session.permanent = True
            return redirect("/?cache_bust=" + str(int(time.time())))

            # Send them back to the homepage
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

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            user = db.CheckLogin(username, password)
            if user:
                session['id'] = user['id']
                session['username'] = username
                session.permanent = True
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
        return redirect("/")

    return render_template("add.html")
#@app.route('serviceworker.js')
#def sw():
    return send_from_directory('static/js', 'serviceworker.js')
#@app.route('/manifest.json')
#def serve_manifest():
    return send_from_directory('static/js', 'manifest.json')
##################################
### New code ends here
##################################

app.run(debug=True, port=5000)

