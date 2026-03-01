# 🤖 Desk Buddy Robot Motherboard

Welcome to the brain of the **Desk Buddy Robot**! This is a 100% custom-designed printed circuit board (PCB) built completely from scratch in KiCad.

I engineered this board over a massive 40-hour sprint to act as the central nervous system for a smart desktop companion. Instead of using messy breadboards and jumper wires, all the complex logic is integrated into a single, clean, 2-layer motherboard.

###  What's on the board:
* **The Core:** An ESP32 microcontroller handling all the processing, logic, and Wi-Fi.
* **Custom Memory:** A fully custom Micro SD Card circuit, engineered with proper 33-ohm resistors for high-speed signal integrity and its own dedicated 3.3V power plant.
* **Senses (Inputs):** A MEMS Microphone for hearing, an MQ-2 Gas sensor for environment tracking, and capacitive touch lines.
* **Expressions (Outputs):** Dual audio amplifiers for stereo sound, custom hardware-logic LED status indicators, and a dedicated header for a TFT screen face.

*Designed by ARNAB*
<img width="1261" height="886" alt="Screenshot 2026-03-01 at 5 03 58 PM" src="https://github.com/user-attachments/assets/8c3f953e-c70f-44d5-87f9-f774344674b5" />
