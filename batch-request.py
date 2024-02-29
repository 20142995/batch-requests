#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import xlsxwriter


async def fetch_webinfo(session, url):
    """
    异步获取单个URL的网页信息
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        async with session.get(url, headers=headers, ssl=False) as response:
            status_code = response.status
            html = await response.text()
            headers = response.headers
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title else ''
            print(url,title)
            return {'url': url, 'status_code': status_code, 'title': title,
                    'Content-Length': headers.get('Content-Length',len(html) if html else 0),
                    'Server': headers.get('Server', ''), 'headers': '\n'.join([f'{k}: {v}' for k, v in headers.items()]),
                    'html': html, 'error': ''}
    except aiohttp.ClientError as e:
        print(url,e)
        return {'url': url, 'status_code': 0, 'title': '', 'Content-Length': 0, 'Server': '',
                'headers': '', 'html': '', 'error': str(e)}


async def main(urls):
    """
    主函数，处理并发获取多个URL的网页信息
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch_webinfo(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        results = {url: response for url, response in zip(urls, responses)}
        return results


def save_to_xlsx(filename, results):
    """
    将网页信息保存到Excel文件中
    """
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("Webpage Info")
    worksheet.write_row(0, 0, ['URL', 'Status Code', 'Title', 'Content-Length', 'Server', 'Headers', 'HTML', 'Error'])
    row = 1
    for url, response in results.items():
        worksheet.write_row(row, 0, [
            response['url'], response['status_code'], response['title'], response['Content-Length'],
            response['Server'], response['headers'], response['html'], response['error']
        ])
        row += 1
    workbook.close()



if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(f'Usage: {sys.argv[0]} urls.txt')

    urls_file = sys.argv[1]
    urls = [url.strip() for url in open(urls_file, 'r', encoding='utf8').readlines()]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(urls))
    save_to_xlsx(f'{urls_file}.xlsx', results)


        
