import os
import aiohttp
import asyncio
from urllib.parse import urlparse

url = 'https://storage.googleapis.com/panels-api/data/20240916/media-1a-i-p~s'

async def download_image(session, image_url, file_path):
    try:
        async with session.get(image_url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download image: {response.status}")
            content = await response.read()
            with open(file_path, 'wb') as f:
                f.write(content)
    except Exception as e:
        print(f"Error downloading image: {str(e)}")

async def download_images_concurrently(session, images_data, download_dir):
    tasks = []
    file_index = 1

    for key, subproperty in images_data.items():
        if subproperty and subproperty.get('dhd'):
            image_url = subproperty['dhd']
            # print(f"🔍 Found image URL!")

            parsed_url = urlparse(image_url)
            ext = os.path.splitext(parsed_url.path)[-1] or '.jpg'
            filename = f"{file_index}{ext}"
            file_path = os.path.join(download_dir, filename)

            task = asyncio.create_task(download_image(session, image_url, file_path))
            tasks.append(task)
            file_index += 1

    await asyncio.gather(*tasks)
    print(f"✅ All images downloaded!")

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"⛔ Failed to fetch JSON file: {response.status}")
                json_data = await response.json()
                data = json_data.get('data')

                if not data:
                    raise Exception('⛔ JSON does not have a "data" property at its root.')

                download_dir = os.path.join(os.getcwd(), 'downloads')
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                    print(f"📁 Created directory: {download_dir}")

                await download_images_concurrently(session, data, download_dir)

    except Exception as e:
        print(f"Error: {str(e)}")

def ascii_art():
    print("""
 /$$      /$$ /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$$
| $$$    /$$$| $$  /$$/| $$__  $$ /$$__  $$| $$__  $$
| $$$$  /$$$$| $$ /$$/ | $$  \\ $$| $$  \\__/| $$  \\ $$
| $$ $$/$$ $$| $$$$$/  | $$$$$$$ |  $$$$$$ | $$  | $$
| $$  $$$| $$| $$  $$  | $$__  $$ \\____  $$| $$  | $$
| $$\\  $ | $$| $$\\  $$ | $$  \\ $$ /$$  \\ $$| $$  | $$
| $$ \\/  | $$| $$ \\  $$| $$$$$$$/|  $$$$$$/| $$$$$$$/
|__/     |__/|__/  \\__/|_______/  \\______/ |_______/""")
    print("")
    print("🤑 Starting downloads from your favorite sellout grifter's wallpaper app...")

if __name__ == "__main__":
    ascii_art()
    asyncio.run(main())