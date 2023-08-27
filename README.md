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
    2. MPU6050 Accelerometer and Gyroscope Sensor
    3. BMP280 Pressure Sensor
    4. Raspberry Pi Camera Module 2
    5. NRF20L01 Wireless Module
    6. Battery System 

### Software specs

The OBSW was developed in Python, and the operating system on which the software runs is Raspberian. <br>
The following optimizations have been made to improve overall system performance:

- Deactivating Wi-Fi Module
- Deactivating Bluetooth Module
- Deactivating Update Module
- Deactivating UI


## Guideline

### Initialization
The following steps should be performed before the core software will run:

1. Prepare the GCM by plug in the power source and run the receiver code

- A successful connection message should be displayed in the terminal.
- A warning message should appear to notify the failure to connect with the OBC.

2. Plug in OBC and follow the steps:

- Start OS Optimization code (OptiPiWizzard.py).[^1]
- Start Testing Phase.[^2]
- Run OnBoard Software code (OBSW.py).


### Testing Phase

Running the script <b>Test.py</b>, the OBC should begin testing sequence and a custom TM is sent to the GCM via the RFM that indicates the sensors has been detected. <br>
If the RFM is not working or is not responding the RED LED will blink continuously.<br>
If the RFM is working the GREEN LED will blink continuously and a TM will be send to the GCM with the following format:

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
8. <b>Pressure</b>[hPa] float (Eg. 1013.89) and represent the pressure applied to the CubeSat. <br>

<br>
One TM is sent every 5 seconds. <br>
Keep in mind that TMTC will only be available for a period of time until the CubeSat moves out of range of the GCM.

### SDCard

The entire CubeSat video flight will be stored on the video card. <br>
Also because the RFM allows communication over a relatively short distance with the GCM the flight parameters will be stored on the OBC's internal SD Card. <br>
The OBSW will notify the approaching maximum range and detect the loss of GCM connection, and the data will be passed in .txt(???) format. <br>

## Acronyms

- LEO - Low Earth Orbit
- OBSW - OnBoard Software
- UI - User Interface
- OBC - OnBoard Computer
- TMTC - Telemetry/Telecommand
- GCM - Ground Communication Module
- RFM - RF Module 

## About me

## Footnotes
[^1]: Go through the OS Optimization phase
[^2]: Go through the Testing phase

