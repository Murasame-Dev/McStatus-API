from mc_status_img.get_background import download_image_with_httpx_auto_redirect
from mc_status_img.create_image import create_image

# Java版查询模块
from JavaServerStatus import java_status
# 基岩版查询模块
from BedrockServerStatus import bedrock_status
# 此API优先解析 srv 记录
from dnslookup import dns_lookup
# 格式化文本
from FormatData import format_java_data, format_bedrock_data

import base64
import asyncio

BACKGROUND_URL = "https://www.loliapi.com/acg/"
DEFAULT_ICON = "./minecraft-creeper-face.png"

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

    if status.icon:
        image = await loop.run_in_executor(None,
                                           create_image,
                                           background_data,
                                           base64.b64decode(status.icon.split(",")[1]),
                                           text_list,
                                           motd_list)
    else:
        image = await loop.run_in_executor(None,
                                           create_image,
                                           background_data,
                                           icon_data,
                                           text_list,
                                           motd_list)
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

    image = await loop.run_in_executor(None,
                                       create_image,
                                       background_data,
                                       icon_data,
                                       text_list,
                                       motd_list)
    return image
