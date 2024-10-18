# Raspberry Pi Pico Adventure: Sensor & Display Project

## Overview

This project demonstrates a Raspberry Pi Pico-based system that interfaces with various sensors and a 7-segment display. It is designed to simulate sensor readings and control elements using a Wokwi simulation environment.

The project includes:
- A **7-segment display** for numeric output.
- A **NTC temperature sensor** to simulate temperature readings.
- A **photoresistor (LDR)** to measure light intensity.
- A **slide potentiometer** to simulate analog input.
- A **pushbutton** for user interaction.

This project can be simulated directly on Wokwi, allowing you to experiment with the behavior of the different sensors and outputs.

## Features

- **7-Segment Display:** Displays numeric values controlled by the Raspberry Pi Pico.
- **NTC Temperature Sensor:** Reads and simulates temperature values.
- **Photoresistor (LDR):** Measures ambient light and changes output accordingly.
- **Slide Potentiometer:** Provides analog input simulation.
- **Pushbutton:** User interaction for control or triggering events.

## Components

The following components are connected to the Raspberry Pi Pico:

1. **Raspberry Pi Pico:** The microcontroller used to manage sensors and outputs.
2. **7-Segment Display:** Displays numeric data (connected to GP0 - GP11).
3. **NTC Temperature Sensor:** Outputs temperature data (connected to GP28).
4. **Photoresistor (LDR):** Measures light intensity (connected to GP26).
5. **Slide Potentiometer:** Provides variable analog input (connected to GP27).
6. **Pushbutton:** Simple user input (connected to GP16).

## Wiring Diagram

The wiring connections can be found in the `diagram.json` file. This file contains detailed information about how each component is connected to the breadboard and the Raspberry Pi Pico.

- The breadboard and components are wired according to the design specified in the `diagram.json` file.
- The Raspberry Pi Pico interacts with the sensors and display using GPIO pins.

## Simulation

This project can be simulated using Wokwi, a virtual hardware simulation platform. You can simulate the entire setup by visiting the following URL:

[Simulate on Wokwi](https://wokwi.com/projects/403865672358304769)

To run the simulation:
1. Visit the link above.
2. Observe the interaction between sensors and the 7-segment display in the virtual environment.

## How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/pico-sensor-display-project.git
   ```

2. **Open Wokwi Simulation:**
   - Run the project in Wokwi using the provided simulation link above, or by uploading the files manually to [Wokwi](https://wokwi.com).

3. **Modify Code:**
   - The main logic for the project is in the `main.py` file. You can modify this file to change the behavior of the sensors and display.

## Files

- `diagram.json`: Contains the wiring diagram for the project.
- `main.py`: Contains the main MicroPython code for running the project on the Raspberry Pi Pico.
- `wokwi-project.txt`: Contains the simulation link for the project on Wokwi.
