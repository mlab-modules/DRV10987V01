# Python control class for DRV10987 BLDC driver

This class provides a convenient interface to control a BLDC motor using the DRV10987V01 module, which contains the Texas Instruments DRV10987 motor driver IC. It allows configuration of various parameters and registers to control the motor speed, current, and other functionalities.

The DRV10987V01 module is designed for use with 3-phase sensorless BLDC motors, and this class
simplifies the communication and configuration process, making it easier to drive the motor.

Before using this class, make sure you have properly initialized the communication interface to
communicate with the DRV10987 module using the SMBus interface. For example, you can use the
USBI2C01 module (https://www.mlab.cz/module/USBI2C01) to connect your computer to the driver.

Note:
- Connect the DRV10987V01 module to your motor and power supply according to the module's specifications.
- The methods of this class assume that you have already set up the communication interface (SMBus) correctly.

Example usage:
drv = MLAB_DRV10987()
drv.configure_CONFIG1(RMValue=0b0111011, odpor_vinuti=1)
drv.set_SpeedCtrl(speed=50)  # Set motor speed to 50% (default override=True)
drv.enable_motor()  # Enable motor output
drv.print_status_registers()  # Print the current status registers
drv.disable_motor()  # Disable motor output
"""
