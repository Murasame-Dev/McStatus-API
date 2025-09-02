# 图片生成模块
from mc_status_img.get_background import download_image_with_httpx_auto_redirect
from mc_status_img.create_image import create_image
from mc_status_img.get_icon import get_icon_image

# Java版查询模块
from JavaServerStatus import java_status
# 基岩版查询模块
from BedrockServerStatus import bedrock_status
# 此API优先解析 srv 记录
from dnslookup import dns_lookup
# 格式化文本
from FormatData import format_java_data, format_bedrock_data

# 环境变量
from config import BACKGROUND_URL, DEFAULT_ICON, FONT_PATH, IMAGE_WIDTH, IMAGE_HEIGHT

import base64
import asyncio

async def get_font_url():
    if not FONT_PATH:
        font_url = None
    else:
        font_url = FONT_PATH
    return font_url

async def get_image_size():
    if not IMAGE_WIDTH or not IMAGE_HEIGHT:
        image_size = [0,0]
    else:
        image_size = [IMAGE_WIDTH, IMAGE_HEIGHT]
    return image_size

async def get_background_image():
    if BACKGROUND_URL.startswith("http://") or BACKGROUND_URL.startswith("https://"):
        background_data = await download_image_with_httpx_auto_redirect(BACKGROUND_URL)
    elif BACKGROUND_URL == "":
        background_data = None
    else:
        with open(BACKGROUND_URL, "rb") as f:
            background_data = f.read()
    return background_data


async def get_icon_image(url: str):
    if url.startswith("http"):
        icon_data = await download_image_with_httpx_auto_redirect(url)
        if icon_data:
            return icon_data
        else:
            return None
    else:
        def read_file(path):
            with open(path, "rb") as f:
                return f.read()
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, read_file, url)

async def generate_java_status_image(addr: str):
    loop = asyncio.get_event_loop()
    try:
        ip, type = await loop.run_in_executor(None, dns_lookup, addr)
        status = await loop.run_in_executor(None, java_status, ip)
        data = format_java_data(ip, type, status)
    except Exception as e:
        print(f"查询服务器时出错: {e}")
        return
    
    background_data = await download_image_with_httpx_auto_redirect(BACKGROUND_URL)
    if not background_data:
        background_data = None
        
    icon_data = await get_icon_image(DEFAULT_ICON)
            
    motd_list = data['motd'].split("\n")
    text_list = [
        f"ip: {data['ip']}",
        f"type: {data['type']}",
        f"version: {data['version']}",
        f"latency: {round(data['latency'], 2)} ms",
        f"players: {data['players']['online']}/{data['players']['max']}",
    ]

    font_url = await get_font_url()
    
    image_size = await get_image_size()
    
    if status.icon:
        image = await loop.run_in_executor(None,
                                           create_image,
                                           background_data,
                                           base64.b64decode(status.icon.split(",")[1]),
                                           text_list,
                                           motd_list,
                                           font_url,
                                           image_size)
    else:
        image = await loop.run_in_executor(None,
                                           create_image,
                                           background_data,
                                           icon_data,
                                           text_list,
                                           motd_list,
                                           font_url,
                                           image_size)                
    return image

async def generate_bedrock_status_image(addr: str):
    loop = asyncio.get_event_loop()
    try:
        ip, type = await loop.run_in_executor(None, dns_lookup, addr)
        status = await loop.run_in_executor(None, bedrock_status, ip)
        data = format_bedrock_data(ip, status)
    except Exception as e:
        print(f"查询服务器时出错: {e}")
        return
    
    background_data = await download_image_with_httpx_auto_redirect(BACKGROUND_URL)
    if not background_data:
        background_data = None
        
    icon_data = await get_icon_image(DEFAULT_ICON)
    
    motd_list = data['motd'].split("\n")
    text_list = [
        f"ip: {data['ip']}",
        f"version: {data['version']}",
        f"latency: {round(data['latency'], 2)} ms",
        f"players: {data['players']['online']}/{data['players']['max']}",
    ]

    font_url = await get_font_url()
    
    image_size = await get_image_size()

    image = await loop.run_in_executor(None,
                                       create_image,
                                       background_data,
                                       icon_data,
                                       text_list,
                                       motd_list,
                                       font_url,
                                       image_size)
    return image