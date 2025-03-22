import os
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import info


def split_text(text, segment):
    """Incrementally adds parts to the list."""
    part_size = len(text) // segment
    result = []
    for i in range(0, len(text), part_size):
        result.append(text[: i + part_size])  # Just build up text, no cursor yet
    return result


def display_terminal(text_list, delay=0.5, font_path="FSEX302.ttf"):
    """Displays text progressively with a blinking cursor effect in an OpenCV window."""
    # Create a black image to display text
    height, width = 500, 1000  # Image size
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Load the font
    try:
        font = ImageFont.truetype(font_path, size=20)
    except IOError:
        print("Font not found, using default.")
        font = ImageFont.load_default()

    # Convert image to Pillow format
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    font_color = (0, 255, 0)  # Green text
    y_position = 50  # Fixed Y position (don't center vertically)
    line_height = 30  # Distance between lines

    for i, part in enumerate(text_list):
        # Clear the image
        pil_image.paste((0, 0, 0), [0, 0, width, height])

        # Add blinking cursor every even frame
        text = part
        # text = part + "█" if i % 2 == 0 else part

        # Split text into lines
        lines = text.split("\n")

        for line in lines:
            # Get text width for centering on X-axis
            text_width = draw.textbbox((0, 0), line, font=font)[2]  

            # Calculate X position to center the text
            x_position = (width - text_width) // 2

            # Draw text at (centered X, fixed Y)
            draw.text((x_position, y_position), line, font=font, fill=font_color)
            y_position += line_height  # Move to next line

        # Convert back to OpenCV format and show
        image = np.array(pil_image)
        cv2.imshow("Terminal", image)

        # Delay for effect
        key = cv2.waitKey(int(delay * 1000))
        if key == 27:  # ESC to exit
            break

        # Reset Y position for the next frame
        y_position = 50  

    # Keep window open after completing the text display
    while True:
        key = cv2.waitKey(1)  # Wait for any key press
        if key != -1:  # Exit the window on any key press
            break

    # Close window
    cv2.destroyAllWindows()




def main():
    terminal_string = info.create_terminal_string(same_length=True)
    print(terminal_string)

    frames, dur_sec = 50, 3
    text_parts = split_text(terminal_string, frames)
    display_terminal(text_parts, dur_sec / frames)


if __name__ == "__main__":
    main()
