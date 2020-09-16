import smbus
import time
from .utils import *


class LSM6DSL:
    # accelerometro and gyroscope sensor
    LSM6DSL_ACC_GYRO_I2C_ADDRESS_HIGH = 0xD6
    LSM6DSL_ACC_GYRO_OUTX_L_XL = 0X28
    LSM6DSL_ACC_GYRO_CTRL1_XL = 0X10
    LSM6DSL_ACC_GYRO_FS_XL_2g = 0x00
    LSM6DSL_ACC_GYRO_FS_XL_16g = 0x04
    LSM6DSL_ACC_GYRO_FS_XL_4g = 0x08
    LSM6DSL_ACC_GYRO_FS_XL_8g = 0x0C
    LSM6DSL_ACC_SENSITIVITY_FOR_FS_2G = 0.061
    LSM6DSL_ACC_SENSITIVITY_FOR_FS_4G = 0.122
    LSM6DSL_ACC_SENSITIVITY_FOR_FS_8G = 0.244
    LSM6DSL_ACC_SENSITIVITY_FOR_FS_16G = 0.488
    LSM6DSL_ACC_GYRO_FS_XL_MASK = 0x0C

    LSM6DSL_ACC_GYRO_OUTX_L_G = 0X22
    LSM6DSL_ACC_GYRO_CTRL2_G = 0X11
    LSM6DSL_ACC_GYRO_FS_125_MASK = 0x02
    LSM6DSL_ACC_GYRO_FS_125_ENABLED = 0x02
    LSM6DSL_ACC_GYRO_FS_125_DISABLED = 0x00
    LSM6DSL_GYRO_SENSITIVITY_FOR_FS_125DPS = 04.375
    LSM6DSL_GYRO_SENSITIVITY_FOR_FS_245DPS = 08.750
    LSM6DSL_GYRO_SENSITIVITY_FOR_FS_500DPS = 17.500
    LSM6DSL_GYRO_SENSITIVITY_FOR_FS_1000DPS = 35.000
    LSM6DSL_GYRO_SENSITIVITY_FOR_FS_2000DPS = 70.000
    LSM6DSL_ACC_GYRO_FS_G_MASK = 0x0C
    LSM6DSL_ACC_GYRO_FS_G_245dps = 0x00
    LSM6DSL_ACC_GYRO_FS_G_500dps = 0x04
    LSM6DSL_ACC_GYRO_FS_G_1000dps = 0x08
    LSM6DSL_ACC_GYRO_FS_G_2000dps = 0x0C

    LSM6DSL_ACC_GYRO_IF_INC_ENABLED = 0x04
    LSM6DSL_ACC_GYRO_BDU_BLOCK_UPDATE = 0x40
    LSM6DSL_ACC_GYRO_FIFO_MODE_BYPASS = 0x00
    LSM6DSL_ACC_GYRO_ODR_XL_POWER_DOWN = 0x00
    LSM6DSL_ACC_GYRO_ODR_G_POWER_DOWN = 0x00

    LSM6DSL_ACC_GYRO_CTRL3_C = 0X12
    LSM6DSL_ACC_GYRO_BDU_MASK = 0x40
    LSM6DSL_ACC_GYRO_FIFO_CTRL5 = 0X0A
    LSM6DSL_ACC_GYRO_FIFO_MODE_MASK = 0x07
    LSM6DSL_ACC_GYRO_ODR_XL_MASK = 0xF0
    LSM6DSL_ACC_GYRO_IF_INC_MASK = 0x04

    LSM6DSL_ACC_GYRO_ODR_XL_POWER_DOWN = 0x00
    LSM6DSL_ACC_GYRO_ODR_XL_13Hz = 0x10
    LSM6DSL_ACC_GYRO_ODR_XL_26Hz = 0x20
    LSM6DSL_ACC_GYRO_ODR_XL_52Hz = 0x30
    LSM6DSL_ACC_GYRO_ODR_XL_104Hz = 0x40
    LSM6DSL_ACC_GYRO_ODR_XL_208Hz = 0x50
    LSM6DSL_ACC_GYRO_ODR_XL_416Hz = 0x60
    LSM6DSL_ACC_GYRO_ODR_XL_833Hz = 0x70
    LSM6DSL_ACC_GYRO_ODR_XL_1660Hz = 0x80
    LSM6DSL_ACC_GYRO_ODR_XL_3330Hz = 0x90
    LSM6DSL_ACC_GYRO_ODR_XL_6660Hz = 0xA0

    LSM6DSL_ACC_GYRO_ODR_G_POWER_DOWN = 0x00
    LSM6DSL_ACC_GYRO_ODR_G_13Hz = 0x10
    LSM6DSL_ACC_GYRO_ODR_G_26Hz = 0x20
    LSM6DSL_ACC_GYRO_ODR_G_52Hz = 0x30
    LSM6DSL_ACC_GYRO_ODR_G_104Hz = 0x40
    LSM6DSL_ACC_GYRO_ODR_G_208Hz = 0x50
    LSM6DSL_ACC_GYRO_ODR_G_416Hz = 0x60
    LSM6DSL_ACC_GYRO_ODR_G_833Hz = 0x70
    LSM6DSL_ACC_GYRO_ODR_G_1660Hz = 0x80
    LSM6DSL_ACC_GYRO_ODR_G_3330Hz = 0x90
    LSM6DSL_ACC_GYRO_ODR_G_6660Hz = 0xA0

    LSM6DSL_ACC_GYRO_ODR_G_MASK = 0xF0

    def LSM6DSL_ACC_GYRO_W_IF_Addr_Incr(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(self.LSM6DSL_ACC_GYRO_CTRL3_C, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_IF_INC_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(self.LSM6DSL_ACC_GYRO_CTRL3_C, 1, r)

    def LSM6DSL_ACC_GYRO_W_BDU(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(self.LSM6DSL_ACC_GYRO_CTRL3_C, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_BDU_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(self.LSM6DSL_ACC_GYRO_CTRL3_C, 1, r)

    def LSM6DSL_ACC_GYRO_W_FIFO_MODE(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(
            self.LSM6DSL_ACC_GYRO_FIFO_CTRL5, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_FIFO_MODE_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(
            self.LSM6DSL_ACC_GYRO_FIFO_CTRL5, 1, r)

    def LSM6DSL_ACC_GYRO_W_ODR_XL(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(self.LSM6DSL_ACC_GYRO_CTRL1_XL, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_ODR_XL_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(self.LSM6DSL_ACC_GYRO_CTRL1_XL, 1, r)

    def LSM6DSL_ACC_GYRO_W_FS_XL(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(self.LSM6DSL_ACC_GYRO_CTRL1_XL, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_FS_XL_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(self.LSM6DSL_ACC_GYRO_CTRL1_XL, 1, r)

    def Set_X_FS(self, fullScale):  # 2.0
        new_fs = 0.0
        if fullScale <= 2.0:
            new_fs = self.LSM6DSL_ACC_GYRO_FS_XL_2g
        elif fullScale <= 4.0:
            new_fs = self.LSM6DSL_ACC_GYRO_FS_XL_4g
        elif fullScale <= 8.0:
            new_fs = self.LSM6DSL_ACC_GYRO_FS_XL_8g
        else:
            new_fs = self.LSM6DSL_ACC_GYRO_FS_XL_16g
        self.LSM6DSL_ACC_GYRO_W_FS_XL(new_fs)

    def LSM6DSL_ACC_GYRO_W_ODR_G(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(self.LSM6DSL_ACC_GYRO_CTRL2_G, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_ODR_G_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(self.LSM6DSL_ACC_GYRO_CTRL2_G, 1, r)

    def LSM6DSL_ACC_GYRO_W_FS_125(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(self.LSM6DSL_ACC_GYRO_CTRL2_G, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_FS_125_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(self.LSM6DSL_ACC_GYRO_CTRL2_G, 1, r)

    def LSM6DSL_ACC_GYRO_W_FS_G(self, param):
        r = self.LSM6DSL_ACC_GYRO_ReadRegRaw(self.LSM6DSL_ACC_GYRO_CTRL2_G, 1)
        r[0] &= ~self.LSM6DSL_ACC_GYRO_FS_G_MASK
        r[0] |= param
        self.LSM6DSL_ACC_GYRO_WriteRegRaw(self.LSM6DSL_ACC_GYRO_CTRL2_G, 1, r)

    def Set_G_FS(self, fullScale):  # 2000.0
        if fullScale <= 125.0:
            self.LSM6DSL_ACC_GYRO_W_FS_125(
                self.LSM6DSL_ACC_GYRO_FS_125_ENABLED)
        else:
            new_fs = 0.0
            if fullScale <= 245.0:
                new_fs = self.LSM6DSL_ACC_GYRO_FS_G_245dps
            elif fullScale <= 500.0:
                new_fs = self.LSM6DSL_ACC_GYRO_FS_G_500dps
            elif fullScale <= 1000.0:
                new_fs = self.LSM6DSL_ACC_GYRO_FS_G_1000dps
            else:
                new_fs = self.LSM6DSL_ACC_GYRO_FS_G_2000dps
            self.LSM6DSL_ACC_GYRO_W_FS_125(
                self.LSM6DSL_ACC_GYRO_FS_125_DISABLED)
            self.LSM6DSL_ACC_GYRO_W_FS_G(new_fs)

    def start(self):
        self.LSM6DSL_ACC_GYRO_W_IF_Addr_Incr(
            self.LSM6DSL_ACC_GYRO_IF_INC_ENABLED)
        self.LSM6DSL_ACC_GYRO_W_BDU(self.LSM6DSL_ACC_GYRO_BDU_BLOCK_UPDATE)
        self.LSM6DSL_ACC_GYRO_W_FIFO_MODE(
            self.LSM6DSL_ACC_GYRO_FIFO_MODE_BYPASS)
        self.LSM6DSL_ACC_GYRO_W_ODR_XL(self.LSM6DSL_ACC_GYRO_ODR_XL_POWER_DOWN)
        self.Set_X_FS(2.0)
        self.LSM6DSL_ACC_GYRO_W_ODR_G(self.LSM6DSL_ACC_GYRO_ODR_G_POWER_DOWN)
        self.Set_G_FS(2000.0)

    def Set_X_ODR_When_Enabled(self, odr):
        new_odr = 0.0
        if odr <= 13.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_13Hz
        elif odr <= 26.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_26Hz
        elif odr <= 52.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_52Hz
        elif odr <= 104.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_104Hz
        elif odr <= 208.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_208Hz
        elif odr <= 416.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_416Hz
        elif odr <= 833.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_833Hz
        elif odr <= 1660.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_1660Hz
        elif odr <= 3330.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_3330Hz
        else:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_XL_6660Hz

        self.LSM6DSL_ACC_GYRO_W_ODR_XL(new_odr)

    def Set_G_ODR_When_Enabled(self, odr):
        new_odr = 0.0
        if odr <= 13.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_13Hz
        elif odr <= 26.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_26Hz
        elif odr <= 52.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_52Hz
        elif odr <= 104.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_104Hz
        elif odr <= 208.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_208Hz
        elif odr <= 416.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_416Hz
        elif odr <= 833.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_833Hz
        elif odr <= 1660.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_1660Hz
        elif odr <= 3330.0:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_3330Hz
        else:
            new_odr = self.LSM6DSL_ACC_GYRO_ODR_G_6660Hz
        self.LSM6DSL_ACC_GYRO_W_ODR_G(new_odr)

    def Enable_X(self):
        self.Set_X_ODR_When_Enabled(104.0)

    def Enable_G(self):
        self.Set_G_ODR_When_Enabled(104.0)

    def enableAll(self):
        self.Enable_X()
        self.Enable_G()

    def __init__(self, i2c_bus):
        self._bus = i2c_bus
        self.start()
        self.enableAll()

    def LSM6DSL_ACC_GYRO_WriteRegRaw(self, RegAddr, NumByteToRead, data):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        for i in data:
            self._bus.write_byte_data(
                (((self.LSM6DSL_ACC_GYRO_I2C_ADDRESS_HIGH) >> 1) & 0x7F), RegAddr, i)
            # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LSM6DSL_ACC_GYRO_I2C_ADDRESS_HIGH) >> 1) & 0x7F)))

    def LSM6DSL_ACC_GYRO_ReadRegRaw(self, RegAddr, NumByteToRead):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        self._bus.write_byte(
            (((self.LSM6DSL_ACC_GYRO_I2C_ADDRESS_HIGH) >> 1) & 0x7F), RegAddr)
        # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LSM6DSL_ACC_GYRO_I2C_ADDRESS_HIGH) >> 1) & 0x7F)))

        return raw

    def LSM6DSL_ACC_GYRO_GetRawAccData(self):
        numberOfByteForDimension = 2
        buffer = []
        for i in range(3):
            for j in range(numberOfByteForDimension):
                buffer.append(self.LSM6DSL_ACC_GYRO_ReadRegRaw(
                    self.LSM6DSL_ACC_GYRO_OUTX_L_XL + len(buffer), 1)[0])
        return buffer

    def getGAxesRaw(self):
        numberOfByteForDimension = 2
        buffer = []
        for i in range(3):
            for j in range(numberOfByteForDimension):
                buffer.append(self.LSM6DSL_ACC_GYRO_ReadRegRaw(
                    self.LSM6DSL_ACC_GYRO_OUTX_L_G + len(buffer), 1)[0])
        return buffer

    def getGSensivity(self):
        fullscale125 = self.LSM6DSL_ACC_GYRO_ReadRegRaw(
            self.LSM6DSL_ACC_GYRO_CTRL2_G, 1)[0]
        fullscale125 &= self.LSM6DSL_ACC_GYRO_FS_125_MASK
        if fullscale125 == self.LSM6DSL_ACC_GYRO_FS_125_ENABLED:
            return float(self.LSM6DSL_GYRO_SENSITIVITY_FOR_FS_125DPS)
        else:
            fullscale = self.LSM6DSL_ACC_GYRO_ReadRegRaw(
                self.LSM6DSL_ACC_GYRO_CTRL2_G, 1)[0]
            fullscale &= self.LSM6DSL_ACC_GYRO_FS_G_MASK

            if fullscale == self.LSM6DSL_ACC_GYRO_FS_G_245dps:
                return float(self.LSM6DSL_GYRO_SENSITIVITY_FOR_FS_245DPS)
            elif fullscale == self.LSM6DSL_ACC_GYRO_FS_G_500dps:
                return float(self.LSM6DSL_GYRO_SENSITIVITY_FOR_FS_500DPS)
            elif fullscale == self.LSM6DSL_ACC_GYRO_FS_G_1000dps:
                return float(self.LSM6DSL_GYRO_SENSITIVITY_FOR_FS_1000DPS)
            elif fullscale == self.LSM6DSL_ACC_GYRO_FS_G_2000dps:
                return float(self.LSM6DSL_GYRO_SENSITIVITY_FOR_FS_2000DPS)
            else:
                return -1.0

    def getGAxes(self):
        regValue = self.getGAxesRaw()

        pData = []
        pData.append(twoComplements(regValue[1], regValue[0]))
        pData.append(twoComplements(regValue[3], regValue[2]))
        pData.append(twoComplements(regValue[5], regValue[4]))

        sensitivity = self.getGSensivity()
        pData[0] = (pData[0] * sensitivity)
        pData[1] = (pData[1] * sensitivity)
        pData[2] = (pData[2] * sensitivity)

        return pData

    def getGyroscopeSensivity(self):
        fullScale = self.LSM6DSL_ACC_GYRO_ReadRegRaw(
            self.LSM6DSL_ACC_GYRO_CTRL1_XL, 1)[0]

        fullScale &= self.LSM6DSL_ACC_GYRO_FS_XL_MASK

        if fullScale == self.LSM6DSL_ACC_GYRO_FS_XL_2g:
            return float(self.LSM6DSL_ACC_SENSITIVITY_FOR_FS_2G)
        elif fullScale == self.LSM6DSL_ACC_GYRO_FS_XL_4g:
            return float(self.LSM6DSL_ACC_SENSITIVITY_FOR_FS_4G)
        elif fullScale == self.LSM6DSL_ACC_GYRO_FS_XL_8g:
            return float(self.LSM6DSL_ACC_SENSITIVITY_FOR_FS_8G)
        elif fullScale == self.LSM6DSL_ACC_GYRO_FS_XL_16g:
            return float(self.LSM6DSL_ACC_SENSITIVITY_FOR_FS_16G)
        else:
            return -1.0

    def getGyroscopeXAxis(self):
        regValue = self.LSM6DSL_ACC_GYRO_GetRawAccData()
        sensivity = self.getGyroscopeSensivity()

        gyroXAxis = []
        gyroXAxis.append(twoComplements(regValue[1], regValue[0]))
        gyroXAxis.append(twoComplements(regValue[3], regValue[2]))
        gyroXAxis.append(twoComplements(regValue[5], regValue[4]))

        gyroXAxis[0] = gyroXAxis[0] * sensivity
        gyroXAxis[1] = gyroXAxis[1] * sensivity
        gyroXAxis[2] = gyroXAxis[2] * sensivity

        return gyroXAxis
