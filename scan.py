# -*- coding: utf-8 -*-
#
#

from bluepy import btle

sc = btle.Scanner(1)
for s in sc.scan():
    print "%s %s %s %s" % (s.getValueText(9), s.iface, s.addr, s.addrType)
