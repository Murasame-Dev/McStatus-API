# -*- coding: utf-8 -*-
# 此模块用于查询基岩版版服务器状态，并将其数据赋值给类以供灵活调用单个值
from mcstatus import BedrockServer


class BedrockStatus:
    def __init__(self, gamemode, map_name, latency, motd, version, players, online_player, max_players):
        self.gamemode = gamemode
        self.map_name = map_name
        self.latency = latency
        self.motd = motd
        self.version = version
        self.players = players
        self.online_player = online_player
        self.max_players = max_players

def bedrock_status(ip):
    try:
        server = BedrockServer.lookup(ip)
        print(f'正在解析: {ip}')
        status = server.status()

        # 将 status 属性拆分成多个变量
        gamemode = status.gamemode  # 游戏模式
        map_name = status.map_name  # 地图名
        latency = status.latency # 延迟
        motd = status.description # 标题
        version = status.version.name # 版本

        # 关于玩家信息的获取
        players = status.players # 玩家总类
        online_player = players.online # 在线玩家数
        max_players = players.max # 最大玩家数

        return BedrockStatus(
            gamemode,
            map_name,
            latency,
            motd,
            version,
            players,
            online_player,
            max_players
        )

    except Exception as e:
        return print(f"获取服务器状态时出错: {e}")