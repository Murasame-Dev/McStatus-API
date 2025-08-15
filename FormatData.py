# -*- coding: utf-8 -*-
# 此模块用于格式化此项目的所有文本输出数据，包括那些鸡毛蒜皮的空值提示

# 格式化 Java 服务器状态的数据
def format_java_data(ip, type, status):
    data = {
        'ip': ip,
        'type': type,
        'latency': status.latency,
        'motd': status.motd,
        'version': status.version,
        'enforces_secure_chat': status.enforces_secure_chat,
        'forge_data': status.forge_data,
        'players': {
            'online': status.online_player,
            'max': status.max_players,
            'sample': status.sample_players
        },
        'icon': status.icon
    }
    
    return data

# 格式化基岩版服务器状态的数据
def format_bedrock_data(ip, status):
    data = {
        'ip': ip,
        'gamemode': status.gamemode,
        'map_name': status.map_name,
        'latency': status.latency,
        'motd': status.motd,
        'version': status.version,
        'players': {
            'online': status.online_player,
            'max': status.max_players
        }
    }

    return data

def format_index():
    message = {
        "message": "欢迎使用 Minecraft 服务器状态查询 API！",
        "usage": {
            "JavaStatus": "/java?ip=<IP> - (Required)",
            "BedrockStatus": "/bedrock?ip=<IP> - (Required)"
        }
    }

    return message

def format_java_index():
    message = {
        "message": "缺少 IP 参数",
        "usage": "/java?ip=<IP> - (Required)"
    }

    return message

def format_bedrock_index():
    message = {
        "message": "缺少 IP 参数",
        "usage": "/bedrock?ip=<IP> - (Required)"
    }

    return message
