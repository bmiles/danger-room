"""
Analysis will instruct cherryPick to select wells.
"""

from autoprotocol import *
from autoprotocol_utilities import *
import json
def cherryPick(container_id, selected_wells):
    p = Protocol()
    source_plate = p.ref("source", id=container_id, cont_type="96-flat", storage="cold_4", discard=None)
    target_plate = p.ref("target", id=None, cont_type="96-flat", storage="cold_4", discard=None)
    spread_plate = ref_kit_container(p, "spread_plate", "6-flat", return_agar_plates()["lb_miller_100ug_ml_amp"], discard=True, store=None)
    iptg_plate = p.ref("iptg_plate", id=None, cont_type="96-flat", storage="cold_4", discard=None)

    top_wells = source_plate.wells(selected_wells)

    for i in range(0,len(top_wells)):
        for dest_well in spread_plate.wells_from(i, 6/len(top_wells)):
            p.spread(top_wells[i], dest_well, volume="50:microliter")
        i += 6/len(top_wells)

    p.incubate(spread_plate, "warm_37", "27:hours", shaking=True, co2=0)
    p.dispense_full_plate(target_plate, "lb-broth-100-ml-amp", "180:microliter")

    # TODO choose equally from all spread wells.
    for i in range(0,len(top_wells)):
        p.autopick(spread_plate.wells_from(i, 6/len(top_wells)), target_plate.wells_from(i, 96/(6/len(top_wells))), min_abort=0, criteria={}, dataref='autopick_%s' % i)
        i += 6/len(top_wells)

    p.cover(target_plate)
    # Grow
    p.incubate(target_plate, "warm_37", "21:hour", shaking=True, co2=0)
    # Induce
    p.stamp(iptg_plate, target_plate, "5:microliter", mix_after=True, mix_vol="100:microliter", repetitions=10, flowrate="25:microliter/second")
    p.incubate(target_plate, "warm_37", "4:hour", shaking=True, co2=0)
    # Data
    p.fluorescence(target_plate, target_plate.wells_from(0, 96), "485:nanometer", "532:nanometer", dataref="fl_result")
    p.absorbance(target_plate, target_plate.wells_from(0, 96), "600:nm", dataref="abs_result")
    print json.dumps(p.as_dict())

s_wells = [0,5,7]

cherryPick("ct_id", s_wells)
