"""
Makes a stock plate of IPTG that provides a full plate worth of induction
doses at least 5 times.
"""
# TODO add accurate volume sufficient for 5 doses
from autoprotocol import *
from promodules import transformation_module
import json

p = Protocol()

iptg_plate = p.ref(iptg_plate_date, id=None, cont_type="96-pcr", storage="cold_20", discard=None)
p.provision("iptg", iptg_plate.all_wells(), "50:microliter")
p.seal(iptg_plate)
