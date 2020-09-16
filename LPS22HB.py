import smbus
import time


class LPS22HB:
    # pressure and temperature sensor
    LPS22HB_ADDRESS_HIGH = 0xBA
    LPS22HB_PRESS_OUT_XL_REG = 0x28
    LPS22HB_TEMP_OUT_L_REG = 0x2B

    LPS22HB_LowPower = 0x01
    LPS22HB_ODR_ONE_SHOT = 0x00
    LPS22HB_DISABLE = 0
    LPS22HB_ODR_9 = 0x00
    LPS22HB_BDU_NO_UPDATE = 0x02

    LPS22HB_LCEN_MASK = 0x01
    LPS22HB_RES_CONF_REG = 0x1A
    LPS22HB_CTRL_REG1 = 0x10
    LPS22HB_ODR_MASK = 0x70
    LPS22HB_LPFP_MASK = 0x08
    LPS22HB_LPFP_BIT = 3
    LPS22HB_LPFP_CUTOFF_MASK = 0x04
    LPS22HB_BDU_MASK = 0x02
    LPS22HB_CTRL_REG2 = 0x11
    LPS22HB_ADD_INC_MASK = 0x10
    LPS22HB_ENABLE = not LPS22HB_DISABLE
    LPS22HB_ADD_INC_BIT = 4
    LPS22HB_ODR_ONE_SHOT = 0x00
    LPS22HB_ODR_1HZ = 0x10
    LPS22HB_ODR_10HZ = 0x20
    LPS22HB_ODR_25HZ = 0x30
    LPS22HB_ODR_50HZ = 0x40
    LPS22HB_ODR_75HZ = 0x50

    def LPS22HB_Set_PowerMode(self):
        r = self.LPS22HB_ReadRegRaw(self.LPS22HB_RES_CONF_REG, 1)
        r[0] &= ~self.LPS22HB_LCEN_MASK
        r[0] |= self.LPS22HB_LowPower
        self.LPS22HB_WriteRegRaw(self.LPS22HB_RES_CONF_REG, 1, r)

    def LPS22HB_Set_Odr(self):
        r = self.LPS22HB_ReadRegRaw(self.LPS22HB_CTRL_REG1, 1)
        r[0] &= ~self.LPS22HB_ODR_MASK
        r[0] |= self.LPS22HB_ODR_ONE_SHOT
        self.LPS22HB_WriteRegRaw(self.LPS22HB_CTRL_REG1, 1, r)

    def LPS22HB_Set_LowPassFilter(self):
        r = self.LPS22HB_ReadRegRaw(self.LPS22HB_CTRL_REG1, 1)
        r[0] &= ~self.LPS22HB_LPFP_MASK
        r[0] |= self.LPS22HB_DISABLE << self.LPS22HB_LPFP_BIT
        self.LPS22HB_WriteRegRaw(self.LPS22HB_CTRL_REG1, 1, r)

    def LPS22HB_Set_LowPassFilterCutoff(self):
        r = self.LPS22HB_ReadRegRaw(self.LPS22HB_CTRL_REG1, 1)
        r[0] &= ~self.LPS22HB_LPFP_CUTOFF_MASK
        r[0] |= self.LPS22HB_ODR_9
        self.LPS22HB_WriteRegRaw(self.LPS22HB_CTRL_REG1, 1, r)

    def LPS22HB_Set_Bdu(self):
        r = self.LPS22HB_ReadRegRaw(self.LPS22HB_CTRL_REG1, 1)
        r[0] &= ~self.LPS22HB_BDU_MASK
        r[0] |= self.LPS22HB_BDU_NO_UPDATE
        self.LPS22HB_WriteRegRaw(self.LPS22HB_CTRL_REG1, 1, r)

    def LPS22HB_Set_AutomaticIncrementRegAddress(self):
        r = self.LPS22HB_ReadRegRaw(self.LPS22HB_CTRL_REG2, 1)
        r[0] &= ~self.LPS22HB_ADD_INC_MASK
        r[0] |= self.LPS22HB_ENABLE << self.LPS22HB_ADD_INC_BIT
        self.LPS22HB_WriteRegRaw(self.LPS22HB_CTRL_REG2, 1, r)

    def LPS22HB_Set_Odr(self, odr):
        r = self.LPS22HB_ReadRegRaw(self.LPS22HB_CTRL_REG1, 1)
        r[0] &= ~self.LPS22HB_ODR_MASK
        r[0] |= odr
        self.LPS22HB_WriteRegRaw(self.LPS22HB_CTRL_REG1, 1, r)

    # def GetODR(self, odr):

    def SetODR_When_Enabled(self, Last_odr):
        new_odr = 0.0
        if Last_odr <= 1.0:
            new_odr = self.LPS22HB_ODR_1HZ
        elif Last_odr <= 10.0:
            new_odr = self.LPS22HB_ODR_10HZ
        elif Last_odr <= 25.0:
            new_odr = self.LPS22HB_ODR_25HZ
        elif Last_odr <= 50.0:
            new_odr = self.LPS22HB_ODR_50HZ
        else:
            new_odr = self.LPS22HB_ODR_75HZ
        self.LPS22HB_Set_Odr(new_odr)
        # self.GetODR(Last_odr)

    def enable(self):
        self.LPS22HB_Set_PowerMode()
        self.LPS22HB_Set_Odr(0)
        self.LPS22HB_Set_LowPassFilter()
        self.LPS22HB_Set_LowPassFilterCutoff()
        self.LPS22HB_Set_Bdu()
        self.LPS22HB_Set_AutomaticIncrementRegAddress()
        self.SetODR_When_Enabled(25.0)

    def __init__(self, i2c_bus):
        self._bus = i2c_bus
        self.enable()

    def LPS22HB_WriteRegRaw(self, RegAddr, NumByteToRead, data):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        for i in data:
            self._bus.write_byte_data(
                (((self.LPS22HB_ADDRESS_HIGH) >> 1) & 0x7F), RegAddr, i)
            # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LPS22HB_ADDRESS_HIGH) >> 1) & 0x7F)))

    def LPS22HB_ReadRegRaw(self, RegAddr, NumByteToRead):
        if (NumByteToRead > 1):
            RegAddr |= 0x80

        self._bus.write_byte(
            (((self.LPS22HB_ADDRESS_HIGH) >> 1) & 0x7F), RegAddr)
        # time.sleep(0.02)

        raw = []
        for i in range(NumByteToRead):
            raw.append(self._bus.read_byte(
                (((self.LPS22HB_ADDRESS_HIGH) >> 1) & 0x7F)))

        return raw

    def getTemperature(self):
        buffer0 = self.LPS22HB_ReadRegRaw(self.LPS22HB_TEMP_OUT_L_REG, 2)
        tmp = ((buffer0[1]) << 8) + buffer0[0]

        return tmp/100.0

    def getPressure(self):
        buffer0 = self.LPS22HB_ReadRegRaw(self.LPS22HB_PRESS_OUT_XL_REG, 3)
        tmp = 0
        for i in range(3):
            tmp |= ((buffer0[i]) << (8*i))

        if(tmp & 0x00800000):
            tmp |= 0xFF000000

        return tmp/4096.0
