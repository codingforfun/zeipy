# -*- coding: utf-8 -*-
#

from bluepy import btle
import struct

import logging
_log = logging.getLogger(__name__)
_log.addHandler(logging.StreamHandler())
_log.setLevel(logging.INFO)


def _ZEI_UUID(short_uuid):
    return 'c7e7%04X-c847-11e6-8175-8c89a55d403c' % (short_uuid)


class ZeiCharBase:

    def __init__(self, periph):
        self.periph = periph
        self.hndl = None

    def enable(self):
        _svc = self.periph.getServiceByUUID(self.svcUUID)
        _chr = _svc.getCharacteristics(self.charUUID)[0]
        self.hndl = _chr.getHandle()

        # this is uint16_t - see: https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
        _cccd = _chr.getDescriptors(btle.AssignedNumbers.client_characteristic_configuration)[0]
        _cccd.write(struct.pack("<H", 2), withResponse=True)


class ZeiOrientationChar(ZeiCharBase):
    svcUUID = _ZEI_UUID(0x0010)
    charUUID = _ZEI_UUID(0x0012)

    def __init__(self, periph):
        ZeiCharBase.__init__(self, periph)


class BatteryLevelChar(ZeiCharBase):
    svcUUID = btle.AssignedNumbers.battery_service
    charUUID = btle.AssignedNumbers.battery_level

    def __init__(self, periph):
        ZeiCharBase.__init__(self, periph)


class Zei(btle.Peripheral):

    def __init__(self, *args, **kwargs):
        btle.Peripheral.__init__(self, *args, **kwargs)
        self.withDelegate(ZeiDelegate(self))

        # activate notifications about turn
        self.orientation = ZeiOrientationChar(self)
        self.orientation.enable()


class ZeiDelegate(btle.DefaultDelegate):

    def __init__(self, periph):
        btle.DefaultDelegate.__init__(self)
        self.parent = periph

    def handleNotification(self, cHandle, data):
        if cHandle == 39:
            _log.info("Current side up is %s", struct.unpack('B', data) )
        else:
            _log.info("Notification from hndl: %s - %r", cHandle, data)


def main():

    zei = Zei('f1:05:a5:9c:2e:9b', 'random', iface=0)

    while True:
        try:
            zei.waitForNotifications(5.0)
        except Exception as e:
            _log.exception(e)

            # todo: Not just connect. Check if device is advertising first.
            zei.connect('f1:05:a5:9c:2e:9b', 'random', iface=0)

    zei.disconnect()


if __name__ == "__main__":
    main()
