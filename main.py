import argparse
import smbus
import time
import os
import json
import random
import sys
from .THS221 import THS221
from .LPS22HB import LPS22HB
from .LSM6DSL import LSM6DSL
from .LSM303AGR import LSM303AGR


class Sensors:

    def __init__(self, i2c_bus):
        # Initializing the Bus
        self._bus = smbus.SMBus(i2c_bus)

    def read(self):
        # Initializing class THS221 (humidity and temperature)
        self.ths221 = THS221(self._bus)

        # Initializing class LPS22HB (pressure and temperature)
        self.lps22hb = LPS22HB(self._bus)

        # Initializing class LSM6DSL (accelerometer and gyroscope)
        self.lsm6dsl = LSM6DSL(self._bus)

        # Initializing class LSM303AGR (accelerometer and magnetometer)
        self.lsm303agr = LSM303AGR(self._bus)

        # Get humidity and temperature from THS221
        self.humidity = self.ths221.getHumidity()
        self.temperature1 = self.ths221.getTemperature()

        # Get pressure and temperature from LPS22HB
        self.pressure = self.lps22hb.getPressure()
        self.temperature2 = self.lps22hb.getTemperature()

        # Get accelerometer and gyroscope from LSM6DSL
        self.gyroscopeX = self.lsm6dsl.getGyroscopeXAxis()
        self.GAxis = self.lsm6dsl.getGAxes()

        # Get accelerometer and magnetometer from LSM303AGR
        self.accel2 = self.lsm303agr.getAcceleration()
        self.magneto = self.lsm303agr.getMagnetometer()

        # Return object with readed values
        return self.humidity, self.temperature1, self.pressure, self.temperature2, self.gyroscopeX, self.GAxis, self.accel2, self.magneto

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # Closing the Bus
        self._bus.close()
        logging.info('Bus closed')

    def bufclose(self):
        # Closing the Bus
        self._bus.close()


def getSensorsOneShot(smb=1):
    try:
        # Initializing Sensors class
        s = Sensors(smb)

        # Read Sensors values
        hum, temp1, pressure, temp2, accel1, Gaxis, accel2, magneto = s.read()

        # Closing the Bus
        s.bufclose()

        data = {}
        data['hum'] = hum
        data['temp1'] = temp1
        data['pressure'] = pressure
        data['temp2'] = temp2
        data['accel1'] = accel1
        data['Gaxis'] = Gaxis
        data['accel2'] = accel2
        data['magneto'] = magneto
        j = json.dumps(data)
        return j
    except Exception as e:
        return e


def getSensorsOneShotR():
    try:
        # Return random data, for test purposes only
        data = {}
        data['hum'] = random.uniform(20.0, 30.0)
        data['temp1'] = random.uniform(20.0, 22.0)
        data['pressure'] = random.uniform(0.0, 100.0)
        data['temp2'] = data['temp1'] + random.uniform(-0.5, 0.5)
        data['accel1'] = [
            random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0)]
        data['Gaxis'] = [
            random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0)]
        data['accel2'] = [
            random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0)]
        data['magneto'] = [
            random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0), random.uniform(-1000.0, 1000.0)]
        j = json.dumps(data)
        return j
    except Exception as e:
        return e


if __name__ == "__main__":
    args = argparse.ArgumentParser(
        description='X-NUCLEO-IKS01AS library conversion for python3')

    args.add_argument('--bus', '-b', action='store', dest='smb',
                      type=int, default=1, help='I2C Bus')

    params = args.parse_args()

    while True:
        try:
            # Initializing Sensors class
            s = Sensors(params.smb)

            # Read Sensors values
            hum, temp1, pressure, temp2, accel1, Gaxis, accel2, magneto = s.read()

            os.system('cls' if os.name == 'nt' else 'clear')
            print('Hum[%]:      {}'.format(hum))
            print('Temp[C]:     {}'.format(temp1))
            print('Pres[hPa]:   {}'.format(pressure))
            print('Temp2[C]:    {}'.format(temp2))
            print('Acc[mg]:     {}'.format(accel1))
            print('Gyr[mdps]:   {}'.format(Gaxis))
            print('Acc2[mg]:    {}'.format(accel2))
            print('Mag[mGauss]: {}'.format(magneto))
            print('')
            print('')

            # Closing the Bus
            s.bufclose()

            time.sleep(0.1)
        except Exception as e:
            print(e)
            time.sleep(2)
