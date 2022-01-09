"""
Asynchronous example
"""

import asyncio
import time

import aiofiles
import aiohttp


async def write_genre(file_name):
    """
    Uses genrenator from binaryjazz.us to write a random genre to the name of the given file

    Args:
        file_name (str): filename prefix to write files
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://binaryjazz.us/wp-json/genrenator/v1/genre/"
        ) as response:
            genre = await response.json()

    async with aiofiles.open(file_name, "w", encoding="utf-8") as new_file:
        print(f"Writing '{genre}' to '{file_name}'...")
        await new_file.write(genre)


async def main():
    """
    Main Loop
    """
    tasks = []

    for i in range(5):
        tasks.append(write_genre(f"./async/new_file{i}.txt"))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Starting...")
    start = time.time()

    asyncio.run(main())

    end = time.time()
    print(f"Time to complete asynchronous read/writes: {round(end - start, 2)} seconds")
