#import libraries
import math 
import time

from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)
app.secret_key = "gtg"
app.config.update(
    SESSION_PERMANENT=False,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # Only send cookie over HTTPS
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

@app.route("/") #the route for the homepage
def Home():
    #guessData = db.GetAllGuesses() # Note: the new line
    page = request.args.get('page', 1, type=int) #Get the page number from the query parameters and default to 1 if not provided
    per_page = 10 #Limit guesses to 10 per page
    offset = (page - 1) * per_page #Calculate the offset for the database query based on the current page
    guessData = db.GetPages(per_page, offset) #Get the guesses for the current page using limit and offset
    total_guesses = db.TotalGuessCount() #Get the total number of guesses from the guesses database
    total_pages = math.ceil(total_guesses / per_page)#Calculate the total number of pages and round up to the nearest whole number
    return render_template("index1.html", guesses=guessData, page=page, total_pages=total_pages) #Note: passing data, page and total_pages

#the route for the login page
@app.route("/login", methods=["GET", "POST"])
def Login():
    if session.get('username'): #if the user is logged in, redirect them to the homepage
        return redirect("/")

    # They sent us data, get the username and password
    # then check if their details are correct.
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Did they provide good details
        user = db.CheckLogin(username, password)
        if user:
            # Yes! Save their username and id then
            session.clear()
            session['id'] = user['id']
            session['username'] = username
            session.permanent = False

            # Send them back to the homepage
            return redirect("/")

    return render_template("login.html")

#the route for logout
@app.route("/logout")
def Logout():
    session.clear() #Clears all session data
    return redirect("/") #Redirects the user to the homepage

#the route for the register page
@app.route("/register", methods=["GET", "POST"])
def Register():

    #If they are already logged in then send them to the homepage as they don't need to register
    if session.get('username'): 
        return redirect("/")
    #Get the username and password the user sends and add to database
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
            return redirect("/") #Redirects to homepage after registering
    return render_template("register.html")

#the route for adding a new guess
@app.route("/add", methods=["GET","POST"])
def Add():
    #if user is not logged in, send them to the homepage
    if session.get('username') == None:
        return redirect("/")


    # Did they click submit?
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        show = request.form['show']
        score = request.form['score']

        # Send the data to add our new guess to the db
        db.AddGuess(user_id, date, show, score)
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

