import os
import sys
from flask import Flask


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classes.agency import Agency
from classes.mission import Mission
from classes.astronaut import Astronaut
from classes.agencyMission import AgencyMission

import subs.index_subs as indexSubs

app = Flask(__name__)
app.secret_key = 'cosmic-secret-key-for-sessions'

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "space_missions.db")


Agency.read(db_path)
Mission.read(db_path)
Astronaut.read(db_path)
AgencyMission.read(db_path)


if len(Agency.lst) > 0: Agency.first()
if len(Mission.lst) > 0: Mission.first()
if len(Astronaut.lst) > 0: Astronaut.first()
if len(AgencyMission.lst) > 0: AgencyMission.first()

@app.route("/", methods=["POST", "GET"])
def index():
    return indexSubs.index(db_path)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, port=port)
