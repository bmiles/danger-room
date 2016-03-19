"""
This is a sketch
"""

from itertools import islice
from transcriptic import db

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

strains = islice(sorted(
    db.findStrains(projectId = 'p1swift'}),
    key = lambda x: x['metadata']['evolver-score']
), 20)

if len(strains) < 10:
    # bootstrap
    pass

evolver = Evolver(
    mutator = HydrogenPeroxide(),
    objective = FluorescenceObjective(428, 535),
    initial = strains
)

evolver.run(8080, '/webhook')
