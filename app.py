import os
import sys
from flask import Flask, render_template, request, session, redirect


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classes.agency import Agency
from classes.mission import Mission
from classes.astronaut import Astronaut
from classes.agencyMission import AgencyMission
from classes.userlogin import Userlogin

import subs.index_subs as indexSubs
from subs.apps_userlogin import apps_userlogin

app = Flask(__name__)
app.secret_key = 'cosmic-secret-key-for-sessions'

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "space_missions.db")


Agency.read(db_path)
Mission.read(db_path)
Astronaut.read(db_path)
AgencyMission.read(db_path)
Userlogin.read(db_path)


if len(Agency.lst) > 0: Agency.first()
if len(Mission.lst) > 0: Mission.first()
if len(Astronaut.lst) > 0: Astronaut.first()
if len(AgencyMission.lst) > 0: AgencyMission.first()
if len(Userlogin.lst) > 0: Userlogin.first()

@app.route("/", methods=["POST", "GET"])
def index():
    if session.get("user") is None:
        return redirect("/login")
    return indexSubs.index(db_path)

@app.route("/login")
def login():
    return render_template("login.html", user="", password="", ulogin=session.get("user"), resul="")

@app.route("/logoff")
def logoff():
    session.pop("user", None)
    return redirect("/login")

@app.route("/chklogin", methods=["POST", "GET"])
def chklogin():
    user = request.form.get("user", "")
    password = request.form.get("password", "")
    resul = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        return redirect("/")
    return render_template("login.html", user=user, password=password, ulogin=session.get("user"), resul=resul)

@app.route("/Userlogin", methods=["POST", "GET"])
def userlogin():
    if session.get("user") is None:
        return redirect("/login")
    return apps_userlogin()

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(port=port)
