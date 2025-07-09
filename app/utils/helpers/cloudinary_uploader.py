# app/utils/cloudinary_uploader.py
import cloudinary
import cloudinary.uploader
from flask import current_app
from typing import BinaryIO # For type hinting file-like objects

def init_cloudinary():
    """
    Initializes Cloudinary configuration using credentials from Flask's current_app config.
    This function should be called before any Cloudinary upload/delete operations.
    """
    cloudinary.config(
        cloud_name=current_app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=current_app.config.get('CLOUDINARY_API_KEY'),
        api_secret=current_app.config.get('CLOUDINARY_API_SECRET')
    )

def upload_qr_code_to_cloudinary(file_stream: BinaryIO, public_id: str) -> str:
    """
    Uploads a QR code image to Cloudinary.
    The image is stored in a dedicated 'qr_codes' folder on Cloudinary.

    :param file_stream: A BytesIO object (or any file-like object) of the image to upload.
    :param public_id: A unique identifier for the image within Cloudinary.
                      It's recommended to use the QR code's UUID for this.
    :return: The secure URL of the uploaded image on Cloudinary.
    :raises Exception: If the Cloudinary upload fails.
    """
    init_cloudinary() # Ensure Cloudinary is configured
    try:
        response = cloudinary.uploader.upload(
            file_stream,
            public_id=f"{public_id}", # Stores image with the given public_id
            folder="qr_codes", # Explicitly set folder
            resource_type="image" # Specify resource type as image
        )
        # Cloudinary's upload response contains various details, 'secure_url' is the HTTPS URL
        return response['secure_url']
    except Exception as e:
        # Log the error for debugging purposes
        current_app.logger.error(f"Cloudinary upload failed for public_id '{public_id}': {e}")
        # Re-raise the exception to be handled by the calling function/endpoint
        raise

def delete_qr_code_from_cloudinary(public_id: str):
    """
    Deletes a QR code image from Cloudinary.

    :param public_id: The public_id of the image to delete. This should match
                      the public_id used during the upload (e.g., "qr_codes/your_uuid").
    """
    init_cloudinary() # Ensure Cloudinary is configured
    try:
        # Cloudinary's destroy method requires the full public_id including the folder path
        cloudinary.uploader.destroy(f"qr_codes/{public_id}", resource_type="image")
        current_app.logger.info(f"Cloudinary image '{public_id}' deleted successfully.")
    except Exception as e:
        # Log the error. Depending on application requirements, you might
        # choose to re-raise the exception or just log if deletion failure
        # is not critical (e.g., if the record is already gone from DB).
        current_app.logger.error(f"Cloudinary deletion failed for public_id '{public_id}': {e}")
        # Example: raise if you want to ensure deletion is critical
        # raise

