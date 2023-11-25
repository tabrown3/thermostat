from smbus2 import SMBus
import time
import requests

bus = SMBus(1)
DEVICE_ADDRESS = 0x49
TEMPERATURE_REG = 0x00
RELAY_URL = "http://localhost:8080/currenttemp"

try:
    while True:
        celsius = bus.read_byte_data(DEVICE_ADDRESS, TEMPERATURE_REG)
        fahrenheit = round((1.8 * celsius) + 32)
        print(fahrenheit)
        res = requests.post(url=RELAY_URL, params={"curTemp":fahrenheit})
        print("Is ok: ", res.ok)
        time.sleep(2)
finally:
    bus.close()