"""
Boostraps the mutation process by inserting a gene containing plasmid into the
XL-1 mutator strain and initiates the first culture and fluorescence read.
"""


# TODO Needs pUC 18 control transformation per agar plate.
# TODO Needs to plate a full agar plate in order to generate 96 picks
# TODO prewarm SOC media



from autoprotocol import *
from promodules import transformation_module
from autoprotocol_utilities import *
import json

p = Protocol()



num_xfm = 1
xl1_res = "resource"#resource id for xl1
xl1_quant = num_xfm * Unit(100, "microliter")


dna = p.ref("dna", id=None, cont_type="micro-1.5", storage="cold_20", discard=None)
cells = p.ref("xl1", id=None, cont_type="micro-1.5", storage=None, discard=True)
soc = p.ref("soc", id=None, cont_type="micro-1.5", storage=None, discard=True)
x_plate = p.ref("xf_plate", id=None, cont_type="96-pcr", storage=None, discard=True)
b_mercap = p.ref("b_mercap", id=None, cont_type="micro-1.5", storage="ambient", discard=None)
spread_plate = ref_kit_container(protocol=p, name="spread_plate", container="6-flat", kit_id=return_agar_plates()["lb_miller_100ug_ml_amp"],discard=False, store="cold_4")
cult_plate = p.ref("cult_plate", id=None, cont_type="96-flat", storage="cold_4", discard=None)
iptg_plate =  p.ref("iptg_plate", id=None, cont_type="96-flat", storage="cold_4", discard=None)

xfm_wells = x_plate.wells_from(0, num_xfm)

p.provision(xl1_res, cells.well(0), xl1_quant)


p.incubate(x_plate, "cold_20", "30:minute", shaking=False, co2=0)
p.mix(cells.well(0), 0.25 * xl1_quant, speed="25:microliter/second", repetitions=10)

for well in xfm_wells:
    p.transfer(cells.well(0), well, "100:microliter")
    p.transfer(b_mercap.well(0), well, "1.7:microliter")

for i in range(0,5):
    for well in xfm_wells:
        p.mix(well, "50:microliter", speed="10:microliter/second", repetitions=10)
    p.thermocycle(x_plate, [
        {"cycles": 1,
            "steps": [{
                "temperature": "0:celsius",
                "duration": "2:minute",
                }]
        }
    ])


for well in xfm_wells:
    p.transfer(dna.well(0), well, "2:microliter")

p.incubate(x_plate, "cold_4", "30:minute", shaking=False, co2=0)
p.thermocycle(x_plate, [
    {"cycles": 1,
        "steps": [{
            "temperature": "42:celsius",
            "duration": "45:second",
            },
            {
                "temperature": "0:celsius",
                "duration": "2:minute",
            }
        ]
    }
])

for well in xfm_wells:
    p.transfer(soc.well(0), well, "900:microliter")  # exceeds well volume
p.incubate(x_plate, "warm_37", "1:hour", shaking=False, co2=0)

p.dispense_full_plate(cult_plate, "lb-broth-100-ml-Amp", "150:microliter")

for well in xfm_wells:
    p.spread(well, spread_plate.well(well.index), volume="50:microliter")
p.incubate(spread_plate, "warm_37", "25:hour", shaking=False, co2=0)
p.autopick(spread_plate.well(0), cult_plate.wells_from(0, 96), min_abort=0, criteria={}, dataref='autopick')
p.cover(cult_plate)
# Grow
p.incubate(cult_plate, "warm_37", "12:hour", shaking=True, co2=0)
# Induce
p.unseal(iptg_plate)
p.stamp(iptg_plate, x_plate, "5:microliter", mix_after=True, mix_vol="100:microliter", repetitions=10, flowrate="25:microliter/second")
p.seal(iptg_plate)
p.incubate(cult_plate, "warm_37", "4:hour", shaking=True, co2=0)
# Data
p.fluorescence(cult_plate, cult_plate.wells_from(0, 96), "485:nanometer", "532:nanometer", dataref="fl_reuslt")

print json.dumps(p.as_dict())

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
