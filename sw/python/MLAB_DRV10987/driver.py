#! /usr/bin/python3

import smbus2 as smbus
import time

class MLAB_DRV10987():
    """
    Class for controlling BLDC motor using the DRV10987V01 MLAB module.
    https://www.mlab.cz/module/DRV10987V01

    This class provides a convenient interface to control a BLDC motor using the DRV10987V01 module,
    which contains the Texas Instruments DRV10987 motor driver IC. It allows configuration of various
    parameters and registers to control the motor speed, current, and other functionalities.

    The DRV10987V01 module is designed for use with 3-phase sensorless BLDC motors, and this class
    simplifies the communication and configuration process, making it easier to drive the motor.

    Before using this class, make sure you have properly initialized the communication interface to
    communicate with the DRV10987 module using the SMBus interface. For example, you can use the
    USBI2C01 module (https://www.mlab.cz/module/USBI2C01) to connect your computer to the driver.

    Note:
    - Connect the DRV10987V01 module to your motor and power supply according to the module's specifications.
    - The methods of this class assume that you have already set up the communication interface (SMBus) correctly.
    """

    DRVADDR = 0b1010010
    FaultReg = 0x00
    MotorSpeed = 0x01
    MotorPeriod = 0x02
    MotorXt = 0x03
    MotorCurrent = 0x04
    IPDPosition = 0x05
    SupplyVoltage = 0x05
    SpeedCmd = 0x06
    SpdCmdBuffer = 0x06
    AnalogInLvl = 0x07
    DeviceId = 0x08
    SpeedCtrl = 0x30
    EepromProgramming1 = 0x31
    EepromProgramming2 = 0x32
    EepromProgramming3 = 0x33
    EepromProgramming4 = 0x34
    EepromProgramming5 = 0x35
    EepromProgramming6 = 0x36
    EECTRL = 0x60
    CONFIG1 = 0x90
    CONFIG2 = 0x91
    CONFIG3 = 0x92
    CONFIG4 = 0x93
    CONFIG5 = 0x94
    CONFIG6 = 0x95
    CONFIG7 = 0x96

    EepromProgramming5_ShadowMode = 1 << 12  # Bit 12 for enabling shadow mode in EepromProgramming5

    def __init__(self, bus: smbus.SMBus = smbus.SMBus(1), addr: int = 0b1010010, initialize: bool = True, enable_motor: bool = True, shadow: bool = True) -> None:
        """
        Initialize the DRV10xx motor driver class.

        Args:
            bus (smbus.SMBus, optional): The I2C bus object for communication. Default is /dev/i2c-1.
            addr (int, optional): The address of the device. Default is 0b1010010.
        """
        self.bus = bus
        self.addr = addr

        if not shadow:
            raise "Non shadow mode is not supported yet" # type: ignore
        else:
            self.set_shadow_mode()
        
        if initialize:
            self.disable_motor()
            time.sleep(1)
            self.configure_CONFIG1()
            self.configure_CONFIG2()
            self.configure_CONFIG3()
            self.configure_CONFIG4()
            self.configure_CONFIG5()
            self.configure_CONFIG6()
            self.configure_CONFIG7()

        if enable_motor:
            self.enable_motor()

    def _crop(self, val, min, max):
        """
        Crop the value to be within the given range.

        Args:
            val (float): The value to be cropped.
            min (float): The minimum value of the range.
            max (float): The maximum value of the range.

        Returns:
            float: The cropped value within the range.
        """
        if val < min:
            return min
        elif val > max:
            return max
        else:
            return val

    def _write_config_register(self, reg: int, bit_values: dict) -> None:
        """
        Write the configuration register with the specified bit values.

        Args:
            reg (int): The address of the configuration register.
            bit_values (dict): A dictionary with bit positions as keys and their values.

        Note:
            The `bit_values` dictionary should contain the bit positions as keys (0 to 15) and
            the corresponding bit values (0 or 1) to be written to the register.
        """
        value = 0
        for bit_pos, bit_value in bit_values.items():
            value |= bit_value << bit_pos
        self.write(reg, value)

    def read(self, reg: int) -> int:
        """
        Read a 16-bit value from the specified register address.

        Args:
            reg (int): The address of the register to read from.

        Returns:
            int: The 16-bit value read from the register.
        """
        # Implement the logic to read from the I2C bus
        a = self.bus.read_i2c_block_data(self.addr, reg, 2)
        return (a[1]) | (a[0]) << 8
    
    def write(self, reg: int, value: int) -> None:
        """
        Write a 16-bit value to the specified register address.

        Args:
            reg (int): The address of the register to write to.
            value (int): The 16-bit value to be written to the register.
        """
        # Implement the logic to write to the I2C bus
        self.bus.write_i2c_block_data(self.DRVADDR, reg, [value>>8, value&0xff])

        print(f"WRITE: reg 0x{reg:0x} -> 0b{value:016b}")



    def clear_faults(self) -> None:
        """
        Clear faults by writing 0xFF to the Fault Register.
        """
        self.write(self.FaultReg, 0xFF)


    def set_SpeedCtrl(self, speed: float, override: bool = True) -> bool:
        """
        Set the speed of the motor.

        Args:
            speed (float): Speed of the motor (0-100%).
            override (bool): Override (Binary) - True by default. Override analogue/PWM input.
        Returns:
            bool: True if successful.
        """
        val = (0b1 << 15) if override else 0b0
        val |= int(511.0 * self._crop(speed, 0.0, 100.0)/100.0)
        self.write(self.SpeedCtrl, val)
        return True

    def enable_motor(self):
        """
        Enable the motor by writing 1 to the motor enable bit (15th bit) in the control register (0x60).
        """
        control_reg = self.read(self.EECTRL)
        control_reg &= ~(1 << 15)
        self.write(self.EECTRL, control_reg)

    def disable_motor(self):
        """
        Disable the motor by writing 0 to the motor enable bit (15th bit) in the control register (0x60).
        """
        control_reg = self.read(self.EECTRL)
        control_reg |= 1 << 15
        self.write(self.EECTRL, control_reg)


    def set_shadow_mode(self):
        """
        Set Shadow Register mode by enabling the 12th bit in the EepromProgramming5 register.
        This sets the EEPROM into the shadow mode.
        """

        # Read the current value of the EepromProgramming5 register
        eeprom_reg5 = self.read(self.EepromProgramming5)
        # Set the 12th bit to 1 to enable shadow mode
        eeprom_reg5 |= self.EepromProgramming5_ShadowMode
        # Write the modified value back to the EepromProgramming5 register
        self.write(self.EepromProgramming5, eeprom_reg5)


    def configure_CONFIG1(self, RMValue: int = 0b0111011, ClkCycleAdjust: bool = True, FGCycle: int = 0b0111, FGOLSel: int = 0b00, SSMConfig: int = 0b11):
        """
        Configure the CONFIG1 register.

        Args:
            RMValue (int): RMValue + RMShift (7-bit value).
            ClkCycleAdjust (bool): 0: Full-cycle adjust, 1: Half-cycle.
            FGCycle (int): FG motor pole count (4-bit value).
            FGOLSel (int): FG Open-loop output select (2-bit value).
            SSMConfig (int): Spread spectrum modulation control (2-bit value).
        """
        bit_values = {
            0: RMValue,           # RMValue + RMShift
            7: ClkCycleAdjust,    # 0: Full-cycle adjust, 1: Half-cycle
            8: FGCycle,           # FG motor pole count
            12: FGOLSel,          # FG Open-loop output select
            14: SSMConfig,        # Spread spectrum modulation control
        }
        self._write_config_register(self.CONFIG1, bit_values)

    def configure_CONFIG2(self, KtValue: int = 0x28, CommAdvMode: int = 0, TCtrlAdvValue: int = 0b0111011):
        """
        Configure the CONFIG2 register.

        Args:
            KtValue (int): BEMF Kt value (8-bit value).
            CommAdvMode (int): Commutation advanced value (1-bit value).
            TCtrlAdvValue (int): Commutation advanced mode (1-bit value).
        """
        bit_values = {
            0: TCtrlAdvValue,    # Commutation advanced value
            7: CommAdvMode,      # Commutation advanced mode
            8: KtValue,          # BEMF Kt value
        }
        self._write_config_register(self.CONFIG2, bit_values)

    def configure_CONFIG3(self, BrkDoneThr: int = 0b111, OpLCurrRt: int = 0b11, OpLCurr: int = 0b11, RvsDrThr: int = 0, RvsDrEn: int = 0, ISDEn: int = 1, BEMF_HYS: int = 0, BrkCurThrSel: int = 0, ISDThr: int = 0):
        """
        Configure the CONFIG3 register.

        Args:
            BrkDoneThr (int): Braking mode setting (3-bit value).
            OpLCurrRt (int): Open-loop current ramp-up setting (2-bit value).
            OpLCurr (int): Open-loop current setting (3-bit value).
            RvsDrThr (int): The threshold where the device starts to process reverse drive or brake (2-bit value).
            RvsDrEn (int): Reverse drive (1-bit value).
            ISDEn (int): Initial speed detect (1-bit value).
            BEMF_HYS (int): 0: low hysteresis 20mV for BEMF comparator, 1: high 40mV (1-bit value).
            BrkCurThrSel (int): Brake current-level-threshold selection (1-bit value).
            ISDThr (int): ISD stationary judgment threshold (1-bit value).
        """
        bit_values = {
            0: BrkDoneThr,       # Braking mode setting
            3: OpLCurrRt,        # Open-loop current ramp-up setting
            6: OpLCurr,          # Open-loop current setting
            8: RvsDrThr,         # The threshold where the device starts to process reverse drive or brake
            10: RvsDrEn,         # Reverse drive
            11: ISDEn,           # Initial speed detect
            12: BEMF_HYS,        # 0: low hysteresis 20mV for BEMF comparator, 1: high 40 mV
            13: BrkCurThrSel,    # Brake current-level-threshold selection
            14: ISDThr,          # ISD stationary judgment threshold
        }
        self._write_config_register(self.CONFIG3, bit_values)

    def configure_CONFIG4(self, AlginTime: int = 0b011, Op2ClsThr: int = 0b1111, StAccel: int = 0b0101000, AccelRangeSel: int = 0):
        """
        Configure the CONFIG4 register.

        Args:
            AlginTime (int): Align time (3-bit value).
            Op2ClsThr (int): Typical open-to-closed loop threshold (frequency) (5-bit value).
            StAccel (int): Open-loop start-up acceleration (6-bit value).
            AccelRangeSel (int): Accel range selection (1-bit value).
        """
        bit_values = {
            0: AlginTime,        # Align time
            3: Op2ClsThr,        # Typical open-to-closed loop threshold (frequency)
            8: StAccel,          # Open-loop start-up acceleration
            14: AccelRangeSel,   # Accel range selection
        }
        self._write_config_register(self.CONFIG4, bit_values)

    def configure_CONFIG5(self, IPDasHwILimit: int = 0b1, HWiLimitThr: int = 0b111, SWiLimitThr: int = 0b111, LockEn0: int = 0, LockEn1: int = 0, LockEn2: int = 0, LockEn3: int = 0, LockEn4: int = 0, LockEn5: int = 0, OTWarningLimit: int = 0b1):
        """
        Configure the CONFIG5 register.

        Args:
            IPDasHwILimit (int): Range of current limit for lock detection (1-bit value).
            HWiLimitThr (int): Current limit for lock detection (3-bit value).
            SWiLimitThr (int): Software current limit threshold (4-bit value).
            LockEn0 (int): Lock-detection current limit for normal lock (1-bit value).
            LockEn1 (int): Abnormal speed lock detect (1-bit value).
            LockEn2 (int): Abnormal Kt lock detect (1-bit value).
            LockEn3 (int): No motor fault lock detect (1-bit value).
            LockEn4 (int): Open-loop stuck lock detect (1-bit value).
            LockEn5 (int): Closed-loop stuck lock detect (1-bit value).
            OTWarningLimit (int): Over-temperature warning current limit (1-bit value).
        """
        bit_values = {
            0: IPDasHwILimit,       # Range of current limit for lock detection
            1: HWiLimitThr,         # Current limit for lock detection
            4: SWiLimitThr,         # Software current limit threshold
            8: LockEn0,             # Lock-detection current limit: 1=En
            9: LockEn1,             # Abnormal speed, 1=en
            10: LockEn2,            # Abnormal Kt, 1=en
            11: LockEn3,            # No motor fault, 1=En
            12: LockEn4,            # Open-loop stuck, 1=en
            13: LockEn5,            # Closed-loop stuck, 1=En
            14: OTWarningLimit,     # Over-temperature warning current limit
        }
        self._write_config_register(self.CONFIG5, bit_values)

    def configure_CONFIG6(self, SlewRate: int = 0b11, DutyCycleLimit: int = 0b00, ClsLpAccel: int = 0b11, CLoopDis: int = 0, IPDRIsMd: int = 0b1, AVSMMd: int = 0b1, AVSMEn: int = 0b1, AVSIndEn: int = 0b1, KtLckThr: int = 0, PWMfreq: int = 0, SpedCtrlMd: int = 0):
        """
        Configure the CONFIG6 register.

        Args:
            SlewRate (int): Slew-rate control for phase node (2-bit value).
            DutyCycleLimit (int): Minimum duty-cycle limit (2-bit value).
            ClsLpAccel (int): Closed-loop accelerate (1-bit value).
            CLoopDis (int): 0: transfer to closed-loop enabled, 1: transfer to closed-loop disabled (1-bit value).
            IPDRIsMd (int): IPD release mode; 0=break when inductive release, 1=Hi-z when inductive release (1-bit value).
            AVSMMd (int): Mechanical AVS mode, 0: to Vcc, 1: to 24V (1-bit value).
            AVSMEn (int): Enable mechanical AVS, 1: enable (1-bit value).
            AVSIndEn (int): Enable inductive AVS, 1: enable (1-bit value).
            KtLckThr (int): Abnormal Kt lock detect threshold (1-bit value).
            PWMfreq (int): PWM frequency control, 0: 25kHz, 1: 50kHz (1-bit value).
            SpedCtrlMd (int): 0: Analogue input at SPEED pin, 1: PWM input at SPED pin (1-bit value).
        """
        bit_values = {
            0: SlewRate,                # Slew-rate control for phase node
            2: DutyCycleLimit,          # Minimum duty-cycle limit
            4: ClsLpAccel,              # Closed-loop accelerate
            7: CLoopDis,                # 0: transfer to closed-loop enabled, 1: transfer to closed-loop disabled
            8: IPDRIsMd,                # IPD release mode; 0=break when inductive release, 1=Hi-z when inductive release
            9: AVSMMd,                  # Mechanical AVS mode, 0: to Vcc, 1: to 24V
            10: AVSMEn,                  # Enable mechanical AVS, 1: enable
            11: AVSIndEn,                # Enable inductive AVS, 1: enable
            12: KtLckThr,                # Abnormal Kt lock detect threshold
            14: PWMfreq,                 # PWM frequency control, 0: 25kHz, 1: 50kHz
            15: SpedCtrlMd,              # 0: Analogue input at SPEED pin, 1: PWM input at SPED pin
        }
        self._write_config_register(self.CONFIG6, bit_values)

    def configure_CONFIG7(self, DeadTime: int = 0b1010, CtrlCoef: int = 0b01, IPDClk: int = 0b10, IPDCurrThr: int = 0b1111, IPDAdvcAg: int = 0b01):
        """
        Configure the CONFIG7 register.

        Args:
            DeadTime (int): Driver dead time (5-bit value).
            CtrlCoef (int): SCORE control constant (3-bit value).
            IPDClk (int): Inductive sense clock (2-bit value).
            IPDCurrThr (int): IPD (inductive sense) current threshold (4-bit value).
            IPDAdvcAg (int): Advance angle after inductive sense, 0: 30 deg, 1: 60deg, 2: 90deg, 3: 120 deg (2-bit value).
        """
        bit_values = {
            0: DeadTime,            # Driver dead time
            5: CtrlCoef,            # SCORE control constant
            8: IPDClk,              # Inductive sense clock
            10: IPDCurrThr,         # IPD (inductive sense) current threshold
            14: IPDAdvcAg,          # Advance angle after inductive sense, 0: 30 deg, 1: 60deg, 2: 90deg, 3: 120 deg
        }
        self._write_config_register(self.CONFIG7, bit_values)

    def decode_FaultReg(self, fault_register: int) -> dict:
        """
        Decode the fault register and return a dictionary with decoded status flags.

        Args:
            fault_register (int): The value of the fault register.

        Returns:
            dict: Dictionary containing the decoded status flags from the fault register.
        """
        fault_flags = {
            "Lock0": bool(fault_register & 0b1),
            "Lock1": bool(fault_register & 0b10),
            "Lock2": bool(fault_register & 0b100),
            "Lock3": bool(fault_register & 0b1000),
            "Lock4": bool(fault_register & 0b10000),
            "Lock5": bool(fault_register & 0b100000),
            "V3P3_UVLO": bool(fault_register & 0b10000000),
            "VCC_UVLO": bool(fault_register & 0b100000000),
            "VREG_UVLO": bool(fault_register & 0b1000000000),
            "CP_UVLO": bool(fault_register & 0b10000000000),
            "OverCurr": bool(fault_register & 0b100000000000),
            "VREG_OC": bool(fault_register & 0b1000000000000),
            "VCC_OC": bool(fault_register & 0b10000000000000),
            "TempWarning": bool(fault_register & 0b100000000000000),
            "OverTemp": bool(fault_register & 0b1000000000000000),
        }

        return fault_flags

    def read_status_registers(self) -> dict:
        """
        Read status registers and return them as a dictionary.

        Returns:
            dict: Dictionary containing the status registers with their names as keys.

        Note:
            The dictionary returned by this function will have the following structure:

            {
                "FaultFlags": {  # Status flags from the FaultReg register
                    "Lock0": bool,         # True if Lock0 flag is set, False otherwise
                    "Lock1": bool,         # True if Lock1 flag is set, False otherwise
                    "Lock2": bool,         # True if Lock2 flag is set, False otherwise
                    "Lock3": bool,         # True if Lock3 flag is set, False otherwise
                    "Lock4": bool,         # True if Lock4 flag is set, False otherwise
                    "Lock5": bool,         # True if Lock5 flag is set, False otherwise
                    "V3P3_UVLO": bool,     # True if V3P3_UVLO flag is set, False otherwise
                    "VCC_UVLO": bool,      # True if VCC_UVLO flag is set, False otherwise
                    "VREG_UVLO": bool,     # True if VREG_UVLO flag is set, False otherwise
                    "CP_UVLO": bool,       # True if CP_UVLO flag is set, False otherwise
                    "OverCurr": bool,      # True if OverCurr flag is set, False otherwise
                    "VREG_OC": bool,       # True if VREG_OC flag is set, False otherwise
                    "VCC_OC": bool,        # True if VCC_OC flag is set, False otherwise
                    "TempWarning": bool,   # True if TempWarning flag is set, False otherwise
                    "OverTemp": bool       # True if OverTemp flag is set, False otherwise
                },
                "MotorSpeed": float,      # Speed of the motor in Hz
                "BEMF_KT": float,         # BEMF value in volts per Hz
                "MotorCurrent": float,    # Current of the motor in amperes
                "SupplyVoltage": float,   # Supply voltage in volts
                "Power": float,           # Power consumption in watts
                "SpeedCmd": float,        # Speed command in percentage (duty cycle)
                "SpeedBuff": float,       # Speed buffer in percentage (duty cycle)
                "IPD": int                # Inductive Position Detect value
            }
        """
        FaultReg = self.read(self.FaultReg)
        MotorSpeed = self.read(self.MotorSpeed) / 10
        MotorPeriod = self.read(self.MotorPeriod) * 10
        MotorXt = self.read(self.MotorXt)/2/1090
        MotorCurrent = self.read(self.MotorCurrent)
        if MotorCurrent>=1023:
            MotorCurrent -= 1023
        MotorCurrent /= 512.0
        SupplyVoltageReg = self.read(self.SupplyVoltage)
        SupplyVoltage = (SupplyVoltageReg & 0b11111111) * 30 / 255
        SpeedCmd = self.read(self.SpeedCmd)

        fault_flags = self.decode_FaultReg(FaultReg)

        status_registers = {
            "FaultFlags": fault_flags,
            "MotorSpeed": MotorSpeed * (1 / (16 / 2)),
            "MotorPeriod": MotorPeriod,
            "BEMF_KT": MotorXt,
            "MotorCurrent": MotorCurrent,
            "SupplyVoltage": SupplyVoltage,
            "Power": MotorCurrent * SupplyVoltage,
            "SpeedCmd": (SpeedCmd >> 8) * 100.0 / 255,
            "SpeedBuff": (SpeedCmd & 0xff) * 100.0 / 255,
            "IPD": ((SupplyVoltageReg >> 8) - 1),
        }

        return status_registers

