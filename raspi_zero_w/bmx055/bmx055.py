# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BMX055
# This code is designed to work with the BMX055_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

accl_address = 0x19
gyro_address = 0x69
mag_address  = 0x13

def accl_setup():
    try:
        # BMX055 Accl address, 0x18(24)
        # Select PMU_Range register, 0x0F(15)
        #		0x03(03)	Range = +/- 2g
        bus.write_byte_data(accl_address, 0x0F, 0x03)
        # BMX055 Accl address, 0x18(24)
        # Select PMU_BW register, 0x10(16)
        #		0x08(08)	Bandwidth = 7.81 Hz
        bus.write_byte_data(accl_address, 0x10, 0x08)
        # BMX055 Accl address, 0x18(24)
        # Select PMU_LPW register, 0x11(17)
        #		0x00(00)	Normal mode, Sleep duration = 0.5ms
        bus.write_byte_data(accl_address, 0x11, 0x00)

    except IOError as e:
        print("accl setup error")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    time.sleep(0.5)

def gyro_setup():
    try:
        # BMX055 Gyro address, 0x68(104)
        # Select Range register, 0x0F(15)
        #		0x04(04)	Full scale = +/- 125 degree/s
        bus.write_byte_data(gyro_address, 0x0F, 0x04)
        # BMX055 Gyro address, 0x68(104)
        # Select Bandwidth register, 0x10(16)
        #		0x07(07)	ODR = 100 Hz
        bus.write_byte_data(gyro_address, 0x10, 0x07)
        # BMX055 Gyro address, 0x68(104)
        # Select LPM1 register, 0x11(17)
        #		0x00(00)	Normal mode, Sleep duration = 2ms
        bus.write_byte_data(gyro_address, 0x11, 0x00)
    except IOError as e:
        print("gyro setup error")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    time.sleep(0.5)

def mag_setup():
    try:
        # BMX055 Mag address, 0x10(16)
        # Select Mag register, 0x4B(75)
        #		0x83(121)	Soft reset
        bus.write_byte_data(mag_address, 0x4B, 0x83)
        # BMX055 Mag address, 0x10(16)
        # Select Mag register, 0x4C(76)
        #		0x00(00)	Normal Mode, ODR = 10 Hz
        bus.write_byte_data(mag_address, 0x4C, 0x00)
        # BMX055 Mag address, 0x10(16)
        # Select Mag register, 0x4E(78)
        #		0x84(122)	X, Y, Z-Axis enabled
        bus.write_byte_data(mag_address, 0x4E, 0x84)
        # BMX055 Mag address, 0x10(16)
        # Select Mag register, 0x51(81)
        #		0x04(04)	No. of Repetitions for X-Y Axis = 9
        bus.write_byte_data(mag_address, 0x51, 0x04)
        # BMX055 Mag address, 0x10(16)
        # Select Mag register, 0x52(82)
        #		0x0F(15)	No. of Repetitions for Z-Axis = 15
        bus.write_byte_data(mag_address, 0x52, 0x0F)
    except IOError as e:
        print("mag setup error")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    time.sleep(0.5)

def bmx_setup():
    accl_setup()
    gyro_setup()
    mag_setup()

def get_accl_value():
    try:
        # BMX055 Accl address, 0x18(24)
        # Read data back from 0x02(02), 6 bytes
        # xAccl LSB, xAccl MSB, yAccl LSB, yAccl MSB, zAccl LSB, zAccl MSB
        data = bus.read_i2c_block_data(accl_address, 0x02, 6)

        # Convert the data to 12-bits
        xAccl = ((data[1] * 256) + (data[0] & 0xF0)) / 16
        if xAccl > 2047 :
            xAccl -= 4096
        yAccl = ((data[3] * 256) + (data[2] & 0xF0)) / 16
        if yAccl > 2047 :
            yAccl -= 4096
        zAccl = ((data[5] * 256) + (data[4] & 0xF0)) / 16
        if zAccl > 2047 :
            zAccl -= 4096

        return xAccl, yAccl, zAccl
    
    except IOError as e:
        print("accl get error")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return 100, 100, 100

def get_gyro_value():
    try:
        # BMX055 Gyro address, 0x68(104)
        # Read data back from 0x02(02), 6 bytes
        # xGyro LSB, xGyro MSB, yGyro LSB, yGyro MSB, zGyro LSB, zGyro MSB
        data = bus.read_i2c_block_data(gyro_address, 0x02, 6)

        # Convert the data
        xGyro = data[1] * 256 + data[0]
        if xGyro > 32767 :
            xGyro -= 65536
        yGyro = data[3] * 256 + data[2]
        if yGyro > 32767 :
            yGyro -= 65536
        zGyro = data[5] * 256 + data[4]
        if zGyro > 32767 :
            zGyro -= 65536

        return xGyro, yGyro, zGyro

    except IOError as e:
        print("gyro get error")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return 100, 100, 100

def get_mag_value():
    try:
        # BMX055 Mag address, 0x10(16)
        # Read data back from 0x42(66), 6 bytes
        # X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB
        data = bus.read_i2c_block_data(mag_address, 0x42, 6)    

        # Convert the data
        xMag = ((data[1] * 256) + (data[0] & 0xF8)) / 8
        if xMag > 4095 :
            xMag -= 8192
        yMag = ((data[3] * 256) + (data[2] & 0xF8)) / 8
        if yMag > 4095 :
            yMag -= 8192
        zMag = ((data[5] * 256) + (data[4] & 0xFE)) / 2
        if zMag > 16383 :
            zMag -= 32768

        return xMag, yMag, zMag

    except IOError as e:
        print("mag get error")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return 100, 100, 100

if __name__ == "__main__":
    bmx_setup()
    while(True):
        xAccl, yAccl, zAccl = get_accl_value() 
        xGyro, yGyro, zGyro = get_gyro_value()
        xMag, yMag, zMag = get_mag_value()

        print("Acceleration in X-Axis: ", xAccl)
        print("Acceleration in Y-Axis: ", yAccl)
        print("Acceleration in Z-Axis: ", zAccl)
        print("X-Axis of Rotation: ", xGyro)
        print("Y-Axis of Rotation: ", yGyro)
        print("Z-Axis of Rotation: ", zGyro)
        print("Magnetic field in X-Axis: ", xMag)
        print("Magnetic field in Y-Axis: ", yMag)
        print("Magnetic field in Z-Axis: ", zMag)
        time.sleep(0.5)
