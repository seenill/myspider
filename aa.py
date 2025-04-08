import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.bestblogs.dev',
    'Referer': 'https://www.bestblogs.dev/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'User-Id': 'VU_1ae5fc',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'keyword': '',
    'qualifiedFilter': '',
    'sourceId': '',
    'collectionId': '',
    'category': 'programming',  # 仅保留分类名称
    'timeFilter': '1w',         # 时间范围（1周内）
    'language': 'all',          # 语言类型
    'userLanguage': 'zh',       # 用户语言
    'sortType': 'time_desc',    # 关键参数：按时间降序排序
    'currentPage': 1,
    'pageSize': 10,
}

response = requests.post('https://api.bestblogs.dev/api/resource/list', headers=headers, json=json_data)

# 将响应内容写入文件
try:
    with open('response_data.json', 'w', encoding='utf-8') as file:
        import json
        json.dump(response.json(), file, ensure_ascii=False, indent=4)
    print("响应内容已成功写入到 response_data.json 文件中。")
except Exception as e:
    print(f"写入文件时出现错误: {e}")