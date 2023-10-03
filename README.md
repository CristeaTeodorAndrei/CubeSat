# CubeSat

## Introduction

### About CubeSat

A CubeSat is a compact but sophisticated space platform, meticulously engineered to achieve its scientific goals. These miniaturised satellites are created with precision and purpose, representing a cost-effective and efficient approach to space exploration. Their primary role involves specific scientific, technological or educational missions. <br>
Equipped with payloads, sensors and specialised instruments, CubeSats are deployed to collect critical data, monitor phenomena or conduct experiments in space. Their modular nature allows for versatility, enabling CubeSats to address a wide range of research objectives, from observing Earth to studying cosmic phenomena. <br>
They contribute to advancing our understanding of the cosmos, demonstrating that innovation can thrive even within the confines of a compact form factor.

### About the project

The project was developed with the objective of understanding the complexity of space systems, approaching the different problems that arise in this field and solving them in the most energy and cost efficient way. <br>
The future of this project consists in creating a stable platform that allows future improvements so that young students in this domain can develop.

## CubeSat specifications

### Hardware specs

    1. Raspberry PI 4 Model B
    2. MPU6050 Accelerometer and Gyroscope Sensor
    3. BMP280 Pressure Sensor
    4. Raspberry Pi Camera Module 2
    5. NRF20L01 Wireless Module
    6. Battery System UPS 

### Software specs

OBSW was developed in Python, and the operating system on which the software runs is Raspberian on which some software optimizations have been applied.  <br>
The project is structured in 4 phases:

- Activating Remote Control Phase
- Optimization phase
- Testing phase
- OBSW phase


<br>
Each of these phases has a well-defined objective and must be fulfilled before the final code runs.

## Guideline


### Activating Remote Control Phase

Keep in mind that each script that will run will be sent as a command through the GCM. <br>

Power on the GCM, run the script and open the receiver Interface.

- The Interface should prompt a successful connection message.
- A warning message should appear to notify the failure to connect with the OBC. <br>

Power on the OBC.

- Both GREEN and RED LEDs should be ON indicating that OBC is active and ready for requests.
- A succesful connection message should appear on GCM's Interface to ensure that communcations with the OBC is active and can proceed to the optimization phase.

<br>
GCM will try to connect with the OBC every 5 seconds.

### Optimization Phase

In order to reduce energy usage and ensure efficient performance of the whole system, a number of optimizations have been implemented:

- Deactivating Wi-Fi Module
- Deactivating Bluetooth Module
- Deactivating Update Module
- Deactivating UI

By requesting the OBC to run the script <b> Optimization.py</b> via GCM all of those optimizations will be applied and after that the OBC will reboot. <br>
After restarting the system, the GREEN LED will turn ON and RED LED OFF to indicate successful optimization and a confirmation message should appear. in GCM's Interface. <br>
<br>
OBC can proceed to the testing phase.

### Testing Phase

By requesting the OBC to run the script <b>Test.py</b>, the OBC begins testing sequence and a custom TM is sent back to the GCM that indicates the sensors has been detected. <br>
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

<br>
If the TM's values are not nominal OBSW will repeat the test every 5 seconds. <br>
OBC can proceed to the running phase or main code.

### Running phase

In the phase of running the main code all CubeSat components should work according to the parameters.
<br><br>
By requesting the OBC to run the main code <b>OBSW.py</b> nominal TMs should appear in GCM's Interface. <br>
As discussed in the SDCard chapter before the CubeSat leaves the range of the GCM the OBSW will send a warning message that it will soon disconnect and the data will be written locally. 
<br><br>
That's the final state for the CubeSat before the flight. 

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
Because the RFM allows communication over a relatively short distance with the GCM the flight parameters will be stored on the OBC's internal SD Card. <br>
The OBSW will notify the approaching maximum range and detect the loss of GCM connection, and the data will be passed in .txt format. <br>


## Acronyms

- LEO - Low Earth Orbit
- OBSW - OnBoard Software
- UI - User Interface
- OBC - OnBoard Computer
- TMTC - Telemetry/Telecommand
- GCM - Ground Communication Module
- RFM - Radio Frequency Module

## About me
