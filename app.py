"""
This is a sketch
"""

from itertools import islice
# from transcriptic import db
from protocols import cherrypick
from protocols import xl1_cloning
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/boot")
def boot():
    s_wells = [0,5,7]
    cherrypick.cherryPick("ct_id", s_wells)
    return 'Booted'

@app.route("/updates", methods=['GET', 'POST'])
def updates():
    if request.method == 'POST':
        print request.method
        return "even processed"
        cherryPick("ct_id", s_wells)
    elif request.method == 'GET':
        print request.method
        return "this is the updates endpoint"
    else:
        pass

class TranscripticEvent(object):
    def handleEvent(self, event):
        pass

class Mutator(object):
    def protocol(self, aliquots):
        pass

class HydrogenPeroxide(Mutator):
    def protocol(self, aliquots):
        pass

class Objective(object):
    def protocol(self):
        pass
    def score(self, data):
        pass

class FluorescenceObjective(Objective):
    def protocol(self, excitation, emission):
        pass
    def score(self, data):
        pass

# strains = islice(sorted(
#     db.findStrains(projectId = 'p1swift'}),
#     key = lambda x: x['metadata']['evolver-score']
# ), 20)
#
# if len(strains) < 10:
#     # bootstrap
#     pass
#
# evolver = Evolver(
#     mutator = HydrogenPeroxide(),
#     objective = FluorescenceObjective(428, 535),
#     initial = strains
# )

if __name__ == "__main__":
    app.run()

# evolver.run(8080, '/webhook')
