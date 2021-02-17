# MakeUofT_2021
Project for MakeUofT 2021

## Installation of packages

```bash
conda install -c conda-forge pyserial
conda install -c conda-forge matplotlib
```
## Project Details

**Electric circuit learning and automarker for high school students (potentially university students)**

Login system - allow users (teachers or students) to register and login, record the marks and analysis the trend of study
- For each student: must refer to a teacher, have username and password set
- For each teacher: have him/herself an account with username and password, have a list of students that is under the teacher’s name
- For mark analysis: from students’ view, can see their marks and trend, for teachers, can see the marks of all students and the trend

Prototype database - pre-draw circuits and record them. Setting solutions to be checked
- Main components of a circuit: battery, resistor, capacitor, potentiometer, thermistor
- Very simple and easy circuits including:
  - Parallel and serial connection of resistors
  - Estimate the resistance of a potentiometer
  - Design a specific current/resistance/voltage
  - How the thermistor resistance change due to temperature
  - RC circuit and output wave (hard/optional)

Marking system - read data from the real breadboard and send it to the software. Check the answers to the solutions and reflect the result in the form of a mark.
- Collect the voltage/resistor/current from the breadboard and send them to the software
- Compare the results with the solution and provide a mark for the overall performance
- Also, display the mark on an LCD
- Detection of potential sources of error?

## Project Pace Tracker

| Module/Part  | Name | Expected Finish Date |
| ------------- | ------------- | ------------- |
| Login System | Mengqi | Feb 17  |
| Login Database  | Mengqi  | Feb 17  |
| Circuit interface| Mengzhu  | Feb 17 |
| Circuits schematics | Mengzhu   | Feb 18  |
| Contents| Mengzhu & Xuening  | Feb 17  |
| Oscilloscope | Xuening   | Feb 16  |
| Other data detection| Xuening | Feb 17  |
| Arduino component | Xuening  | Feb 17  |
