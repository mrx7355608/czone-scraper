import os
import json
import time
import random
import cloudinary
from dotenv import load_dotenv
import cloudinary.uploader

# load .env file
load_dotenv()

# Cloudinary configurations
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def main():
    filenames = os.listdir("./backup_data")
    files_count = 0

    for filename in filenames:
        # 1. Read file
        items_list = read_file(filename)

        # 2. Upload images to cloudinary
        for index, item in enumerate(items_list):
            images = item["images"]
            category = item["category"]
            secure_urls = upload_images(images, category)
            print("Items Completed: ", index + 1)

            # 3. Replace the existing images links with the "secure_urls"
            # provided by the cloudinary
            item["images"] = secure_urls

            # 4. Add a small delay
            time.sleep(1)

        files_count += 1
        print("Files Completed: ", files_count)
        write_json_file("updated-" + filename, items_list)


# Upload image directly to cloudinary
def upload_images(images_to_upload, category):
    secure_urls = []

    for link in images_to_upload:
        try:
            img_link = "https://www.czone.com.pk" + link
            result = cloudinary.uploader.upload(
                img_link, folder=f"thrifty-gaming/{category}"
            )
            secure_urls.append(result["secure_url"])
        except Exception as e:
            print("--------------")
            print("     ERROR    ")
            print("--------------")
            print(str(e))
            continue

    return secure_urls


def read_file(filename):
    with open(f"./backup_data/{filename}", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def write_json_file(filename, items):
    print("--- Writing to file ---")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, indent=4)


def delay():
    timer = random.randint(2, 6)
    print(f"--- Sleeping for {timer} seconds ---")
    time.sleep(timer)  # Adds a random delay


main()