def print_status_registers(status_registers: dict):
    """
    Print the status registers with a formatted output.

    Args:
        status_registers (dict): A dictionary containing the decoded status values
            for different registers.

    Note:
        The input dictionary should have the same structure as the one returned by
        the `read_status_registers` function.

    """
    print("")
    print("Status Registers:")
    print("-----------------")

    print("Status Registers:")
    print("Fault Flags: {}".format(status_registers["FaultFlags"]))
    print("Motor Speed: {:0.3f} Hz  ({:0.2f} RPM)".format(status_registers["MotorSpeed"], status_registers["MotorSpeed"] * 60))
    print("Motor Period: {:0.3f} us".format(status_registers["MotorPeriod"]))
    print("BEMF (KT): {:0.3f} V/Hz".format(status_registers["BEMF_KT"]))
    print("Motor Current: {:0.2f} A".format(status_registers["MotorCurrent"]))
    print("Supply Voltage: {:0.2f} V".format(status_registers["SupplyVoltage"]))
    print("Power: {:0.2f} W".format(status_registers["Power"]))
    print("Speed Command: {:0.2f} % (duty)".format(status_registers["SpeedCmd"]))
    print("Speed Buffer: {:0.2f} % (duty)".format(status_registers["SpeedBuff"]))
    print("IPD: {}".format(status_registers["IPD"]))
    print("-----------------")

