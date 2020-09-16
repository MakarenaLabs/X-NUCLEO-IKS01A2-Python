import smbus
import time
from .utils import *


class THS221:
    # Humidity and temperature sensor
    HTS221_H0_RH_X2 = 0x30
    HTS221_H1_RH_X2 = 0x31
    HTS221_T0_DEGC_X8 = 0x32
    HTS221_T1_DEGC_X8 = 0x33
    HTS221_T0_T1_DEGC_H2 = 0x35
    HTS221_H0_T0_OUT_L = 0x36
    HTS221_H0_T0_OUT_H = 0x37
    HTS221_H1_T0_OUT_L = 0x3A
    HTS221_H1_T0_OUT_H = 0x3B
    HTS221_T0_OUT_L = 0x3C
    HTS221_T0_OUT_H = 0x3D
    HTS221_T1_OUT_L = 0x3E
    HTS221_T1_OUT_H = 0x3F
    HTS221_I2C_ADDRESS = 0xBE
    HTS221_HR_OUT_L_REG = 0x28
    HTS221_TEMP_OUT_L_REG = 0x2A
    HTS221_CTRL_REG1 = 0x20
    HTS221_PD_MASK = 0x80
    HTS221_BDU_MASK = 0x04
    HTS221_ODR_MASK = 0x03
    HTS221_ENABLE = 1
    HTS221_BDU_BIT = 2
    HTS221_ODR_1HZ = 0x01

    def enable(self):
        r = self.HTS221_ReadRegRaw(self.HTS221_CTRL_REG1, 1)
        r[0] |= self.HTS221_PD_MASK
        self.HTS221_WriteRegRaw(self.HTS221_CTRL_REG1, 1, r)

    def setBdu(self):
        r = self.HTS221_ReadRegRaw(self.HTS221_CTRL_REG1, 1)
        r[0] &= ~self.HTS221_BDU_MASK
        r[0] |= self.HTS221_ENABLE << self.HTS221_BDU_BIT
        self.HTS221_WriteRegRaw(self.HTS221_CTRL_REG1, 1, r)
        r = self.HTS221_ReadRegRaw(self.HTS221_CTRL_REG1, 1)
        r[0] &= ~self.HTS221_ODR_MASK
        r[0] |= self.HTS221_ODR_1HZ
        self.HTS221_WriteRegRaw(self.HTS221_CTRL_REG1, 1, r)

    def __init__(self, i2c_bus):
        self._bus = i2c_bus
        self.enable()
        self.setBdu()

    def HTS221_WriteRegRaw(self, RegAddr, NumByteToRead, data):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        for i in data:
            self._bus.write_byte_data(
                (((self.HTS221_I2C_ADDRESS) >> 1) & 0x7F), RegAddr, i)
            # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.HTS221_I2C_ADDRESS) >> 1) & 0x7F)))

        return raw

    def HTS221_ReadRegRaw(self, RegAddr, NumByteToRead):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        self._bus.write_byte(
            (((self.HTS221_I2C_ADDRESS) >> 1) & 0x7F), RegAddr)
        # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.HTS221_I2C_ADDRESS) >> 1) & 0x7F)))

        return raw

    def getHumidity(self):
        # self.setBdu()
        buffer0 = self.HTS221_ReadRegRaw(self.HTS221_H0_RH_X2, 2)
        H0_rh = buffer0[0] >> 1
        H1_rh = buffer0[1] >> 1

        buffer1 = self.HTS221_ReadRegRaw(self.HTS221_H0_T0_OUT_L, 2)
        H0_T0_out = ((buffer1[1]) << 8) | buffer1[0]

        buffer2 = self.HTS221_ReadRegRaw(self.HTS221_H1_T0_OUT_L, 2)
        H1_T0_out = ((buffer2[1]) << 8) | buffer2[0]

        buffer3 = self.HTS221_ReadRegRaw(self.HTS221_HR_OUT_L_REG, 2)
        H_T_out = ((buffer3[1]) << 8) | buffer3[0]

        tmp_f = float(H_T_out - H0_T0_out) * float(H1_rh - H0_rh) / \
            float(H1_T0_out - H0_T0_out) + H0_rh

        return tmp_f

    def getTemperature(self):
        # self.setBdu()
        buffer0 = self.HTS221_ReadRegRaw(self.HTS221_T0_DEGC_X8, 2)
        tmp = self.HTS221_ReadRegRaw(self.HTS221_T0_T1_DEGC_H2, 1)

        T0_degC_x8_u16 = ((tmp[0] & 0x03) << 8) | buffer0[0]
        T1_degC_x8_u16 = ((tmp[0] & 0x0C) << 6) | buffer0[1]
        T0_degC = T0_degC_x8_u16 >> 3
        T1_degC = T1_degC_x8_u16 >> 3

        buffer2 = self.HTS221_ReadRegRaw(self.HTS221_T0_OUT_L, 4)
        T0_out = twoComplements(buffer2[1], buffer2[0])
        T1_out = twoComplements(buffer2[3], buffer2[2])

        buffer3 = self.HTS221_ReadRegRaw(self.HTS221_TEMP_OUT_L_REG, 2)

        T_out = twoComplements(buffer3[1], buffer3[0])

        tmp_f = float(T_out - T0_out) * float(T1_degC - T0_degC) / \
            float(T1_out - T0_out) + float(T0_degC)

        return tmp_f
