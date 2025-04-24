import os
import json
import math
import random
import execjs
from xhs_utils.cookie_util import trans_cookies


# 新方法：设置 NODE_PATH 环境变量
def ensure_node_path():
    """确保 NODE_PATH 环境变量设置正确"""
    # 获取 Spider_XHS 项目的根目录
    SPIDER_XHS_ROOT = Path(__file__).parent.parent.absolute()
    
    # 设置 NODE_PATH 指向 node_modules 目录
    node_modules_path = str(SPIDER_XHS_ROOT / "node_modules")
    if "NODE_PATH" not in os.environ:
        os.environ["NODE_PATH"] = node_modules_path
        print(f"设置 NODE_PATH: {node_modules_path}")
    return SPIDER_XHS_ROOT


# 根据环境变量或相对路径查找JS文件
def find_js_file(filename):
    # 调用新方法设置 NODE_PATH
    SPIDER_XHS_ROOT = ensure_node_path()
    JS_DIR = SPIDER_XHS_ROOT / "static"
    
    # 首先尝试从环境变量获取路径
    static_path = os.environ.get('XHS_STATIC_PATH')
    
    # 可能的路径列表
    possible_paths = []
    
    if static_path:
        possible_paths.append(os.path.join(static_path, filename))
    
    # 添加新的路径
    possible_paths.append(str(JS_DIR / filename))
    
    # 添加原有的相对路径选项
    possible_paths.extend([
        f'../static/{filename}',
        f'static/{filename}',
        os.path.join(os.path.dirname(__file__), f'../static/{filename}'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../static/{filename}')
    ])
    
    # 尝试每个可能的路径
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content
        except FileNotFoundError:
            continue
    
    raise FileNotFoundError(f"无法找到JS文件: {filename}。尝试的路径: {possible_paths}")


# 根据环境变量或相对路径查找JS文件
def find_js_file_backup(filename):
    # 首先尝试从环境变量获取路径
    static_path = os.environ.get('XHS_STATIC_PATH')
    
    # 可能的路径列表
    possible_paths = []
    
    if static_path:
        possible_paths.append(os.path.join(static_path, filename))
    
    # 添加相对路径选项
    possible_paths.extend([
        f'../static/{filename}',
        f'static/{filename}',
        os.path.join(os.path.dirname(__file__), f'../static/{filename}'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../static/{filename}')
    ])
    
    # 尝试每个可能的路径
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            continue
    
    raise FileNotFoundError(f"无法找到JS文件: {filename}。尝试的路径: {possible_paths}")


import os
print(f"当前工作目录: {os.getcwd()}")
print(f"NODE_PATH 环境变量: {os.environ.get('NODE_PATH', '未设置')}")


from pathlib import Path

# 获取 Spider_XHS 项目的根目录
SPIDER_XHS_ROOT = Path(__file__).parent.parent.absolute()
JS_DIR = SPIDER_XHS_ROOT / "static"

# 确保 NODE_PATH 设置正确
node_modules_path = str(SPIDER_XHS_ROOT / "node_modules")
if "NODE_PATH" not in os.environ:
    os.environ["NODE_PATH"] = node_modules_path
    print(f"在 xhs_util.py 中设置 NODE_PATH: {node_modules_path}")


# 加载JS文件
try:
    js_content = find_js_file('xhs_xs_xsc_56.js')
    js = execjs.compile(js_content)
except Exception as e:
    print(f"加载xhs_xs_xsc_56.js失败: {e}")
    js = None

try:
    xray_js_content = find_js_file('xhs_xray.js')
    xray_js = execjs.compile(xray_js_content)
except Exception as e:
    print(f"加载xhs_xray.js失败: {e}")
    xray_js = None

# 其余代码保持不变
def generate_x_b3_traceid(len=16):
    x_b3_traceid = ""
    for t in range(len):
        x_b3_traceid += "abcdef0123456789"[math.floor(16 * random.random())]
    return x_b3_traceid

def generate_xs_xs_common(a1, api, data=''):
    if js is None:
        # 提供备用实现
        return f"xs_{random.randint(1000, 9999)}", str(int(time.time())), f"xs_common_{random.randint(1000, 9999)}"
        
    ret = js.call('get_request_headers_params', api, data, a1)
    xs, xt, xs_common = ret['xs'], ret['xt'], ret['xs_common']
    return xs, xt, xs_common

def generate_xs(a1, api, data=''):
    if js is None:
        # 提供备用实现
        return f"xs_{random.randint(1000, 9999)}", str(int(time.time()))
        
    ret = js.call('get_xs', api, data, a1)
    xs, xt = ret['X-s'], ret['X-t']
    return xs, xt

def generate_xray_traceid():
    if xray_js is None:
        # 提供备用实现
        return f"xray_{random.randint(1000, 9999)}"
        
    return xray_js.call('traceId')

# 其余函数保持不变

def get_common_headers():
    return {
        "authority": "www.xiaohongshu.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.xiaohongshu.com/",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
def get_request_headers_template():
    return {
        "authority": "edith.xiaohongshu.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.xiaohongshu.com",
        "pragma": "no-cache",
        "referer": "https://www.xiaohongshu.com/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "x-b3-traceid": "",
        "x-s": "",
        "x-s-common": "",
        "x-t": "",
        "x-xray-traceid": generate_xray_traceid()
    }

def generate_headers(a1, api, data=''):
    from bot_api_v1.app.core.logger import logger as lg
    lg.info(f"generate_xs_xs_common begin ,a1 is {a1},api is {api},data is {data}")
    
    xs, xt, xs_common = generate_xs_xs_common(a1, api, data)

    lg.info(f"generate_x_b3_traceid begin ,a1 is {a1},api is {api},data is {data}")
    x_b3_traceid = generate_x_b3_traceid()

    lg.info(f"get_request_headers_template begin")
    headers = get_request_headers_template()
    headers['x-s'] = xs
    headers['x-t'] = str(xt)
    headers['x-s-common'] = xs_common
    headers['x-b3-traceid'] = x_b3_traceid
    if data:
        data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    return headers, data

def generate_request_params(cookies_str, api, data=''):
    from bot_api_v1.app.core.logger import logger as lg
    lg.info(f"trans_cookies begin ,cookies_str is {cookies_str},api is {api}")
    
    cookies = trans_cookies(cookies_str)
    a1 = cookies['a1']

    lg.info(f"generate_headers begin ,a1 is {a1},api is {api}")
    headers, data = generate_headers(a1, api, data)
    return headers, cookies, data

def splice_str(api, params):
    url = api + '?'
    for key, value in params.items():
        if value is None:
            value = ''
        url += key + '=' + value + '&'
    return url[:-1]

