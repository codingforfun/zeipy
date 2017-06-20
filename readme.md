# Some experimental code to communicate with Zei° time tracking device
    
## General

Basically Zei° is a Bluetooth LE device. 

It seams to support the following characteristics (check read_characteristics.py)

| Idx | Characteristics                            | Properties    |   Handle | Notes 
| --- | ------------------------------------------ | ------------- | -------- | ------
|     | Standard profiles                          |               |          |
|  0  | Device Name                                | READ WRITE    |        3 |
|  1  | Appearance                                 | READ          |        5 |
|  2  | Peripheral Preferred Connection Parameters | READ          |        7 |
|  3  | Manufacturer Name String                   | READ          |       11 |
|  4  | Model Number String                        | READ          |       13 |
|  5  | Serial Number String                       | READ          |       15 |
|  6  | Hardware Revision String                   | READ          |       17 |
|  7  | Firmware Revision String                   | READ          |       19 |
|  8  | Software Revision String                   | READ          |       21 |
|  9  | System ID                                  | READ          |       23 |
| 10  | PnP ID                                     | READ          |       25 |
| 11  | Tx Power Level                             | READ          |       28 |
| 12  | Battery Level                              | NOTIFY READ   |       31 |
|     |                                            |               |          |
|     | Zei° specific                              |               |          |
| 13  | c7e70001-c847-11e6-8175-8c89a55d403c       | NOTIFY WRITE  |       35 | unknown notification
| 14  | c7e70012-c847-11e6-8175-8c89a55d403c       | READ INDICATE |       39 | this is the currently active side
| 15  | c7e70011-c847-11e6-8175-8c89a55d403c       | READ          |       42 | new value on every change (timestamp??)
| 16  | c7e70021-c847-11e6-8175-8c89a55d403c       | INDICATE      |       45 | indicates switching off the device
| 17  | c7e70022-c847-11e6-8175-8c89a55d403c       | WRITE         |       48 | unknown (probably for firmware update?)
| 18  | c7e70041-c847-11e6-8175-8c89a55d403c       | WRITE         |       51 |
| 19  | c7e70042-c847-11e6-8175-8c89a55d403c       | WRITE         |       53 |
    
    
## Current state
    
+ `test.py` has a small example that basically already reads everything interesting from the device.
+ `read_characteristics.py` dumps all the BTLE characteristics 
+ `discover.py` has a very basic discovery example (note: you need to have root permissions for scanning)
+ `scan.py` has a very basic scanning example

+ Basic communication with the device is straight forward and seams to work, however there are still open questions. 
  + If you press the OFF switch the device sends notification about shutdown to HNDL45.
    - The software should stop tracking in this case.
    - Is Zei° still bonded on the next connection attempt? 
  + If the device is placed on the base (Side 0 or 9) it's going to sleep and the connections is lost. 
    - No notification on HNDL45 -> do not stop tracking.
    - How to resume if it wakes up again? I think we need to catch the connection lost and start scanning for advertisements until it wakes up again.
    - Zei° seams to wake up again if placed on one of the other sides again
    - I think the same also happens after a while without moving Zei°
  + What data comes from HNDL42? How is the format? How to decode? 
  + What are all the other undocumented characteristics for? 
  
   
Example traffic
```bash
>$ python test.py

{'sec': ['low'], 'state': ['conn'], 'rsp': ['stat'], 'dst': ['f1:05:a5:9c:2e:9b'], 'mtu': [0]}
Current side up is 8, '\xe0\xff\xff\xff\xc0\xfc\xff\xff\x80\x02\x00\x00'
Battery level: '\x1c'
Current side up is 5, '\xb0\xfc\xff\xff\x10\x00\x00\x00p\x02\x00\x00'
Current side up is 0, '`\xfe\xff\xff@\x00\x00\x00\xb0\x03\x00\x00'
Notification from hndl: 45 - '\x01'    <--(after pressing switch off)
```

