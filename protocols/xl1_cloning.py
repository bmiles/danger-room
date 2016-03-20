from autoprotocol import *
from promodules import transformation_module
import json

p = Protocol()

pGFP = p.ref("gfp", id=None, cont_type="micro-1.5", storage="cold_20", discard=None)
cells = p.ref("xl1", id=None, cont_type="micro-1.5", storage=None, discard=True)
soc = p.ref("soc", id=None, cont_type="micro-1.5", storage=None, discard=True)
x_plate = p.ref("xf_plate", id=None, cont_type="96-pcr", storage=None, discard=True)
b_mercap = p.ref("b_mercap", id=None, cont_type="micro-1.5", storage="ambient", discard=None)
spread_plate = p.ref(name, id=None, cont_type="cont_type", storage=None, discard=None)
cult_plate = p.ref("cult_plate", id=None, cont_type="96-flat", storage="cold_4", discard=None)

p.mix(cells.well(0), "100:microliter", speed="25:microliter/second", repetitions=10)
p.incubate(x_plate, "cold_20", "30:minute", shaking=False, co2=0)
p.transfer(cells.well(0), x_plate.well(0), "100:microliter")
p.transfer(b_mercap.well(0), x_plate.well(0), "1.7:microliter")
for i in irange(0, 5):
    p.mix(x_plate.well(0), "50:microliter", speed="10:microliter/second", repetitions=10)
    p.incubate(x_plate, "cold_4", "2:minute", shaking=False, co2=0)
    i += 1
p.transfer(cell.well(0), x_plate.well(0), "2:microliter")
p.incubate(x_plate, cold_4, "30:minute", shaking=False, co2=0)
p.thermocycle(x_plate, [
             {"cycles": 1,
              "steps": [{
                "temperature": "42:celsius",
                "duration": "45:second",
                },
                {
                  "temperature": "0:celsius",
                  "duration": "2:minute",
                }]
            }])

p.transfer(soc.well(0), x_plate.well(0), "900:microliter")
p.incubate(x_plate, "warm_37", "1:hour", shaking=False, co2=0)
p.spread(x_plate.well(0), spread_plate.wells_from(0, 2), "50:microliter")
p.incubate(spread_plate, "warm_37", "25:hour", shaking=False, co2=0)
p.autopick(spread_plate, cult_plate.wells_from(0, 96), min_count=0)
p.cover(cult_plate)
p.incubate(cult_plate, "warm_37", "16:hour", shaking=True, co2=0)
p.fluorescence(cult_plate, cult_plate.wells_from(0, 96), "485:nanometer", "532:nanometer", dataref=fl_reuslt)


# xfm = transformation_module(p, params = {
#     "transformation_setup": {
#         "bacterial_strain": "xl1",
#         "volume": "10:microliter",
#         "colonies": 96,
#         "warm_incubate": True
#         },
#     "transformations": [
#         {"group_label": "name",
#          "dna": pGFP.wells_from(0, 3),
#          "media_type": "lb-broth-noAB"
#         }]
#     },
#     args = {
#         "agar_incubation": 30
#         })
