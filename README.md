# 网页信息获取工具

这是一个使用Python编写的网页信息获取工具，可以异步获取给定URL列表中的网页信息，并将结果保存到Excel文件中。

## 功能介绍

- 支持并发获取多个URL的网页信息，提高获取效率。
- 获取的网页信息包括URL、状态码、网页标题、内容长度、服务器信息、HTTP头部和HTML内容。
- 使用异步IO和aiohttp库实现异步请求。
- 使用BeautifulSoup库解析HTML内容。

## 使用示例

1. 准备URL列表文件（urls.txt），每行包含一个URL。

```plaintext
https://www.example.com
https://www.google.com
https://www.github.com
```
  2.运行程序：

```
python batch-request.py urls.txt
```

 3.程序将会异步获取每个URL的网页信息，并将结果保存到urls.txt.xlsx文件中。

结果示例：

| URL                                                 | Status Code | Title          | Content-Length | Server                           | Headers                                         | HTML               |
| --------------------------------------------------- | ----------- | -------------- | -------------- | -------------------------------- | ----------------------------------------------- | ------------------ |
| [https://www.example.com](https://www.example.com/) | 200         | Example Domain | 1270           | N/A                              | Content-Type: text/html; charset=UTF-8 ...      | <!doctype html>... |
| [https://www.google.com](https://www.google.com/)   | 200         | Google         | 13199          | gws                              | Content-Type: text/html; charset=ISO-8859-1 ... | <!doctype html>... |
| [https://www.github.com](https://www.github.com/)   | 200         | GitHub         | 178627         | [GitHub.com](http://github.com/) | Content-Type: text/html; charset=utf-8 ...      | <!doctype html>... |

依赖库安装
使用以下命令安装所需的依赖库：

```
pip install -r requirements.txt
```

请确保已经安装了Python和pip，并在项目根目录下执行上述命令。


