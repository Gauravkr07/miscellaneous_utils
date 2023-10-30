"""
Script to upload resize images on aws bucket 
"""

import os
import boto3
from PIL import Image
import logging

access_key = "aws_access_key"
secret_key = "aws_secret_key"
bucket_name = "s3_bucket_name"

s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)


# Resize given images of directory
def compress_upload_image(src_path, s3_bucket_path, size):
    try:
        with Image.open(src_path) as im:
            im = im.resize((size, size), Image.ANTIALIAS)
            basename, extension = os.path.splitext(src_path)
            new_path = basename + f"_{size}x{size}" + extension
            im.save(new_path, quality=95)
            # print(new_path)

            s3.upload_file(new_path, bucket_name, s3_bucket_path)

            # print(f"Uploaded {src_path} {s3_bucket_path}")
            logging.info(f"Uploaded {new_path} in {s3_bucket_path}")
    except Exception as err:
        logging.error(f"Error in {src_path}")
        print("error in image resizing", str(err))


def process_directory(
    local_dir,
    s3_dir=None,
):
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            if file.lower().endswith((".jpeg", ".png")):
                local_path = os.path.join(root, file)
                s3_path = os.path.join(s3_dir, os.path.relpath(local_path, local_dir))
                # size is for length and breadth of image required
                compress_upload_image(local_path, s3_path, size=240)


if __name__ == "__main__":
    logging.info("Script is start running ")
    file_address = "/home/gaurav/Pictures/"
    s3_directory = "banners/content/"
    process_directory(file_address, s3_directory)
