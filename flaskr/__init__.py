from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import mysql.connector

app = Flask(__name__)
#Hier geven we de secret key aan, deze is nodig voor het gebruik van sessies en encryptie en decryptie.
app.secret_key = "BrunoBroodje"
#De maximale tijd dat data mag worden opgeslagen in een sessie.
app.permanent_session_lifetime = timedelta(days=1)

cnx = mysql.connector.connect(user='root',
                             password='Rookie1241',
                             host='localhost',
                             database='cor_edb')

cursor = cnx.cursor()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        achternaam = request.form["achternaam"].lower()
        ticketnummer = request.form["ticketnummer"]

        #Maak het zo dat de ingevoerde waarde voor achternaam alles kan zijn (kleine letter/grote letter) zolang het de goede naam is.
        #Eerst word de naam klein gemaakt en daarna krijgt hij een hoofdletter zodat de naam goed geprint word op de landingspagina.
        achternaam = achternaam.capitalize()

        #Query de database voor de 2 waarden die nodig zijn om in te mogen loggen.
        cursor.execute("SELECT * FROM passagier WHERE ticketnummer = %s AND achternaam = %s", (ticketnummer, achternaam))
        user = cursor.fetchone()

        #Als de login correct is mag je door naar de landingspagina.
        if user is not None:
            session["achternaam"] = achternaam
            return redirect("/landingspage")
        
        #Als de login niet kloppend is word er een waarschuwing gegeven.
        else:
            flash("Login failed, try again.")
            return render_template("login.html")
    
    #Als de request method GET is word de login pagina weergeven.
    return render_template("login.html")
        
@app.route("/landingspage")
def landingspagina():
    #Checkt of de user is ingelogd.
    if "achternaam" in session:
        return render_template("landingspage.html", achternaam=session["achternaam"])
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    #Haalt de user weg van de sessie.
    session.pop("achternaam", None)
    flash('You were logged out! Please login again if you want to use the internet.')
    return redirect("/login")

@app.route("/entertainmentpage")
def entertainmentpage():
    if "achternaam" in session:
        return render_template("entertainmentpage.html", achternaam=session["achternaam"])
    else:
        return redirect("/login")

@app.route("/weatherpage")
def weatherpage():
    if "achternaam" in session:
        return render_template("weatherpage.html", achternaam=session["achternaam"])
    else:
        return redirect("/login")

@app.route("/infopage")
def infopage():
    achternaam = session["achternaam"]
    if "achternaam" in session:
        cursor.execute("SELECT * FROM passagier WHERE achternaam = %s", (achternaam,))
        row = cursor.fetchone()
        return render_template("infopage.html", row=row, achternaam=session["achternaam"])
    else:
        return redirect("/login")


if __name__ == "__main__":
	app.run(debug=True)