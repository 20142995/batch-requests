# -*- coding: UTF-8 -*-

import csv
import sys
import re
import asyncio
import aiohttp
import datetime
from tqdm import tqdm
import async_timeout


async def fetch_webinfo(url):
    """
    异步获取单个URL的网页信息
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with async_timeout.timeout(10):
                async with session.get(url, headers=headers, ssl=False) as response:
                    status_code = response.status
                    html = await response.text()
                    headers = await response.headers
                    titles = re.findall(
                        '<title>(.*?)</title>', re.I | re.DOTALL)
                    title = titles[0] if titles else ""
                    return {'URL': url, 'Status Code': status_code, 'Title': title,
                            'Content-Length': headers.get('Content-Length', len(html) if html else 0),
                            'Server': headers.get('Server', ''), 'Headers': '\n'.join([f'{k}: {v}' for k, v in headers.items()]),
                            'HTML': html, 'Error': ''}
        except Exception as e:
            return {'URL': url, 'Status Code': 0, 'Title': '', 'Content-Length': 0, 'Server': '',
                    'Headers': '', 'HTML': '', 'Error': str(e)}


async def main(urls):
    """
    主函数，处理并发获取多个URL的网页信息
    """

    tasks = [asyncio.create_task(fetch_webinfo(url)) for url in urls]
    results = []

    with tqdm(total=len(tasks)) as pbar:
        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)
            pbar.update(1)
    return results


def save_to_csv(filename, results):
    """
    将网页信息保存到csv文件中
    """
    fieldnames = ['URL', 'Status Code', 'Title',
                  'Content-Length', 'Server', 'Headers', 'HTML', 'Error']
    with open(filename, 'w', newline='', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(f'Usage: {sys.argv[0]} urls.txt')

    urls_file = sys.argv[1]
    urls = [url.strip() for url in open(
        urls_file, 'r', encoding='utf8').readlines() if url.strip()]
    print(f'[{datetime.datetime.now()}] urls: {len(urls)}')
    print(f'[{datetime.datetime.now()}] start')
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(urls))
    print(f'[{datetime.datetime.now()}] end')
    save_to_csv(f'{urls_file}.csv', results)
    print(f'[{datetime.datetime.now()}] save to {urls_file}.csv')
