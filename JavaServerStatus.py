# -*- coding: utf-8 -*-
# 此模块用于查询 Java 版服务器状态，并将其数据赋值给类以供灵活调用单个值
from mcstatus import JavaServer

class JavaStatus:
    def __init__(self, enforces_secure_chat, forge_data, icon, latency, motd, version, players, online_player, max_players, sample_players):
        self.enforces_secure_chat = enforces_secure_chat
        self.forge_data = forge_data
        self.icon = icon
        self.latency = latency
        self.motd = motd
        self.version = version
        self.players = players
        self.online_player = online_player
        self.max_players = max_players
        self.sample_players = sample_players

def java_status(ip):
    try:
        print(f'正在解析: {ip}')
        server = JavaServer.lookup(ip)
        status = server.status()
    
        # 将 status 属性拆分成多个变量
        enforces_secure_chat = status.enforces_secure_chat # 是否开启聊天签名
        forge_data = status.forge_data # FML版本
        icon = status.icon # 图标，输出为 base64
        latency = status.latency # 延迟
        motd = status.description # 标题
        version = status.version.name # 版本

        # 关于玩家信息的获取
        players = status.players # 玩家总类
        online_player = players.online # 在线玩家数
        max_players = players.max # 最大玩家数
        sample_players = players.sample # 在线玩家的 ID,UUID

        return JavaStatus(
            enforces_secure_chat,
            forge_data,
            icon,
            latency,
            motd,
            version,
            players,
            online_player,
            max_players,
            sample_players,
        )

    except Exception as e:
        return print(f"获取服务器状态时出错: {e}")