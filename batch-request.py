#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import sys
import requests
import xlsxwriter

from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36','Connection':'close'}

def try_get_title(url,timeout=10):
    status = 'error'
    title = ''
    banner = ''
    try:
        url = url if '://' in url else 'http://'+url
        if ':443' in url:
            url = url.replace('http://','https://').replace(':443','')
        if ':80' in url:
            url = url.replace(':80','')
        r = requests.get(url,headers=headers, timeout=timeout,verify=False)
        status = r.status_code
        r.encoding = r.apparent_encoding
        title = re.search(r'<title>(.*)</title>', r.text) #get the title
        if title:
            title = title.group(1).strip().strip("\r").strip('\n')
        banner = r.headers.get('Server','')
    except:
        pass
    return url,status,banner,title

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("{} <链接列表文件> <线程数>".format(sys.argv[0]))
    else:
        inputfile = sys.argv[1]
        outputfile = sys.argv[1] + '-result.xlsx'
        threadNUM = int(sys.argv[2])
        URLS = [i.strip() for i in  open(inputfile,'r',encoding='utf8').readlines()]
        workbook = xlsxwriter.Workbook(outputfile)
        sheet = workbook.add_worksheet() 
        sheet.activate() 
        sheet.write_row('A1',['Url','StatusCode','Banner','Title'])
        ROW = 2
        pool = ThreadPoolExecutor(max_workers=threadNUM)
        for res in pool.map(try_get_title, URLS):
            print(res)
            sheet.write_row('A{}'.format(ROW),res)
            ROW += 1
        workbook.close()
        print("save to {}".format(outputfile))

        
