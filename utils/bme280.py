import smbus2
import bme280
import time

def calcula_temp_ambiente():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)
    time.sleep(0.5)
    data = bme280.sample(bus, address, calibration_params)
    # the compensated_reading class has the following attributes
    print(data.temperature)
    return data.temperature