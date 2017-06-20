# -*- coding: utf-8 -*-
#
#

from bluepy import btle
from tabulate import tabulate

def short_uuid_str(uuid):
    return "0x%s" % (str(uuid)[4:8])



# connect (enter your own devices MAC address of course)
zei = btle.Peripheral('f1:05:a5:9c:2e:9b', 'random', iface=0)


try:
    srv_data = []
    for s in zei.getServices():
        srv_data.append((short_uuid_str(s.uuid), s.uuid.getCommonName()))

    char_data=[]
    for c in zei.getCharacteristics():
        char_data.append((short_uuid_str(c.uuid), c.uuid.getCommonName(), c.propertiesToString(), c.getHandle()))

    print tabulate(tabular_data=srv_data,
                   headers=[ "SrvUUID", "Service"],
                   tablefmt="pipe")

    print ""

    print tabulate(tabular_data=char_data,
                   headers=["CharUUID", "Characteristics", "Properties", "Handle"],
                   tablefmt="pipe")

finally:
    zei.disconnect()


