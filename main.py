import time
from urllib import response

from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)
app.secret_key = "gtg"
app.config.update(
    SESSION_PERMANENT=False,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_HTTPONLY=True
)

@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' #Convert all http requests to https
    response.headers['Content-Security-Policy'] = "default-src 'self'" #Tells browser where it can load various types of resource from, in this case only from the server
    response.headers['X-Content-Type-Options'] = 'nosniff' #Don't let the browser guess the content type, it must be what we say it is
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" #Don't cache any pages, always get a fresh copy from the server
    response.headers["Pragma"] = "no-cache" #Older HTTP 1.0 header to prevent caching and included for compatability with older browsers
    response.headers["Expires"] = "0" #Browser knows the content is expired so must check with the server before using any cached version
    response.headers["Vary"] = "Cookie" #If the user is logged in, show different content than if they are not
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
            session.permanent = False
            #return redirect("/?cache_bust=" + str(int(time.time())))

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
                session.permanent = False
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

#Start the server
app.run(debug=True, port=5000)

