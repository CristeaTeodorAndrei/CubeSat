# CubeSat

## Introduction

### About CubeSat

A CubeSat serves as a compact yet sophisticated space platform, designed with meticulous engineering to achieve targeted scientific objectives. These miniaturized satellites are crafted with precision and purpose, representing a cost-effective and efficient approach to space exploration. Their primary role revolves around specific scientific, technological, or educational missions. <br>
Equipped with specialized payloads, sensors, and instruments, CubeSats are deployed to gather critical data, monitor phenomena, or conduct experiments in space. These small wonders demonstrate engineering ingenuity, showcasing how intricate systems can be optimized to function flawlessly within a constrained space. Their modular nature allows for versatility, enabling CubeSats to address a diverse array of research goals, from Earth observation to studying cosmic phenomena. <br>
These diminutive pioneers contribute to the advancement of our understanding of the cosmos, proving that innovation can thrive even within the confines of a compact form factor.

### About the project

The project was developed with the goal of creating a mini-satellite that would photograph and film the Earth's curvature at about 30 kilometres above the ground. <br>
In order to reach the altitude of 30 kilometres the CubeSat will be lifted using a helium balloon and returned using a parachute. <br>
The future goal of this project is to reach LEO.

## CubeSat specifications

### Hardware specs

    1. Raspberry PI 4 Model B
    2. MPU6050 Accelerometer and Gyroscope Module
    3. BMP280 Pressure Sensor
    4. Raspberry Pi Camera Module 2
    5. NRF20L01 Wireless Module
    6. Battery System 

### Software specs

The OBSW was developed in Python, and the operating system on which the software runs is Raspberian. <br>
The following optimizations have been made to improve overall system performance:

- Deactivating Wi-Fi Module,
- Deactivating Bluetooth Module,
- Deactivating Update Module,
- Deactivating UI


## User manual

### TS Phase

Running the script <b>TS.py</b> the OBC should begin testing sequence and a custom TM is sent to the GCM via the RF Module that indicates the sensors has been detected. <br>
If the RF Module is not working or is not responding the RED LED will blink continuously.<br>
If the RF Module is working the GREEN LED will blink continuously and a TM will be send with the following format:

- [0x00, 0x00, 0x00, 0x00]

TM's params should have the following values:

1. (First) 0x00 - MPU6050 has been detected.

- 0x01 - MPU6050 has not been detected.

2. (Second) 0x00 - BMP280 has been detected.

- 0x01 - BMP280 has not been detected.

3. (Third) 0x00 - Camera Module has been detected.

- 0x01 - Camera Module has not been detected.

4. (Fourth) 0x00 - Power supply voltage is nominal.

- 0x05 - The OBC is undervoltage and the power supply should be verified.

### TMTC Format

A nominal TM should have the following format:

- [TimeStamp, Voltage, Temperature, Load, AccX, AccY, AccZ, GyroX, GyroY, GyroZ, Altitude, Pressure]

TM's params should have the following values:

1. <b>TimeStamp</b> [seconds] float (Eg. 1.00) and represent the relative time. 
2. <b>Voltage</b> hex format (Eg. 0x00).

- 0x00 indicates that the voltage is nominal.
- 0x05 indicates that the OBC is undervoltage and the power supply should be checked.

3. <b>Temperature</b>[degrees] float (Eg. 57.01) and represent the OBC's temperature.
4. <b>Load</b> [%] integer (Eg. 5%) and represent the OBC's load.
5. <b>Acceleration{X,Y,Z}</b>[m/s^2] float (Eg. 10.32) and represent the acceleration on each axis.
6. <b>Gyro{X,Y,Z}</b>[deg/s] float (Eg. 11.01) and represent the rotation on each axis.
7. <b>Altitude</b>[meters] integer (Eg. 1100) and represent the altitude of the CubeSat.
8. <b>Pressure</b>[hPa] float (Eg. 1013.89) and represent the pressure applied to the CubeSat.
Keep in mind that TMTC will only be available for a period of time until the CubeSat moves out of range of the GCM.

### SDCard

Because the RF module allows a relatively short data transmission distance, the whole flight video and params will be stored on the RPI's internal SD Card.

TBC
## Acronyms

- LEO - Low Earth Orbit
- OBSW - OnBoard Software
- UI - User Interface
- TS - Test Sequence
- OBC - OnBoard Computer
- TMTC - Telemetry/Telecommand
- GCM - Ground Communication Module

## About me

