# Cubesat

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

The OBSW was developed in Python, and the operating system on which the software runs is Raspberian, to which optimizations have been applied. <br>
The following optimizations have been made to improve overall system performance:

- Deactivating Wi-Fi Module,
- Deactivating Bluetooth Module,
- Deactivating Update Module,
- Deactivating UI


## User manual

### TS Phase

Running the script TS.py the OBC should begin testing sequence where the LED (idk) will blink confirming that it has detected every single sensor, camera and RF Module. <br>
After that, a TM is sent to the user via the RF Module with the standard format and a message indicating that the user can proceed to the main code.
### TMTC Format

A nominal TM should follow the following pattern:

- TimeStamp_Voltage_Temp_Load_AccX_AccY_AccZ_GyroX_GyroY_GyroZ_Att_Press
If the structure looks allright now you should take a look about every param:

1. <b>TimeStamp</b> should be a float (Eg. 1.00) because the OBC is using the internal clock of the RPI. [seconds]
2. <b>Voltage</b> should be in hex format (Eg. 0x00).

- 0x00 indicates that the voltage is nominal.
- 0x05 indicates that the OBC is undervoltage and the power supply should be checked.

3. <b>Temp</b> should be a float (Eg. 57.01) . [degrees]
4. <b>Acc</b> Represent the acceleration on each axis and should be a float [m/s^2]
5. <b>Gyro</b> Represent the rotation on each axis and should be float [deg/s]

params should be double

### SDCard
Because the RF module allows a relatively short data transmission distance, the video will be stored on the RPI's internal SD Card.
## Acronyms

- LEO - Low Earth Orbit
- OBSW - OnBoard Software
- UI - User Interface
- TS - Test Sequence
- OBC - OnBoard Computer
- TMTC - Telemetry/Telecommand

## About me

