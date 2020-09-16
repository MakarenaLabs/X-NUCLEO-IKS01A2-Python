import smbus
import time
from .utils import *


class LSM303AGR:
    # accelerometer and magnetometer sensor
    LSM303AGR_ACC_LPEN_DISABLED = 0x00
    LSM303AGR_ACC_LPEN_ENABLED = 0x08
    LSM303AGR_ACC_HR_DISABLED = 0x00
    LSM303AGR_ACC_HR_ENABLED = 0x08
    LSM303AGR_ACC_FS_2G = 0x00
    LSM303AGR_ACC_FS_4G = 0x10
    LSM303AGR_ACC_FS_8G = 0x20
    LSM303AGR_ACC_FS_16G = 0x30
    LSM303AGR_ACC_CTRL_REG4 = 0X23
    LSM303AGR_ACC_HR_MASK = 0x08
    LSM303AGR_ACC_CTRL_REG1 = 0X20
    LSM303AGR_ACC_LPEN_MASK = 0x08
    LSM303AGR_ACC_FS_MASK = 0x30
    LSM303AGR_ACC_FS_2G = 0x00
    LSM303AGR_ACC_FS_4G = 0x10
    LSM303AGR_ACC_FS_8G = 0x20
    LSM303AGR_ACC_FS_16G = 0x30
    LSM303AGR_ACC_OUT_X_L = 0X28
    LSM303AGR_ACC_I2C_ADDRESS = 0x32
    LSM303AGR_MAG_I2C_ADDRESS = 0x3C
    LSM303AGR_MAG_OUTX_L_REG = 0X68

    LSM303AGR_ACC_BDU_DISABLED = 0x00
    LSM303AGR_ACC_BDU_ENABLED = 0x80

    LSM303AGR_ACC_FM_BYPASS = 0x00
    LSM303AGR_ACC_FM_FIFO = 0x40
    LSM303AGR_ACC_FM_STREAM = 0x80
    LSM303AGR_ACC_FM_TRIGGER = 0xC0

    LSM303AGR_ACC_ODR_DO_PWR_DOWN = 0x00
    LSM303AGR_ACC_ODR_DO_1Hz = 0x10
    LSM303AGR_ACC_ODR_DO_10Hz = 0x20
    LSM303AGR_ACC_ODR_DO_25Hz = 0x30
    LSM303AGR_ACC_ODR_DO_50Hz = 0x40
    LSM303AGR_ACC_ODR_DO_100Hz = 0x50
    LSM303AGR_ACC_ODR_DO_200Hz = 0x60
    LSM303AGR_ACC_ODR_DO_400Hz = 0x70
    LSM303AGR_ACC_ODR_DO_1_6KHz = 0x80
    LSM303AGR_ACC_ODR_DO_1_25KHz = 0x90

    LSM303AGR_ACC_XEN_DISABLED = 0x00
    LSM303AGR_ACC_XEN_ENABLED = 0x01
    LSM303AGR_ACC_XEN_MASK = 0x01
    LSM303AGR_ACC_YEN_DISABLED = 0x00
    LSM303AGR_ACC_YEN_ENABLED = 0x02
    LSM303AGR_ACC_YEN_MASK = 0x02
    LSM303AGR_ACC_ZEN_DISABLED = 0x00
    LSM303AGR_ACC_ZEN_ENABLED = 0x04
    LSM303AGR_ACC_ZEN_MASK = 0x04

    LSM303AGR_ACC_BDU_MASK = 0x80
    LSM303AGR_ACC_FIFO_CTRL_REG = 0X2E
    LSM303AGR_ACC_FM_MASK = 0xC0
    LSM303AGR_ACC_ODR_MASK = 0xF0

    LSM303AGR_MAG_MD_IDLE1_MODE = 0x02
    LSM303AGR_MAG_BDU_ENABLED = 0x10
    LSM303AGR_MAG_ST_DISABLED = 0x00
    LSM303AGR_MAG_ST_ENABLED = 0x02

    LSM303AGR_MAG_CFG_REG_A = 0X60
    LSM303AGR_MAG_CFG_REG_B = 0X61
    LSM303AGR_MAG_CFG_REG_C = 0X62
    LSM303AGR_MAG_MD_MASK = 0x03
    LSM303AGR_MAG_BDU_MASK = 0x10
    LSM303AGR_MAG_ODR_MASK = 0x0C

    LSM303AGR_MAG_ODR_10Hz = 0x00
    LSM303AGR_MAG_ODR_20Hz = 0x04
    LSM303AGR_MAG_ODR_50Hz = 0x08
    LSM303AGR_MAG_ODR_100Hz = 0x0C

    LSM303AGR_MAG_ST_MASK = 0x02
    LSM303AGR_MAG_MD_CONTINUOS_MODE = 0x00

    LSM303AGR_ACC_Sensitivity_List = [[
        980,
        1950,
        3900,
        11720
    ],
        [
        3900,
        7820,
        15630,
        46900
    ],
        [
        15630,
        31260,
        62520,
        187580
    ]]

    def LSM303AGR_ACC_W_BlockDataUpdate(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_CTRL_REG4, 1)
        r[0] &= ~self.LSM303AGR_ACC_BDU_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_CTRL_REG4, 1, r)

    def LSM303AGR_ACC_W_FifoMode(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_FIFO_CTRL_REG, 1)
        r[0] &= ~self.LSM303AGR_ACC_FM_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_FIFO_CTRL_REG, 1, r)

    def LSM303AGR_ACC_W_ODR(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1)
        r[0] &= ~self.LSM303AGR_ACC_ODR_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1, r)

    def LSM303AGR_ACC_W_FullScale(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_CTRL_REG4, 1)
        r[0] &= ~self.LSM303AGR_ACC_FS_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_CTRL_REG4, 1, r)

    def SetFS(self, fullScale):
        new_fs = 0.0
        if fullScale <= 2.0:
            new_fs = self. LSM303AGR_ACC_FS_2G
        elif fullScale <= 4.0:
            new_fs = self. LSM303AGR_ACC_FS_4G
        elif fullScale <= 8.0:
            new_fs = self. LSM303AGR_ACC_FS_8G
        else:
            new_fs = self.LSM303AGR_ACC_FS_16G
        self.LSM303AGR_ACC_W_FullScale(new_fs)

    def LSM303AGR_ACC_W_XEN(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1)
        r[0] &= ~self.LSM303AGR_ACC_XEN_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1, r)

    def LSM303AGR_ACC_W_YEN(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1)
        r[0] &= ~self.LSM303AGR_ACC_YEN_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1, r)

    def LSM303AGR_ACC_W_ZEN(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1)
        r[0] &= ~self.LSM303AGR_ACC_ZEN_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1, r)

    def initACC(self):
        self.LSM303AGR_ACC_W_BlockDataUpdate(self.LSM303AGR_ACC_BDU_ENABLED)
        self.LSM303AGR_ACC_W_FifoMode(self.LSM303AGR_ACC_FM_BYPASS)
        self.LSM303AGR_ACC_W_ODR(self.LSM303AGR_ACC_ODR_DO_PWR_DOWN)
        self.SetFS(2.0)
        self.LSM303AGR_ACC_W_XEN(self.LSM303AGR_ACC_XEN_ENABLED)
        self.LSM303AGR_ACC_W_YEN(self.LSM303AGR_ACC_YEN_ENABLED)
        self.LSM303AGR_ACC_W_ZEN(self.LSM303AGR_ACC_ZEN_ENABLED)

    def LSM303AGR_ACC_W_ODR(self, param):
        r = self.LSM303AGR_ACC_ReadRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1)
        r[0] &= ~self.LSM303AGR_ACC_ODR_MASK
        r[0] |= param
        self.LSM303AGR_ACC_WriteRegRaw(self.LSM303AGR_ACC_CTRL_REG1, 1, r)

    def SetODR_When_Enabled(self, odr):
        new_odr = 0.0
        if odr <= 1.0:
            new_odr = self.LSM303AGR_ACC_ODR_DO_1Hz
        elif odr <= 10.0:
            new_odr = self.LSM303AGR_ACC_ODR_DO_10Hz
        elif odr <= 25.0:
            new_odr = self.LSM303AGR_ACC_ODR_DO_25Hz
        elif odr <= 50.0:
            new_odr = self.LSM303AGR_ACC_ODR_DO_50Hz
        elif odr <= 100.0:
            new_odr = self.LSM303AGR_ACC_ODR_DO_100Hz
        elif odr <= 200.0:
            new_odr = self.LSM303AGR_ACC_ODR_DO_200Hz
        else:
            new_odr = self.LSM303AGR_ACC_ODR_DO_400Hz
        self.LSM303AGR_ACC_W_ODR(new_odr)

    def enableACC(self):
        self.SetODR_When_Enabled(100.0)

    def LSM303AGR_MAG_W_MD(self, param):
        r = self.LSM303AGR_MAG_ReadRegRaw(self.LSM303AGR_MAG_CFG_REG_A, 1)
        r[0] &= ~self.LSM303AGR_MAG_MD_MASK
        r[0] |= param
        self.LSM303AGR_MAG_WriteRegRaw(self.LSM303AGR_MAG_CFG_REG_A, 1, r)

    def LSM303AGR_MAG_W_BDU(self, param):
        r = self.LSM303AGR_MAG_ReadRegRaw(self.LSM303AGR_MAG_CFG_REG_C, 1)
        r[0] &= ~self.LSM303AGR_MAG_BDU_MASK
        r[0] |= param
        self.LSM303AGR_MAG_WriteRegRaw(self.LSM303AGR_MAG_CFG_REG_C, 1, r)

    def LSM303AGR_MAG_W_ODR(self, param):
        r = self.LSM303AGR_MAG_ReadRegRaw(self.LSM303AGR_MAG_CFG_REG_A, 1)
        r[0] &= ~self.LSM303AGR_MAG_ODR_MASK
        r[0] |= param
        self.LSM303AGR_MAG_WriteRegRaw(self.LSM303AGR_MAG_CFG_REG_A, 1, r)

    def SetODR(self, odr):
        new_odr = 0.0
        if odr <= 10.000:
            new_odr = self.LSM303AGR_MAG_ODR_10Hz
        elif odr <= 20.000:
            new_odr = self.LSM303AGR_MAG_ODR_20Hz
        elif odr <= 50.000:
            new_odr = self.LSM303AGR_MAG_ODR_50Hz
        else:
            new_odr = self.LSM303AGR_MAG_ODR_100Hz
        self.LSM303AGR_MAG_W_ODR(new_odr)

    def SetFS(self, param):
        self.fullScale = param

    def LSM303AGR_MAG_W_ST(self, param):
        r = self.LSM303AGR_MAG_ReadRegRaw(self.LSM303AGR_MAG_CFG_REG_C, 1)
        r[0] &= ~self.LSM303AGR_MAG_ST_MASK
        r[0] |= param
        self.LSM303AGR_MAG_WriteRegRaw(self.LSM303AGR_MAG_CFG_REG_C, 1, r)

    def initMAG(self):
        self.LSM303AGR_MAG_W_MD(self.LSM303AGR_MAG_MD_IDLE1_MODE)
        self.LSM303AGR_MAG_W_BDU(self.LSM303AGR_MAG_BDU_ENABLED)
        self.SetODR(100.0)
        self.SetFS(50.0)
        self.LSM303AGR_MAG_W_ST(self.LSM303AGR_MAG_ST_DISABLED)

    def LSM303AGR_MAG_W_MD(self, param):
        r = self.LSM303AGR_MAG_ReadRegRaw(self.LSM303AGR_MAG_CFG_REG_A, 1)
        r[0] &= ~self.LSM303AGR_MAG_MD_MASK
        r[0] |= param
        self.LSM303AGR_MAG_WriteRegRaw(self.LSM303AGR_MAG_CFG_REG_A, 1, r)

    def enableMAG(self):
        self.LSM303AGR_MAG_W_MD(self.LSM303AGR_MAG_MD_CONTINUOS_MODE)

    def __init__(self, i2c_bus):
        self._bus = i2c_bus
        self.initACC()
        self.enableACC()
        self.initMAG()
        self.enableMAG()

    def LSM303AGR_ACC_ReadRegRaw(self, RegAddr, NumByteToRead):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        self._bus.write_byte(
            (((self.LSM303AGR_ACC_I2C_ADDRESS) >> 1) & 0x7F), RegAddr)
        # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LSM303AGR_ACC_I2C_ADDRESS) >> 1) & 0x7F)))

        return raw

    def LSM303AGR_ACC_WriteRegRaw(self, RegAddr, NumByteToRead, data):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        for i in data:
            self._bus.write_byte_data(
                (((self.LSM303AGR_ACC_I2C_ADDRESS) >> 1) & 0x7F), RegAddr, i)
            # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LSM303AGR_ACC_I2C_ADDRESS) >> 1) & 0x7F)))

    def LSM303AGR_MAG_ReadRegRaw(self, RegAddr, NumByteToRead):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        self._bus.write_byte(
            (((self.LSM303AGR_MAG_I2C_ADDRESS) >> 1) & 0x7F), RegAddr)
        # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LSM303AGR_MAG_I2C_ADDRESS) >> 1) & 0x7F)))

        return raw

    def LSM303AGR_MAG_WriteRegRaw(self, RegAddr, NumByteToRead, data):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        for i in data:
            self._bus.write_byte_data(
                (((self.LSM303AGR_MAG_I2C_ADDRESS) >> 1) & 0x7F), RegAddr, i)
            # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LSM303AGR_MAG_I2C_ADDRESS) >> 1) & 0x7F)))

    def LSM303AGR_ACC_Get_Raw_Acceleration(self):
        numberOfByteForDimension = 2
        buffer = []
        for i in range(3):
            for j in range(numberOfByteForDimension):
                buffer.append(self.LSM303AGR_ACC_ReadRegRaw(
                    self.LSM303AGR_ACC_OUT_X_L + len(buffer), 1)[0])
        return buffer

    def LSM303AGR_MAG_Get_Raw_Magnetic(self):
        numberOfByteForDimension = 2
        buffer = []
        for i in range(3):
            for j in range(numberOfByteForDimension):
                buffer.append(self.LSM303AGR_MAG_ReadRegRaw(
                    self.LSM303AGR_MAG_OUTX_L_REG + len(buffer), 1)[0])
        return buffer

    def LSM303AGR_ACC_R_HiRes(self):
        value = self.LSM303AGR_ACC_ReadRegRaw(
            self.LSM303AGR_ACC_CTRL_REG4, 1)[0]
        value &= self.LSM303AGR_ACC_HR_MASK
        return value

    def LSM303AGR_ACC_R_LOWPWR_EN(self):
        value = self.LSM303AGR_ACC_ReadRegRaw(
            self.LSM303AGR_ACC_CTRL_REG1, 1)[0]
        value &= self.LSM303AGR_ACC_LPEN_MASK
        return value

    def LSM303AGR_ACC_R_FullScale(self):
        value = self.LSM303AGR_ACC_ReadRegRaw(
            self.LSM303AGR_ACC_CTRL_REG4, 1)[0]
        value &= self.LSM303AGR_ACC_FS_MASK
        return value

    def LSM303AGR_ACC_Get_Acceleration(self):
        hr = self.LSM303AGR_ACC_R_HiRes()
        lp = self.LSM303AGR_ACC_R_LOWPWR_EN()

        op_mode = 0
        shift = 0

        if lp == self.LSM303AGR_ACC_LPEN_ENABLED and hr == self.LSM303AGR_ACC_HR_DISABLED:
            op_mode = 2
            shift = 8
        elif lp == self.LSM303AGR_ACC_LPEN_DISABLED and hr == self.LSM303AGR_ACC_HR_DISABLED:
            op_mode = 1
            shift = 6
        elif lp == self.LSM303AGR_ACC_LPEN_DISABLED and hr == self.LSM303AGR_ACC_HR_ENABLED:
            op_mode = 0
            shift = 4
        else:
            return None

        fs = self.LSM303AGR_ACC_R_FullScale()

        fs_mode = 0

        if fs == self.LSM303AGR_ACC_FS_2G:
            fs_mode = 0
        elif fs == self.LSM303AGR_ACC_FS_4G:
            fs_mode = 1
        elif fs == self.LSM303AGR_ACC_FS_8G:
            fs_mode = 2
        elif fs == self.LSM303AGR_ACC_FS_16G:
            fs_mode = 3
        else:
            return None

        raw_data_tmp = self.LSM303AGR_ACC_Get_Raw_Acceleration()

        a = twoComplements(raw_data_tmp[1], raw_data_tmp[0])
        b = twoComplements(raw_data_tmp[3], raw_data_tmp[2])
        c = twoComplements(raw_data_tmp[5], raw_data_tmp[4])

        buff = [0, 0, 0]

        buff[0] = (((a) >> shift) *
                   self.LSM303AGR_ACC_Sensitivity_List[op_mode][fs_mode] + 500) / 1000
        buff[1] = (((b) >> shift) *
                   self.LSM303AGR_ACC_Sensitivity_List[op_mode][fs_mode] + 500) / 1000
        buff[2] = (((c) >> shift) *
                   self.LSM303AGR_ACC_Sensitivity_List[op_mode][fs_mode] + 500) / 1000

        return buff

    def LSM303AGR_MAG_Get_Magnetic(self):
        sensivity = 1.5
        regValue = self.LSM303AGR_MAG_Get_Raw_Magnetic()

        pData = [0, 0, 0]

        pData[0] = twoComplements(regValue[1], regValue[0]) * sensivity
        pData[1] = twoComplements(regValue[3], regValue[2]) * sensivity
        pData[2] = twoComplements(regValue[5], regValue[4]) * sensivity

        return pData

    def getAcceleration(self):
        return self.LSM303AGR_ACC_Get_Acceleration()

    def getMagnetometer(self):
        return self.LSM303AGR_MAG_Get_Magnetic()
