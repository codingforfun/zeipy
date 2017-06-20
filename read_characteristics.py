# -*- coding: utf-8 -*-
#
#

from bluepy import btle
from tabulate import tabulate


# connect (enter your own devices MAC address of course)
zei = btle.Peripheral('f1:05:a5:9c:2e:9b', 'random', iface=1)


try:
    data=[]
    for i, c in enumerate(zei.getCharacteristics()):
        data.append((i, c.uuid.getCommonName(), c.propertiesToString(), c.getHandle()))

    print tabulate(tabular_data=data,
                   headers=["", "Characteristics", "Properties", "Handle"])

finally:
    zei.disconnect()


