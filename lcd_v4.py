import os
import sys
import time
import logging
import spidev as SPI
import libcamera
from PIL import Image, ImageDraw, ImageFont
from lib import LCD_1inch8
import numpy as np
from picamera2 import Picamera2, Preview
from PIL import Image
from gpiozero import Button

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

# Initialize the button
button = Button(26)

# Initialize the LCD display
disp = LCD_1inch8.LCD_1inch8()
Lcd_ScanDir = LCD_1inch8.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
# Initialize library.
disp.Init()
# Clear display.
disp.clear()
# Set the backlight to 50%
disp.bl_DutyCycle(100)

# Initialize the camera using picamera2
picam2 = Picamera2()
# Set the preview resolution (for example, 2560x1440)
#preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})

# Set the still capture resolution (for example, 4000x3000)
still_config = picam2.create_still_configuration(main={"size": (2000, 1500)})

# Apply both configurations (preview and still capture)
#picam2.configure(preview_config)
picam2.configure(still_config)
# Start the preview
# picam2.start_preview(Preview.QTGL)
picam2.start()
image = Image.new("RGB", (disp.width, disp.height), "WHITE")
draw = ImageDraw.Draw(image)
font18 = ImageFont.truetype("Font/Font00.ttf",18) 

# Preview loop
try:
    while True:
        # Wait for button press
        
        
        
        logging.info("draw text")
        draw.text((5, 40), 'Waiting', fill = "BLACK",font=font18)
        disp.ShowImage(image)

        if button.is_pressed:

            draw = ImageDraw.Draw(image)
            logging.info("draw text")
            draw.text((5, 40), 'taking photo', fill = "BLACK",font=font18)

            # Capture a frame from the camera
            frame_data = picam2.capture_array()

            # Convert the frame to a PIL image
            image = Image.fromarray(frame_data)

            # Resize the image to fit the LCD screen (160x128)
            image = image.resize((160, 128))

            # Show the image on the LCD
            disp.ShowImage(image)

            # Save the image with a unique filename based on the time
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"/home/andres/Desktop/camera_lego/DCMI/{timestamp}.jpg"
            picam2.capture_file(filename)

            # Sleep for a moment to avoid repeated captures
            time.sleep(1)
            #disp.clear()
            disp.ShowImage(image)
            
        else:
            # If the button isn't pressed, sleep for a short time
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Preview interrupted.")

# Clean up
picam2.stop_preview()
disp.module_exit()
