import cv2
import numpy as np


def apply_crt_warp(image, distortion=0.15):
    """Applies a CRT-style screen warp with subtle barrel distortion."""
    height, width = image.shape[:2]

    # Create normalized coordinate grid (-1 to 1)
    y, x = np.indices((height, width), dtype=np.float32)
    x = (x - width / 2) / (width / 2)
    y = (y - height / 2) / (height / 2)

    # Compute radial distance
    r = np.sqrt(x**2 + y**2)

    # Apply barrel distortion formula
    factor = 1 + distortion * (r**2)

    # Transform coordinates
    new_x = (x * factor) * (width / 2) + width / 2
    new_y = (y * factor) * (height / 2) + height / 2

    # Ensure new coordinates are within bounds
    new_x = np.clip(new_x, 0, width - 1)
    new_y = np.clip(new_y, 0, height - 1)

    # Remap image using OpenCV
    crt_warped = cv2.remap(
        image,
        new_x.astype(np.float32),
        new_y.astype(np.float32),
        interpolation=cv2.INTER_LINEAR,
    )

    return crt_warped


def add_crt_effect(image):
    """Apply a CRT-like effect to an image (scanlines, slight distortion, and optional noise)."""

    # Apply scanlines effect by drawing semi-transparent horizontal lines
    scanline_height = 3
    scanline_color = (255, 0, 0)  # Dark scanlines, but semi-transparent

    # Create scanlines effect by drawing lines on the image
    # for y in range(0, image.shape[0], scanline_height * 2):  # Every other line
    # cv2.line(image, (0, y), (image.shape[1], y), scanline_color, thickness=scanline_height)

    # Apply slight barrel distortion (simulating CRT curvature)
    height, width = image.shape[:2]
    center_x, center_y = width // 2, height // 2

    # Get the distance from the center for each pixel
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            distance = np.sqrt(dx**2 + dy**2)

            # Apply distortion based on distance from the center (weaken the effect here)
            factor = 1.0 + 0.00005 * distance  # Reduced the distortion factor
            new_x = int(center_x + factor * dx)
            new_y = int(center_y + factor * dy)

            # Bound the new coordinates to the image dimensions
            new_x = max(0, min(new_x, width - 1))
            new_y = max(0, min(new_y, height - 1))

            # Apply the pixel distortion
            image[y, x] = image[new_y, new_x]

    # Add noise (optional CRT static noise)
    # noise = np.random.randint(0, 10, (height, width, 3), dtype=np.uint8)  # Reduced noise intensity
    # image = cv2.addWeighted(image, 0.95, noise, 0.05, 0)  # Reduce the noise effect

    return image
