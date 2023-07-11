#! /usr/bin/python3

import smbus2 as smbus
import time

bus = smbus.SMBus(17)

addr = 0b1010010

def write(reg, d, debug = True):
    print([d>>8, d&0xff])
    bus.write_i2c_block_data(addr, reg, [d>>8, d&0xff])
    #bus.write_i2c_block_data(addr, reg, [d&0xff, d>>8])
    if debug:
        print(".......")
        print(bin(d), bin(d>>8), bin(d&0xff))
        print(bin(d))
        print("Write: 0x{0:02x}: 0b{0:016b}".format(reg, d))
        print("0b{0:08b}, 0b{0:08b}".format(d>>8, d&0xff))

        print('0b{0:016b}'.format(d ))

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
c |= 0b0111011  # Rmvalue, odpor vinuti 
c |= 0b1 << 7
c |= 7 << 8
c |= 0b00 << 12
c |= 0b11 << 14
write(0x90, c)
time.sleep(0.1)

c = 0
c |= 0b0111011
c |= 0b0 << 7
c |= 0b00000010 << 8   # Ktvalue
write(0x91, c)
#write(0x91, 0b10111100111011)
time.sleep(0.1)

c = 0
c |= 0b111
c |= 0b100 << 3
c |= 0b10 << 6
c |= 0b00 << 8
c |= 0b0 << 10 # Reverse
# ... 
write(0x92, c)
time.sleep(0.1)

c = 0
c |= 0b111 # align time
c |= 0b11111 << 3 # Open -> Close hz
c |= 0b011000 << 8 # Accel
c |= 0b1 << 14
write(0x93, c)
time.sleep(0.1)

c = 0
c |= 0b1
c |= 0b000 << 1 # HW current limit
c |= 0b001 << 4 # SW limit
c |= 0b100000 << 8
c |= 0b01 << 14
write(0x94, c)
time.sleep(0.1)


write(0x95, 0x3c43)
time.sleep(0.1)

write(0x96, 0x016a)
time.sleep(0.1)

#write(0x30, 0b1000000000000000 | 0b1000)



# Nastav rychlost, 
write(0x30, 0b1000000000000000 | 100)

last_status = 0

speed = 7
while(1):
    #speed += 1
    time.sleep(0.2)
    #print(speed)
    d =  read(0x00)
    if last_status != d:
        print('0b{0:016b}'.format(d ))
        last_status = d
    write(0x00, 0xffff, False)


   # write(0x30, 0b1000000000000000 | speed)



    
    d = read(0x06)
    print('speed 0b{0:016b}'.format(d ))



    d = read(0x05)
    print('Pwr {}V'.format( (d&0b11111111)*30/255 ))

    d = read(0x04)&0b11111111111
    if d>=1023:
        d -= 1023
    print('Curr {}A'.format( d/512.0 ))


    d = read(0x03)/2/1090
    print('Kt {} v/Hz'.format( d ))