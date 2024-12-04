# Python 3.12.7
__version__ = "1.0.0"
__author__ = "unihonest"

import dns.resolver
import os
from datetime import datetime

def get_dns_records(domain, dns_servers):
    records = {}
    # 创建一个自定义解析器
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = dns_servers

    # 获取 A 记录
    try:
        a_records = my_resolver.resolve(domain, 'A')
        records['A'] = [rdata.to_text() for rdata in a_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['A'] = []
    except Exception as e:
        records['A'] = []
        print(f"Error getting A records for {domain}: {e}")

    # 获取 MX 记录
    try:
        mx_records = my_resolver.resolve(domain, 'MX')
        records['MX'] = [(rdata.exchange.to_text(), rdata.preference) for rdata in mx_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['MX'] = []
    except Exception as e:
        records['MX'] = []
        print(f"Error getting MX records for {domain}: {e}")

    # 获取 CNAME 记录
    try:
        cname_records = my_resolver.resolve(domain, 'CNAME')
        records['CNAME'] = [rdata.to_text() for rdata in cname_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['CNAME'] = []
    except Exception as e:
        records['CNAME'] = []
        print(f"Error getting CNAME records for {domain}: {e}")

    # 获取 AAAA 记录
    try:
        aaaa_records = my_resolver.resolve(domain, 'AAAA')
        records['AAAA'] = [rdata.to_text() for rdata in aaaa_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['AAAA'] = []
    except Exception as e:
        records['AAAA'] = []
        print(f"Error getting AAAA records for {domain}: {e}")

    # 获取 NS 记录
    try:
        ns_records = my_resolver.resolve(domain, 'NS')
        records['NS'] = [rdata.to_text() for rdata in ns_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['NS'] = []
    except Exception as e:
        records['NS'] = []
        print(f"Error getting NS records for {domain}: {e}")

    # 获取 TXT 记录
    try:
        txt_records = my_resolver.resolve(domain, 'TXT')
        records['TXT'] = [rdata.to_text() for rdata in txt_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['TXT'] = []
    except Exception as e:
        records['TXT'] = []
        print(f"Error getting TXT records for {domain}: {e}")

    return records


def dnstypeGet(unihonestdnstypedomain,unihonestdnstypeserver):
    # 示例用法
    domain = unihonestdnstypedomain
    dns_servers = [unihonestdnstypeserver]  # 使用 Google 的 DNS 服务器
    dns_records = get_dns_records(domain, dns_servers)

    # 定义一个空列表来存储结果
    result = []  
    
    # 打印DNS记录的标题
    print_title = f"DNS Records for \"{domain}\" :\n"
    result.append(print_title)  # 将标题添加到结果列表中，但实际上此时并不打印
    
    # 遍历dns_records字典
    for record_type, record_list in dns_records.items():
        # 构建记录类型的字符串
        record_type_str = f"{record_type.upper()} Records:"
        result.append(record_type_str)  # 将记录类型的字符串添加到结果列表中
        
        # 遍历该记录类型下的所有记录
        for record in record_list:

            record_str = f" {record}"
            result.append(record_str)  # 将记录字符串添加到结果列表中
        
        result.append("")  
    

    # 获取当前文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__)) 

    # 设置日志文件夹名称
    nmap_folder = "dnstypelog"

    # 设置日志文件夹的路径 
    nmap_path = os.path.join(script_dir, nmap_folder) 

    # 确保日志文件夹创建
    os.makedirs(nmap_path, exist_ok=True)

    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

    # 设置日志文件名称
    log_file_name = f"dnstype_{current_time}.log"

    # 设置日志的路径
    log_file_path = os.path.join(nmap_path, log_file_name)

    # 保存成日志文件
    with open(log_file_path, mode='w', encoding='utf-8') as file:
        # 将结果列表中的所有字符串以换行符连接并写入文件
        file.write("\n".join(result))

    # 返回日志路径信息
    return (f"Logpath: {log_file_path}")