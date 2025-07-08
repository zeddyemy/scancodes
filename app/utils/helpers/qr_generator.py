# app/utils/helpers/qr_generator.py
import qrcode
from io import BytesIO
from typing import Tuple

def generate_qr_code_image(data: str) -> Tuple[BytesIO, str]:
    """
    Generates a QR code image for the given string data.
    The image is returned as a BytesIO object, suitable for in-memory processing
    or direct uploading to cloud storage.

    :param data: The string data to encode in the QR code (e.g., a URL).
    :return: A tuple containing:
             - BytesIO object: The in-memory binary stream of the QR code image (PNG format).
             - str: The MIME type of the image (e.g., 'image/png').
    """
    # Create a QRCode object with specified parameters
    qr = qrcode.QRCode(
        version=1, # Controls the size and data capacity of the QR code (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L, # Error correction level (L, M, Q, H)
        box_size=10, # How many pixels each "box" (module) of the QR code is
        border=4, # How many boxes thick the white border around the QR code is
    )
    qr.add_data(data) # Add the data to be encoded
    qr.make(fit=True) # Compute the QR code structure, fitting the data

    # Create an image from the QR code data
    # fill_color: color of the QR code modules
    # back_color: color of the background
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to an in-memory byte array (BytesIO object)
    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG') # Save as PNG format
    byte_arr.seek(0) # Rewind the stream to the beginning, so it can be read from
    
    return byte_arr, 'image/png'