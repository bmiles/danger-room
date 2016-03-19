from autoprotocol import *
from promodules import transformation_module
import json

p = Protocol()


xfm = transformation_module(p, params = {
    "transformation_setup": {
        "bacterial_strain": "xl1",
        "volume": "10:microliter",
        "colonies": 96,
        "warm_incubate": True
        }
    },
    args = {
        "agar_incubation": 30
        })
       
