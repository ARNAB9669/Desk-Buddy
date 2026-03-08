# Desk Buddy V1

Desk Buddy is designed to be a "nerd desk partner" for students who spend long hours sitting at their desks. It is a smart, interactive companion to keep you company while you study or code!

## What Are These Files?
Everything you need to build Desk Buddy is right here:
* `robo.cpp`: The main Arduino code that runs on the ESP32 board.
* `app.py`: The Python WebSocket server that handles the AI brain.
* `BOM.csv`: The list of all the electronic components you need to buy.
* `.step` / `.stl` / `.f3d`: The 3D printing and CAD files for the robot's body.
* `DESK_BUDDY_V1_PCB.zip`: The Gerber files to print the custom circuit board.

## Dependencies & Libraries

Before you run the code, you need to install a few things.

**For the Python Server (app.py):**
Open your computer's terminal and run this exact command:
`pip install fastapi uvicorn websockets google-generativeai gtts python-dotenv`

**For the ESP32 (robo.cpp):**
Open your Arduino IDE, go to the Library Manager, and install these:
* **WebSockets** by Markus Sattler (Use the latest version)
* **Adafruit GFX Library** by Adafruit
* **Adafruit ST7735 and ST7789 Library** by Adafruit

## How To Make It Yourself

Follow these detailed steps to build your own Desk Buddy:

1. **Download:** Download or clone all the files from this repository.
2. **Shop:** Buy all the hardware components listed in the `BOM.csv` file.
3. **Print:** 3D print the body parts using the `.stl` files and order the custom PCB using the zip file.
4. **Solder:** Solder all the electronic components onto the PCB according to the pin map.
5. **Assemble:** Put the soldered electronics inside the 3D-printed body and close it up.
6. **Setup the AI:** Create a file named `.env` in the same folder as `app.py`. Put your Gemini API key inside it like this: `GEMINI_API_KEY=your_key_here`. 
7. **Run it:** Start the Python server, upload the `robo.cpp` code to your ESP32 (make sure to put your Wi-Fi name and password in the code first!), and you are good to go!

*Note: In the future, I will make a YouTube tutorial showing exactly how to assemble this step-by-step. When I finish it, I will put the video link right here.*

## Fun Fact
It took me over 42 hours to code and design this project so far! It is crazy. I actually have the full screen-recording of the process in a timelapse using the Lapse tool.

## Gallery
Here are some images of the design and setup:

<img width="861" height="855" alt="Screenshot 2026-03-09 at 12 40 12 AM" src="https://github.com/user-attachments/assets/39faeec3-0679-45ba-b742-0d1c5f8f2f3f" />

<img width="1419" height="811" alt="Screenshot 2026-03-09 at 12 41 01 AM" src="https://github.com/user-attachments/assets/3b8b1599-9a80-4926-bc52-143be1504e7d" />

<img width="1913" height="1076" alt="Screenshot 2026-03-09 at 12 41 50 AM" src="https://github.com/user-attachments/assets/c3776b3b-9681-4873-affc-7152fb9058bb" />

<img width="787" height="603" alt="Screenshot 2026-03-09 at 12 43 44 AM" src="https://github.com/user-attachments/assets/6606f465-81a3-4c1c-97cc-e68cc9d70ee9" />

<img width="845" height="700" alt="Screenshot 2026-03-09 at 12 42 36 AM" src="https://github.com/user-attachments/assets/e0d66218-08bf-41b9-b0f1-88d87e4f4736" />

<img width="932" height="681" alt="Screenshot 2026-03-09 at 12 43 11 AM" src="https://github.com/user-attachments/assets/3585ebfb-3c6a-4437-8655-dc056ce34b79" />

<img width="768" height="585" alt="Screenshot 2026-03-09 at 12 43 29 AM" src="https://github.com/user-attachments/assets/cbf6915e-8cce-49b8-bfcb-9673fe6fc4ed" />
This is how evrything is connected 
<img width="1376" height="879" alt="Screenshot 2026-03-09 at 1 20 52 AM" src="https://github.com/user-attachments/assets/523bb76a-35a9-4d37-92b3-6c6b8a09c7e4" />



---
*WHOM TO THANKS - - YEAH ITS ME YOUR BRO ARNAB*
