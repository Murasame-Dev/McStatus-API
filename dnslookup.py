# -*- coding: utf-8 -*-
# 此模块用于解析 SRV 记录，返回值为 IP 和 解析类型(srv 或者 normal)
import dns.resolver

def dns_lookup(ip): 
    # 因为第一次解析是面向于 SRV 的，所以需要做是否带端口号的判断
    if ':' in ip:
        type = f'normal'
        return ip, type

    # 自定义 DNS 解析器
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['223.5.5.5', '223.6.6.6']  # 添加备用DNS
    resolver.timeout = 5  # 单次查询超时时间
    resolver.lifetime = 10  # 总解析时间限制
    
    try:
        print(f'正在解析 SRV 记录: _minecraft._tcp.{ip}')
        answers = resolver.resolve(f'_minecraft._tcp.{ip}', 'SRV')
        
        # address 的源输出末端有沟槽的 "."，去掉它
        address = str(answers[0].target).rstrip('.')
        port = answers[0].port
        
        # 拼接端口号,赋值 SRV
        ip = f'{address}:{port}'
        print(f'解析出 SRV 地址: {ip}')
        type = f'srv'
        return ip, type

    except dns.resolver.NoAnswer:
        print(f'无法解析SRV记录: _minecraft._tcp.{ip} (DNS服务器无答应)')
    except dns.resolver.NXDOMAIN:
        print(f'域名不存在SRV记录: _minecraft._tcp.{ip}')
    except (dns.resolver.Timeout, dns.resolver.LifetimeTimeout):
        print(f'DNS解析超时: {ip}')
    except Exception as e:
        print(f'DNS解析出现未知错误: {e}')

    type = f'normal'
    return ip, type