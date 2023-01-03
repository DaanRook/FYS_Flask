from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import mysql.connector

app = Flask(__name__)
#Hier geven we de secret key aan, deze is nodig voor het gebruik van sessies en encryptie en decryptie.
app.secret_key = "BrunoBroodje"
#De maximale tijd dat data mag worden opgeslagen in een sessie.
app.permanent_session_lifetime = timedelta(days=1)

cnx = mysql.connector.connect(user='root',
                             password='Inkkeval@hva22',
                             host='127.0.0.1',
                             database='cor_edb')

cursor = cnx.cursor()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        achternaam = request.form["achternaam"]
        ticketnummer = request.form["ticketnummer"]

        #Query de database voor de 2 waarden die nodig zijn om in te mogen loggen.
        cursor.execute("SELECT * FROM Passagiers WHERE ticketnummer = %s AND achternaam = %s", (ticketnummer, achternaam))
        user = cursor.fetchone()

        #Als de login correct is mag je door naar de landingspagina.
        if user is not None:
            session["username"] = username
            return redirect("/landingspagina")
        
        #Als de login niet kloppend is word er een waarschuwing gegeven.
        else:
            flash("Login failed, try again.")
            return render_template("login.html")
    
    #Als de request method GET is word de login pagina weergeven.
    return render_template("login.html")
        
@app.route("/landingspagina")
def landingspagina():
    #Checkt of de user is ingelogd.
    if "username" in session:
        return render_template("landingspagina.html", username=session["username"])
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    #Haalt de user weg van de sessie.
    session.pop("username", None)
    return redirect("/login")


if __name__ == "__main__":
	app.run(debug=True)