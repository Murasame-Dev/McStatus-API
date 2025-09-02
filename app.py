# -*- coding: utf-8 -*-
# 重写 Flask-MCMOTD,早期版本用的是面向过程的方式进行写的，一个文件写了400多行，真是要爆了T.T
# 2025/8/28 by Murasame:使用 *Claude Sonnet 4* 重写成了 FastAPI

# 基础模块
import asyncio
import base64
import uvicorn
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
from generate_img import get_icon_image, generate_java_status_image, generate_bedrock_status_image, get_background_image

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
        background_data = await get_background_image()
                        
        # java 服务器的方法
        if type == "java":
            image = await generate_java_status_image(ip)
        
        # bedrock 服务器的方法
        if type == "bedrock":
            image = await generate_bedrock_status_image(ip)

        img_io = BytesIO()
        image.save(img_io, 'JPEG')
        img_io.seek(0)
        return Response(content=img_io.getvalue(), media_type="image/jpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
