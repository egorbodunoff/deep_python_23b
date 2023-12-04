from bs4 import BeautifulSoup
from collections import Counter
import asyncio
import aiohttp
import argparse


def get_url(file_name):
    try:
        with open(file_name, 'r') as urls:
            for url in urls:
                yield url.rstrip()

    except FileNotFoundError:
        yield 'File not found'


def response_process(data, k):
    soup = BeautifulSoup(data, 'html.parser')
    words = soup.get_text().split()

    popular_words = dict()
    for x in Counter(words).most_common(k):
        popular_words[x[0]] = x[1]

    return popular_words


async def fetch_content(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    popular_words = response_process(data, 2)
                else:
                    popular_words = 'No connection'

            return popular_words

    except aiohttp.InvalidURL:
        return 'Invalid URL'

    except aiohttp.ClientConnectionError:
        return 'Connection err'


async def fetch_worker(que):
    while True:
        url = await que.get()
        if url is None:
            await que.put(None)
            break

        result = await fetch_content(url)
        print(result)


async def batch_fetch(urls, n_workers):
    que = asyncio.Queue()

    workers = [fetch_worker(que) for _ in range(n_workers)]

    for url in urls:
        await que.put(url)
    await que.put(None)

    await asyncio.gather(*workers)


async def main(file_name, c):
    urls = get_url(file_name)

    await batch_fetch(urls, int(c))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='количество воркеров')
    parser.add_argument('-f', help='файл с URLами')

    args = parser.parse_args()
    C = args.c
    f = args.f

    if not C.isdecimal():
        raise ValueError('количество воркеров должно быть целым числом')

    asyncio.run(main(f, C))
