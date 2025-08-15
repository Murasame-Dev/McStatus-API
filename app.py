# -*- coding: utf-8 -*-
# 重写 Flask-MCMOTD,早期版本用的是面向过程的方式进行写的，一个文件写了400多行，真是要爆了T.T

# API
from flask import Flask, request, jsonify
from flask_cors import CORS

# Java版查询模块
from JavaServerStatus import java_status
# 基岩版查询模块
from BedrockServerStatus import bedrock_status
# 此API优先解析 srv 记录
from dnslookup import dns_lookup

# 格式化文本
from FormatData import format_java_data, format_bedrock_data, format_index, format_java_index, format_bedrock_index


app = Flask(__name__)
app.json.sort_keys = False
app.json.ensure_ascii = False
app.json.mimetype = 'application/json;charset=UTF-8'
app.json.compact = False
CORS(app)

@app.route('/')
def index():
    message = format_index()
    return jsonify(message), 200

# Java 服务器状态查询
@app.route('/java')
def get_java_status():
    ip = request.args.get('ip')
    # 空值输出 API 用法
    if not ip:
        message = format_java_index()
        return jsonify(message), 400

    try:
        ip, type = dns_lookup(ip)
        print(f"解析Java版IP: {ip}, 是否为 SRV: {type}")
        status = java_status(ip)

        data = format_java_data(ip, type, status)

        return jsonify(data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 基岩版服务器状态查询
@app.route('/bedrock')
def get_bedrock_status():
    ip = request.args.get('ip')
    # 空值输出 API 用法
    if not ip:
        message = format_bedrock_index()
        return jsonify(message), 400
    
    try:
        print(f"解析基岩版IP: {ip}")
        status = bedrock_status(ip)

        data = format_bedrock_data(ip, status)

        return jsonify(data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)