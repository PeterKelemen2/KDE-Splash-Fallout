import os
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Define the terminal string
terminal_string = '''********* NOBARA-LINUX V41.0.0 **********

COPYRIGHT 2075 ROBCO(R)
LOADER V6.13.7
EXEC VERSION 41.0
64k RAM SYSTEM
38911 BYTES FREE
NO HOLOTAPE FOUND
LOAD ROM(1): DEITRIX 303'''

def split_text(text, part_size):
    """Incrementally adds parts to the list."""
    result = []
    for i in range(0, len(text), part_size):
        result.append(text[:i + part_size])  # Just build up text, no cursor yet
    return result

def display_terminal(text_list, delay=0.5, font_path="FSEX302.ttf"):
    """Displays text progressively with a blinking cursor effect in an OpenCV window."""
    # Create a black image to display text
    height, width = 500, 1000  # Image size
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Load the Fixedsys font using Pillow
    try:
        font = ImageFont.truetype(font_path, size=20)
    except IOError:
        print("Font not found, using default.")
        font = ImageFont.load_default()

    # Convert image to Pillow format
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    font_color = (0, 255, 0)  # Green color text
    y_position = 50  # Start Y position for the text
    line_height = 30  # Distance between lines

    for i, part in enumerate(text_list):
        # Clear the image at the start of each iteration (overwrite previous frame)
        pil_image.paste((0, 0, 0), [0, 0, width, height])  # Clear to black
        
        # Add blinking cursor every even frame
        if i % 2 == 0:
            text = part + "█"  # Add cursor
        else:
            text = part  # No cursor

        # Split the text into lines if there are any line breaks
        lines = text.split('\n')

        # Render each line on the same position (override the previous)
        for line in lines:
            draw.text((30, y_position), line, font=font, fill=font_color)
            y_position += line_height  # Move to next line

        # Convert the image back to a NumPy array for OpenCV
        image = np.array(pil_image)

        # Show the image in a window
        cv2.imshow("Terminal", image)

        # Wait for the specified delay (milliseconds)
        key = cv2.waitKey(int(delay * 1000))  # Convert seconds to milliseconds
        if key == 27:  # Exit if ESC is pressed
            break
        
        # Reset y_position for the next iteration
        y_position = 50

    # Close the window
    cv2.destroyAllWindows()

def main():
    text_parts = split_text(terminal_string, 10)
    display_terminal(text_parts)

if __name__ == "__main__":
    main()
