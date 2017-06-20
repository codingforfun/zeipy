# /usr/bin/python
# -*- coding: utf-8 -*-
#
#     Characteristics                             Properties       Handle
# --  ------------------------------------------  -------------  --------
#  0  Device Name                                 READ WRITE            3
#  1  Appearance                                  READ                  5
#  2  Peripheral Preferred Connection Parameters  READ                  7
#  3  Manufacturer Name String                    READ                 11
#  4  Model Number String                         READ                 13
#  5  Serial Number String                        READ                 15
#  6  Hardware Revision String                    READ                 17
#  7  Firmware Revision String                    READ                 19
#  8  Software Revision String                    READ                 21
#  9  System ID                                   READ                 23
# 10  PnP ID                                      READ                 25
# 11  Tx Power Level                              READ                 28
# 12  Battery Level                               NOTIFY READ          31
#
# 13  c7e70001-c847-11e6-8175-8c89a55d403c        NOTIFY WRITE         35  # unknown notification
# 14  c7e70012-c847-11e6-8175-8c89a55d403c        READ INDICATE        39  # this is the currently active side
# 15  c7e70011-c847-11e6-8175-8c89a55d403c        READ                 42  # new value on every change (timestamp??)
# 16  c7e70021-c847-11e6-8175-8c89a55d403c        INDICATE             45  # indicates switching off the device
# 17  c7e70022-c847-11e6-8175-8c89a55d403c        WRITE                48
# 18  c7e70041-c847-11e6-8175-8c89a55d403c        WRITE                51
# 19  c7e70042-c847-11e6-8175-8c89a55d403c        WRITE                53

# device goes into sleep after a short period of time if placed with side 0 or 9 up
# device disconnects without indication on HNDL 45
# wakes up by itself if placed on another side after this
# advertices wake up in scanner

# sometimes it disconnects after a while in general


# algorithm should be:
#   scan for device
#   connect device if found
#       register notification
#       wait for notification
#       on BTLEException.DISCONNECTED
#           start discovery
#   on discovery handle
#       reconnect
#   on shutdown of device signal
#       reset internal states to beginning (reset scanner, clear internal data)


from bluepy import btle


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        if cHandle == 39:
            print "Current side up is %i, %r" % (int(data.encode('hex'), 16), zei.readCharacteristic(42))
        elif cHandle == 31:
            print "Battery level: %i" % int(data.encode('hex'), 16)
        else:
            print "Notification from hndl: %s - %r" % (cHandle, data)


# connect
zei = btle.Peripheral('f1:05:a5:9c:2e:9b', 'random', iface=0)
zei._mgmtCmd("pair")

try:
    print zei.status()

    # wait for notifications
    zei.withDelegate(MyDelegate())

    zei.writeCharacteristic(32, b'\x01\x00')  # activate notification about battery level (HNDL31)
    zei.writeCharacteristic(40, b'\x02\x00')  # activate indication of turn (HNDL39)

    zei.writeCharacteristic(36, b'\x01\x00')  # unknown notification
    zei.writeCharacteristic(46, b'\x02\x00')  # indicate switch off/shutdown

    while True:
        if zei.waitForNotifications(1.0):
            continue

finally:
    zei.disconnect()
