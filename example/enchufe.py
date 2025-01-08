from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, PLUGIP, PLUGKEY, PLUGVERS, USERNAME, PASSWORD, DEVICE_ID
import logging
import time
from tuya_iot import (
    TuyaOpenAPI,
    AuthType,
    TuyaOpenMQ,
    TuyaDeviceManager,
    TuyaHomeManager,
    TuyaDeviceListener,
    TuyaDevice,
    TuyaTokenInfo,
    TUYA_LOGGER,
    device
)
import tuyapower

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY,AuthType.CUSTOM)
openapi.connect(USERNAME, PASSWORD)

import logging

TUYA_LOGGER.setLevel(logging.DEBUG)

(on, w, mA, V, err) = tuyapower.deviceInfo(DEVICE_ID,PLUGIP,PLUGKEY,PLUGVERS)


flag = True
while True:
    input("Pulsa ...")
    flag = not flag
    commands = {'commands': [{'code': 'switch_1', 'value': flag}]}
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
    tuyapower.devicePrint(DEVICE_ID, PLUGIP, PLUGKEY, PLUGVERS)
    print(" state=%s, W=%s, mA=%s, V=%s [%s]"%(on,w,mA,V,err))
