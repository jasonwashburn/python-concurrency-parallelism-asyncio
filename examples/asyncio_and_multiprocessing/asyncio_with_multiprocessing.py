import asyncio
import concurrent.futures
import time
from math import floor
from multiprocessing import cpu_count

import aiofiles
import aiohttp
from bs4 import BeautifulSoup


async def get_and_scrape_pages(num_pages: int, output_file: str):
    """
    Makes {{ num_pages }} requests to Wikipedia to receive {{ num_pages }} random
    articles, then scrapes each page for its title and appends it to {{ output_file }},
    seperating each title with a tab: "\\t"

    Args:
        num_pages (int): Number of random Wikipedia pages to request and scrape
        output_file (str): File to append titles to
    """
    async with aiohttp.ClientSession() as client, aiofiles.open(
        output_file, "a+", encoding="utf-8"
    ) as f:

        for _ in range(num_pages):
            async with client.get(
                "https://en.wikipedia.org/wiki/Special:Random"
            ) as response:
                if response.status > 399:
                    # Original Author was getting a 429 Too Many Requests
                    # at a higher volume of requests
                    response.raise_for_status()

                    page = await response.txt()
                    soup = BeautifulSoup(page, features="html.parser")
                    title = soup.find("h1").text

                    await f.write(title + "\t")

        await f.write("\n")


def start_scraping(num_pages: int, output_file: str, i: int):
    """
    Starts an async process for requesting and scraping Wikipedia pages

    Args:
        num_pages (int): number of wikipedia articles to scrape
        output_file (str): file to output to
        i (int): number of the running process
    """
    print(f"Process {i} starting...")
    asyncio.run(get_and_scrape_pages(num_pages, output_file))
    print(f"Process {i} finished.")


def main():
    NUM_PAGES = 100
    NUM_CORES = cpu_count()
    OUTPUT_FILE = "./wiki_titles.tsv"

    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    PAGES_FOR_FINAL_CORE = PAGES_PER_CORE + NUM_PAGES % PAGES_PER_CORE

    futures = []

    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executer:
        for i in range(NUM_CORES - 1):
            new_future = executer.submit(
                start_scraping, num_pages=PAGES_PER_CORE, output_file=OUTPUT_FILE, i=i
            )
            futures.append(new_future)

        futures.append(
            executer.submit(
                start_scraping, PAGES_FOR_FINAL_CORE, OUTPUT_FILE, NUM_CORES - 1
            )
        )

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Time to complete: {round(time.time() - start, 2)} seconds.")
