# DRV10987V01 BLDC motor controller
This MLAB module features the [DRV10987](https://www.ti.com/lit/ds/symlink/drv10987.pdf?ts=1618316091180&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FDRV10987) controller by Texas Instruments, designed for sensorless operation of Brushless DC ([BLDC](https://en.wikipedia.org/wiki/Brushless_DC_electric_motor)) and Permanent Magnet Synchronous Motors ([PMSM](https://en.wikipedia.org/wiki/Synchronous_motor#Permanent-magnet)).

![](/doc/gen/img/DRV10987V01-bottom.svg) ![](/doc/gen/img/DRV10987V01-top.svg)


### Description
The DRV10987 is a three-phase, sensorless, brushless DC motor driver that carries out all necessary functions for ordinary operation of brushless motors. It is a powerful solution that is compact and easy to implement.

This module offers a straightforward way to integrate this potent driver into your project, whether you're a hobbyist, a researcher, or a professional engineer.
Specifications

 *   Power supply ranging from 6.2V to 28V for driving motors with diverse voltage requirements
 *   Provide a continuous current of 2A and peak current of 3A
 *   Can control motor speed based on PWM, analogue, or digital (I2C) input
 *   Contains an FG pin that can be used to monitor motor rotation
 *   Integrated Buck converter at 5V and 100mA for powering peripheral devices
 *   Brushless design that minimizes wear and enables quiet operation
 *   Sensorless commutation for easy installation and maintenance
 *   PWM input frequency up to 100kHz
 *   Communication via I2C interface
 *   Built-in functions for overload and overheat protection

### Applications

This MLAB module equipted with the DRV10987 controller is highly versatile and is ideal for several applications where efficient and reliable control of smaller motors is required. Some of the primary use cases include:

 * **Small Drones and RC Models**: Due to its compact size and efficient operation, the DRV10987 controller is commonly used in the design of smaller drones and radio-controlled models. These vehicles require precise, reliable motor control for stabilization and maneuverability, which this module can adequately provide.
 * **Robotic Systems**: In robotics, precise control of motor speed and direction is essential. The DRV10987 controller's ability to regulate speed based on PWM, analogue, or digital (I2C) input makes it suitable for smaller robotic applications, including hobbyist robots, robotic toys, and educational kits.
 * **Home Appliances**: Small electrical appliances, such as desk fans, can make use of the DRV10987 controller for efficient and quiet operation. The controller's brushless design minimizes wear, which enhances the lifespan and user experience of these devices.
 * **Hobby Projects**: For hobbyists and DIY enthusiasts, this module with the DRV10987 controller is a great tool for various projects requiring control of smaller BLDC or PMSM motors. Its ease of use and versatility make it a valuable component in prototyping and experimentation.


### Installation and Integration
Our MLAB modules are designed to be as straightforward as possible for integration into your project. To connect this module, you only need a standard power supply and an I2C bus for communication with the control system.

### DRV10987

The DRV10987 from Texas Instruments is a three-phase, sensorless motor driver engineered for brushless DC (BLDC) and Permanent Magnet Synchronous Motors (PMSM). It is designed to handle all necessary functions for the routine operation of brushless motors. Capable of delivering a continuous current of 2A and a peak current of 3A, the DRV10987 can control motor speed based on PWM, analogue, or digital (I2C) input. This versatile chip also features an FG pin for monitoring motor rotation and has an integrated Buck converter at 5V and 100mA for powering peripheral devices. With built-in functions for overload and overheat protection, the DRV10987 represents a robust, compact, and efficient solution for a range of applications that require reliable motor control.

Detailed technical information about the DRV10987 controller can be found in the datasheet, available on the manufacturer's website [here](https://www.ti.com/lit/ds/symlink/drv10987.pdf?ts=1618316091180&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FDRV10987).

### Schematics

[![](/doc/gen/DRV10987V01-schematic.svg)](/doc/gen/DRV10987V01-schematic.pdf)

### Conclusion
Regardless of whether you're building a sophisticated robotic system or a simple hobbyist project, this module with the DRV10987 controller from Texas Instruments is a powerful tool for sensorless control of BLDC and PMSM motors.
