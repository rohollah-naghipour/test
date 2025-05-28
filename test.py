import os
from PIL import Image
import exifread
from datetime import datetime

def get_photo_metadata(image_path):
    """
    Extracts various metadata from a given image file.

    Args:
        image_path (str): The path to the image file.

    Returns:
        dict: A dictionary containing extracted metadata, or None if an error occurs.
    """
    metadata = {}
    try:
        # --- Basic Image Information using Pillow ---
        with Image.open(image_path) as img:
            metadata['Filename'] = os.path.basename(image_path)
            metadata['File Path'] = os.path.abspath(image_path)
            metadata['Image Format'] = img.format
            metadata['Width'] = img.width
            metadata['Height'] = img.height
            metadata['Mode'] = img.mode  # e.g., 'RGB', 'L', 'CMYK'

            # --- EXIF Data using exifread ---
            # Open image file for reading in binary mode
            with open(image_path, 'rb') as f:
                # Get EXIF tags
                tags = exifread.process_file(f)

                if tags:
                    for tag_name, tag_value in tags.items():
                        # We're interested in specific tags, you can add more
                        if tag_name not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                            # exifread returns objects, convert to string for readability
                            metadata[tag_name] = str(tag_value)

                    # --- Common EXIF Tags to look for and format ---
                    if 'EXIF DateTimeOriginal' in tags:
                        try:
                            dt_str = str(tags['EXIF DateTimeOriginal'])
                            metadata['Date Taken'] = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            metadata['Date Taken'] = dt_str # Keep original if parsing fails

                    if 'GPS GPSLatitude' in tags and 'GPS GPSLatitudeRef' in tags and \
                       'GPS GPSLongitude' in tags and 'GPS GPSLongitudeRef' in tags:
                        try:
                            latitude_raw = tags['GPS GPSLatitude'].values
                            latitude_ref = str(tags['GPS GPSLatitudeRef'])
                            longitude_raw = tags['GPS GPSLongitude'].values
                            longitude_ref = str(tags['GPS GPSLongitudeRef'])

                            # Convert GPS coordinates to decimal degrees
                            def convert_to_degrees(value):
                                d = float(value.num) / float(value.den)
                                m = float(value.num) / float(value.den)
                                s = float(value.num) / float(value.den)
                                return d + (m / 60.0) + (s / 3600.0)

                            lat = convert_to_degrees(latitude_raw[0]) + convert_to_degrees(latitude_raw[1]) / 60 + convert_to_degrees(latitude_raw[2]) / 3600
                            lon = convert_to_degrees(longitude_raw[0]) + convert_to_degrees(longitude_raw[1]) / 60 + convert_to_degrees(longitude_raw[2]) / 3600

                            if latitude_ref == 'S':
                                lat *= -1
                            if longitude_ref == 'W':
                                lon *= -1

                            metadata['GPS Latitude'] = f"{lat:.6f}"
                            metadata['GPS Longitude'] = f"{lon:.6f}"
                        except Exception as e:
                            metadata['GPS Info Error'] = f"Could not parse GPS data: {e}"
                else:
                    metadata['EXIF Data'] = "No EXIF data found."
    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")
        return None
    return metadata

def main():
    # Example usage:
    # 1. Process a single image
    single_image_path = "path/to/your/image.jpg" # <--- IMPORTANT: Change this to your image path
    if os.path.exists(single_image_path):
        print(f"\n--- Metadata for {os.path.basename(single_image_path)} ---")
        metadata = get_photo_metadata(single_image_path)
        if metadata:
            for key, value in metadata.items():
                print(f"  {key}: {value}")
    else:
        print(f"\nSkipping single image test: {single_image_path} does not exist.")

    # 2. Process all images in a directory
    image_directory = "path/to/your/photos/" # <--- IMPORTANT: Change this to your directory path
    if os.path.isdir(image_directory):
        print(f"\n--- Processing images in directory: {image_directory} ---")
        for filename in os.listdir(image_directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                full_path = os.path.join(image_directory, filename)
                print(f"\n--- Metadata for {filename} ---")
                metadata = get_photo_metadata(full_path)
                if metadata:
                    for key, value in metadata.items():
                        print(f"  {key}: {value}")
    else:
        print(f"\nSkipping directory test: {image_directory} is not a valid directory.")

if __name__ == "__main__":
    main()
