# Some experimental code to communicate with Zei° time tracking device
    
## General

Basically Zei° is a Bluetooth LE device. 

It seams to support the following characteristics (check read_characteristics.py)

| SrvUUID   | Service                              |
|:----------|:-------------------------------------|
| 0x1800    | Generic Access                       |
| 0x1804    | Tx Power                             |
| 0x1801    | Generic Attribute                    |
| 0x0010    | c7e70010-c847-11e6-8175-8c89a55d403c | Zei° Orientation Service
| 0x180f    | Battery Service                      |
| 0x0020    | c7e70020-c847-11e6-8175-8c89a55d403c | Zei° LED Button Service
| 0x180a    | Device Information                   |
| 0x0040    | c7e70040-c847-11e6-8175-8c89a55d403c | Zei° Test Service
| 0x0000    | c7e70000-c847-11e6-8175-8c89a55d403c | Zei° DFU Service

Standard. See: https://www.bluetooth.com/specifications/gatt/characteristics

| CharUUID   | Characteristics                            | Properties    |   Handle
|:-----------|:-------------------------------------------|:--------------|---------:
| 0x2a00     | Device Name                                | READ WRITE    |        3 |
| 0x2a01     | Appearance                                 | READ          |        5 |
| 0x2a04     | Peripheral Preferred Connection Parameters | READ          |        7 |
| 0x2a29     | Manufacturer Name String                   | READ          |       11 |
| 0x2a24     | Model Number String                        | READ          |       13 |
| 0x2a25     | Serial Number String                       | READ          |       15 |
| 0x2a27     | Hardware Revision String                   | READ          |       17 |
| 0x2a26     | Firmware Revision String                   | READ          |       19 |
| 0x2a28     | Software Revision String                   | READ          |       21 |
| 0x2a23     | System ID                                  | READ          |       23 |
| 0x2a50     | PnP ID                                     | READ          |       25 |
| 0x2a07     | Tx Power Level                             | READ          |       28 |
| 0x2a19     | Battery Level                              | NOTIFY READ   |       31 |  uint8_t 0 - 100

Zei° specific
| CharUUID   | Characteristics                            | Properties    |   Handle
|:-----------|:-------------------------------------------|:--------------|---------:
| 0x0001     | c7e70001-c847-11e6-8175-8c89a55d403c       | NOTIFY WRITE  |       35 |
| 0x0012     | c7e70012-c847-11e6-8175-8c89a55d403c       | READ INDICATE |       39 |
| 0x0011     | c7e70011-c847-11e6-8175-8c89a55d403c       | READ          |       42 |
| 0x0021     | c7e70021-c847-11e6-8175-8c89a55d403c       | INDICATE      |       45 |
| 0x0022     | c7e70022-c847-11e6-8175-8c89a55d403c       | WRITE         |       48 |
| 0x0041     | c7e70041-c847-11e6-8175-8c89a55d403c       | WRITE         |       51 |
| 0x0042     | c7e70042-c847-11e6-8175-8c89a55d403c       | WRITE         |       53 |

- 0x0001 h35 NOTIFY WRITE -- Switch to DFU Bootloader

- 0x0011 h42 READ         -- Accelerometer
  - 3x uint16_t: x,y,z
- 0x0012 h39 READ INDICATE -- Active side index
  - uint8_t

- 0x0021 h45 INDICATE -- Button pushed indicator
  - uint8_t : 0: short, 1: long
- 0x0022 h48 WRITE -- LED



| 0x0041     | c7e70041-c847-11e6-8175-8c89a55d403c       | WRITE         |       51 |
| 0x0042     | c7e70042-c847-11e6-8175-8c89a55d403c       | WRITE         |       53


    
    
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

