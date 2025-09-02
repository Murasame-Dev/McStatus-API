# -*- coding: utf-8 -*-
# 重写 Flask-MCMOTD,早期版本用的是面向过程的方式进行写的，一个文件写了400多行，真是要爆了T.T
# 2025/8/28 by Murasame:使用 *Claude Sonnet 4* 重写成了 FastAPI

# 基础模块
import asyncio
import base64
from io import BytesIO

# API
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

# Java版查询模块
from JavaServerStatus import java_status
# 基岩版查询模块
from BedrockServerStatus import bedrock_status
# 此API优先解析 srv 记录
from dnslookup import dns_lookup

# 格式化文本
from FormatData import format_java_data, format_bedrock_data, format_index, format_java_index, format_bedrock_index, format_img_index

# 图片生成模块
from mcstatus_img.get_background import download_image_with_httpx_auto_redirect
from mcstatus_img.create_image import create_image
from mcstatus_img.get_icon import get_icon_image

# 环境变量
from config import BACKGROUND_URL, DEFAULT_ICON, FONT_PATH, IMAGE_WIDTH, IMAGE_HEIGHT

app = FastAPI(
    title="McStatus API",
    description="Minecraft服务器状态查询API",
    version="3.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    message = format_index()
    return message

# Java 服务器状态查询
@app.get("/java")
async def get_java_status(ip: str = Query(None, description="服务器IP地址或域名")):
    # 空值输出 API 用法
    if not ip:
        message = format_java_index()
        raise HTTPException(status_code=400, detail=message)

    try:
        ip, type = dns_lookup(ip)
        print(f"解析Java版IP: {ip}, 是否为 SRV: {type}")
        status = java_status(ip)

        data = format_java_data(ip, type, status)

        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 基岩版服务器状态查询
@app.get("/bedrock")
async def get_bedrock_status(ip: str = Query(None, description="服务器IP地址或域名")):
    # 空值输出 API 用法
    if not ip:
        message = format_bedrock_index()
        raise HTTPException(status_code=400, detail=message)
    
    try:
        print(f"解析基岩版IP: {ip}")
        status = bedrock_status(ip)

        data = format_bedrock_data(ip, status)

        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 生成服务器状态图片
@app.get("/img")
async def get_status_image(ip: str = Query(None, description="服务器IP地址或域名"), type: str = Query(None, description="服务器版本，java 或 bedrock")):
    # 空值输出 API 用法
    if not ip or not type or type not in ["java", "bedrock"]:
        message = format_img_index()
        raise HTTPException(status_code=400, detail=message)
    
    try:        
        # 背景图获取方法
        if BACKGROUND_URL.startswith("http://") or BACKGROUND_URL.startswith("https://"):
            background_data = await download_image_with_httpx_auto_redirect(BACKGROUND_URL)
        elif BACKGROUND_URL == "none":
            background_data = None
        else:
            with open(BACKGROUND_URL, "rb") as f:
                background_data = f.read()
        
        # 字体设置方法
        if not FONT_PATH:
            font_url = None
        else:
            font_url = FONT_PATH
        
        loop = asyncio.get_event_loop()
                
        # java 服务器的方法
        if type == "java":
            ip, type = await loop.run_in_executor(None, dns_lookup, ip)
            status = await loop.run_in_executor(None, java_status, ip)
            data = format_java_data(ip, type, status)
            # JAVA服务器字典
            text_list = [
                f"ip: {data['ip']}",
                f"type: {data['type']}",
                f"version: {data['version']}",
                f"latency: {round(data['latency'], 2)} ms",
                f"players: {data['players']['online']}/{data['players']['max']}",
            ]
        
        # bedrock 服务器的方法
        if type == "bedrock":
            status = await loop.run_in_executor(None, bedrock_status, ip)
            data = format_bedrock_data(ip, status)
            data['type'] = 'normal'
            status.icon = None
            # BE服务器字典
            text_list = [
                f"ip: {data['ip']}",
                f"version: {data['version']}",
                f"latency: {round(data['latency'], 2)} ms",
                f"players: {data['players']['online']}/{data['players']['max']}",
            ]
            
        # MOTD信息        
        motd_list = data['motd'].split("\n")
        
        # 图标获取方法
        if status.icon:
            icon_data = base64.b64decode(status.icon.split(",")[1])
        else:
            icon_data = await get_icon_image(DEFAULT_ICON)
        
        # 图片尺寸
        if not IMAGE_WIDTH or not IMAGE_HEIGHT:
            image_size = [0,0]
        else:
            image_size = [IMAGE_WIDTH, IMAGE_HEIGHT]
        
        image = await loop.run_in_executor(None,
                                            create_image,
                                            background_data,
                                            icon_data,
                                            text_list,
                                            motd_list,
                                            font_url,
                                            image_size)
        img_io = BytesIO()
        image.save(img_io, 'JPEG')
        img_io.seek(0)
        return Response(content=img_io.getvalue(), media_type="image/jpeg")

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)