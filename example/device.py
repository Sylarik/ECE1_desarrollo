import logging
import time
from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, PLUGIP, PLUGKEY, PLUGVERS, USERNAME, PASSWORD, DEVICE_ID
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
TUYA_LOGGER.setLevel(logging.DEBUG)
# Init
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, AuthType.CUSTOM)

openapi.connect(USERNAME, PASSWORD)
openmq = TuyaOpenMQ(openapi)
openmq.start()

#print("device test-> ", openapi.token_info.uid)
# Get device list
# assetManager = TuyaAssetManager(openapi)
# devIds = assetManager.getDeviceList(ASSET_ID)


# Update device status
deviceManager = TuyaDeviceManager(openapi, openmq)


homeManager = TuyaHomeManager(openapi, openmq, deviceManager)
homeManager.update_device_cache()
# # deviceManager.updateDeviceCaches(devIds)
# device = deviceManager.deviceMap.get(DEVICE_ID)


class tuyaDeviceListener(TuyaDeviceListener):
    def update_device(self, device: TuyaDevice):
        print("_update-->", device)

    def add_device(self, device: TuyaDevice):
        print("_add-->", device)

    def remove_device(self, device_id: str):
        pass


deviceManager.add_device_listener(tuyaDeviceListener())

# Turn on the light
#deviceManager.send_commands(device, [{'code': 'switch_1', 'value': True}])
#time.sleep(1)
#print('status: ', device)

# # Turn off the light
#deviceManager.send_commands(device, [{'code': 'switch_1', 'value': False}])
#time.sleep(1)
#print('status: ', device)
(on, w, mA, V, err) = tuyapower.deviceInfo(DEVICE_ID,PLUGIP,PLUGKEY,PLUGVERS)

flag = True
while True:
    input("............................")
    flag = not flag
    commands = {'commands': [{'code': 'switch_1', 'value': flag}]}
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
    print(" state=%s, W=%s, mA=%s, V=%s [%s]"%(on,w,mA,V,err))