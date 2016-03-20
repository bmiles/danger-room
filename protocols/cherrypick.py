"""
Analysis will instruct cherryPick to select wells.
"""

from autoprotocol import *
from autoprotocol_utilities import *

def cherryPick(protocol, container_id, wells, round):
    target_plate = p.ref("target", id=None, cont_type="96-flat", storage="cold_4", discard=None)
    spread_plate = ref_kit_container(p, "spread_plate", "6-flat", return_agar_plates()["lb_miller_100ug_ml_amp"], discard=True, store=None)

    for i in range(0,len(wells):
        p.spread(wells[i], spread_plate.wells_from(i, 6/len(wells)), volume)
        i += 6/len(wells)

    p.incubate(spread_plate, "warm_37", "27:hours", shaking=True, co2=0)
    p.dispense_full_plate(ref, "lb-broth-100-ml-amp", "180:microliter")

    # TODO choose equally from all spread wells.
    for i in range(0,len(wells):
        p.autopick(spread_plate.well(0), target_plate.wells_from(0, 96), min_abort=0, criteria={}, dataref='autopick')

    p.cover(target_plate)
    # Grow
    p.incubate(target_plate, "warm_37", "21:hour", shaking=True, co2=0)
    # Induce
    p.stamp(iptg_plate, x_plate, "5:microliter", mix_after=True, mix_vol="100:microliter", repetitions=10, flowrate="25:microliter/second")
    p.incubate(target_plate, "warm_37", "4:hour", shaking=True, co2=0)
    # Data
    p.fluorescence(target_plate, target_plate.wells_from(0, 96), "485:nanometer", "532:nanometer", dataref="fl_result")
    p.absorbance(target_plate, target_plate.wells_from(0, 96), "600:nm", dataref="abs_result")

top_wells = WellGroup([Well(Container(target), 0, None), Well(Container(target), 1, None), Well(Container(target), 2, None)])
cherryPick(p, "ct_id", top_wells)
