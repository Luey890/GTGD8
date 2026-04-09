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

            # Send them back to the homepage
            return redirect("/")


##################################
### New code ends here
##################################

    return render_template("login.html")



app.run(debug=True, port=5000)