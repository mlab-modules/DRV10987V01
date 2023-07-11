#! /usr/bin/python3

import smbus2 as smbus
import time

bus = smbus.SMBus(17)

addr = 0b1010010

def write(reg, d, debug = True):
    val = [(d>>8)&0xff, (d&0xff)]
    bus.write_i2c_block_data(addr, reg, val)
    if debug:
        print("Write:", hex(reg), hex(d))

def read(reg):
    a = bus.read_i2c_block_data(addr, reg, 2)
    #print(a)
    return (a[1]) | (a[0])<<8




write(0x35, 0b0001000000000000) # shadowed
write(0x60, 0b0000000000000000) 


print("0b{0:016b}".format(read(0x35)))

write(0x20, 0x3851)
write(0x21, 0x2d2d)


# write(0x90, 0xC05D)
# time.sleep(0.1)
# write(0x91, 0x4a49)
# time.sleep(0.1)
# write(0x92, 0x0081)
# time.sleep(0.1)
# write(0x93, 0x3792)
# time.sleep(0.1)
# write(0x94, 0x3baf)
# time.sleep(0.1)
# write(0x95, 0xd843)
# time.sleep(0.1)
# write(0x96, 0x006a)
# time.sleep(0.1)


# write(0x90, 0b0110001111111010)
# time.sleep(0.1)
# write(0x91, 0b0011110001001001)
# time.sleep(0.1)
# write(0x92, 0b0000000010001000)
# time.sleep(0.1)
# write(0x93, 0b0111001110111010)
# time.sleep(0.1)
# write(0x94, 0b11101110101111)
# time.sleep(0.1)
# write(0x95, 0x7840)
# time.sleep(0.1)
# write(0x96, 0x007A)
# time.sleep(0.1)

#write(0x92, 0b1111111111100000)
#write(0x94, 0b1111111111111111)


c = 0
c |= 0b0111010  # Rmvalue, odpor vinuti 
c |= 0b1 << 7
c |= 7 << 8
c |= 0b00 << 12
c |= 0b11 << 14
write(0x90, c)
time.sleep(0.1)

c = 0
c |= 0b0111011
c |= 0b0 << 7
c |= 0b101111 << 8
write(0x91, c)
#write(0x91, 0b10111100111011)
time.sleep(0.1)

write(0x92, 0x0050)
time.sleep(0.1)
write(0x93, 0x1bba)
time.sleep(0.1)

c = 0
c |= 0b0
c |= 0b110 << 1 # HW current limit
c |= 0b110 << 4
c |= 0b100000 << 8
c |= 0b01 << 14
write(0x94, c)
time.sleep(0.1)


write(0x95, 0x3c43)
time.sleep(0.1)

write(0x96, 0x016a)
time.sleep(0.1)

write(0x30, 0b1000000000000000 | 0b1111)


last_status = 0

while(1):
    time.sleep(0.25)
    d =  read(0x00)
    if last_status != d:
        print('0b{0:016b}'.format(d ))
        last_status = d
    write(0x00, 0xffff, False)


    
   # d = read(0x30)
   # print('0b{0:016b}'.format(d ))

