#! /usr/bin/python3

import smbus2 as smbus
import time

import keyboard

from MLAB_DRV10987 import MLAB_DRV10987
from MLAB_DRV10987 import print_status_registers


bus = smbus.SMBus(18)
drv = MLAB_DRV10987(bus)

# drv.set_shadow_mode()
# drv.disable_motor()
# drv.configure_CONFIG1()
# drv.configure_CONFIG2()
# drv.configure_CONFIG3()
# drv.configure_CONFIG4()
# drv.configure_CONFIG5()
# drv.configure_CONFIG6()
# drv.configure_CONFIG7()
# drv.enable_motor()

#drv.configure_CONFIG1(RMValue=0b0111011, ClkCycleAdjust=True, FGCycle=0b0000, FGOLSel=0b00, SSMConfig=0b00)
#drv.configure_CONFIG2(TCtrlAdvValue=0, CommAdvMode=0, KtValue=0x28)
#drv.configure_CONFIG3(BrkDoneThr=0, OpLCurrRt=0b111, OpLCurr=0, RvsDrThr=0, RvsDrEn=0, ISDEn=0, BEMF_HYS=0, BrkCurThrSel=0, ISDThr=0)
#drv.configure_CONFIG4(AlginTime=0, Op2ClsThr=0, StAccel=0, AccelRangeSel=0)
#drv.configure_CONFIG5(IPDasHwILimit=0, HWiLimitThr=0, SWiLimitThr=0, LockEn0=0, LockEn1=0, LockEn2=0, LockEn3=0, LockEn4=0, LockEn5=0, OTWarningLimit=0)
#drv.configure_CONFIG6(SlewRate=0, DutyCycleLimit=0, ClsLpAccel=0, CLoopDis=0, IPDRIsMd=0, AVSMMd=0, AVSMEn=0, AVSIndEn=0, KtLckThr=0, PWMfreq=0, SpedCtrlMd=0)
#drv.configure_CONFIG7(DeadTime=0, CtrlCoef=0, IPDClk=0, IPDCurrThr=0, IPDAdvcAg=0)


spd = 10
drv.set_SpeedCtrl(spd)


while(1):
    status = drv.read_status_registers()
    print_status_registers(status)
    time.sleep(0.2)

    if keyboard.is_pressed('down'):
        print('You Pressed down!')
        spd -= 1
        if spd < 0: spd=0
        drv.set_SpeedCtrl(spd)
        print("SPD", spd)
        time.sleep(0.1)
    if keyboard.is_pressed('up'):
        spd += 1
        if spd > 100: spd=100
        drv.set_SpeedCtrl(spd)
        print("SPD", spd)
        time.sleep(0.1)
