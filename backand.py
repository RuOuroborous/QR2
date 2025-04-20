# backend.py - QR code generation logic

import qrcode
from PIL import Image
from io import BytesIO

def generate_qr_code(content, size=400):
    """
    Generate a QR code from the given content
    
    Args:
        content (str): The content to encode in the QR code
        size (int): The size of the QR code image in pixels
        
    Returns:
        PIL.Image: The generated QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img

def save_qr_code(image, filename):
    """
    Save the QR code image to a file
    
    Args:
        image (PIL.Image): The QR code image to save
        filename (str): The path to save the image to
    """
    image.save(filename)