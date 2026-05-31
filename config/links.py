# -*- coding: utf-8 -*-
"""菜单栏外部链接数据"""


def get_menu_links():
    """返回三个分类的菜单链接:
    0: 渗透测试, 1: 应急响应, 2: 新闻资讯
    """
    pentest = {
        "渗透测试": [
            ("资产测绘", [
                ("fofa", "https://fofa.info/"),
                ("微步在线", "https://x.threatbook.com/v5/mapping"),
                ("奇安信鹰图", "https://hunter.qianxin.com/"),
                ("360quake", "https://quake.360.net/"),
                ("zoomeye", "https://www.zoomeye.org/"),
                ("censys", "https://search.censys.io/"),
                ("shodan", "https://www.shodan.io/"),
            ]),
            ("搜索引擎", [
                ("google", "https://www.google.com/"),
                ("百度", "https://www.baidu.com/"),
            ]),
            ("代码托管", [
                ("github", "https://github.com/"),
                ("gitee", "https://gitee.com/"),
            ]),
            ("站长工具", [
                ("chinaz", "https://ip.tool.chinaz.com/"),
                ("ip138", "https://www.ip138.com/"),
            ]),
            ("企业信息", [
                ("天眼查", "https://www.tianyancha.com/"),
                ("企查查", "https://www.qcc.com/"),
                ("爱企查", "https://aiqicha.baidu.com/"),
            ]),
            ("漏洞查询", [
                ("cnvd", "https://www.cnvd.org.cn/flaw/list"),
                ("知道创宇", "https://www.seebug.org/?s1=search#"),
                ("阿里云", "https://avd.aliyun.com/"),
                ("微步", "https://x.threatbook.com/v5/vulIntelligence"),
            ]),
            ("子域发现", [
                ("OneForAll", "https://github.com/shmilylty/OneForAll"),
            ]),
        ]
    }

    incident = {
        "应急响应": [
            ("威胁情报", [
                ("微步", "https://x.threatbook.com/"),
                ("深信服", "https://ti.sangfor.com.cn/analysis-platform"),
                ("绿盟", "https://ti.nsfocus.com/"),
                ("奇安信", "https://ti.qianxin.com/"),
                ("360", "https://ti.360.net/"),
            ]),
            ("云沙箱", [
                ("微步", "https://s.threatbook.com/"),
                ("virustotal", "https://www.virustotal.com/gui/home/upload"),
                ("virscan", "https://www.virscan.org/"),
                ("奇安信", "https://sandbox.ti.qianxin.com/sandbox/page"),
                ("天穹", "https://sandbox.qianxin.com/sscc-tq-web/"),
                ("360", "https://ata.360.net/"),
                ("安恒", "https://sandbox.dbappsecurity.com.cn/"),
            ]),
            ("杀毒软件", [
                ("(Win)360杀毒", "https://sd.360.cn/download_center.html"),
                ("(Win)火绒", "https://www.huorong.cn/"),
                ("(Win)天融信", "http://edr.topsec.com.cn/"),
                ("(Win)卡巴斯基", "https://www.kaspersky.com.cn/downloads"),
                ("(Linux)clamav", "https://www.clamav.net/"),
            ]),
            ("木马专杀", [
                ("D盾", "https://www.d99net.net/"),
                ("河马在线", "https://n.shellpub.com/"),
                ("河马本地", "https://www.shellpub.com/?download=1"),
            ]),
            ("综合工具", [
                ("(Win)SysinternalsSuite", "https://learn.microsoft.com/en-us/sysinternals/downloads/"),
                ("(Linux)busybox", "https://busybox.net/"),
            ]),
            ("辅助分析", [
                ("(Win)WinPrefetchView", "https://www.nirsoft.net/utils/win_prefetch_view.html"),
                ("(Win)Everything", "https://www.voidtools.com/zh-cn/downloads/"),
                ("(Win)ChromeCacheView", "http://www.nirsoft.net/utils/chrome_cache_view.html"),
                ("(Win)BrowsingHistoryView", "http://www.nirsoft.net/utils/browsing_history_view.html"),
                ("(Win)WifiHistoryView", "http://www.nirsoft.net/utils/wifi_history_view.html"),
            ]),
            ("流量分析", [
                ("wireshark", "https://www.wireshark.org/"),
                ("burp", "https://portswigger.net/burp/communitydownload"),
                ("fiddler", "https://www.telerik.com/download/fiddler"),
            ]),
            ("日志分析", [
                ("(Win)full_event_log_view", "https://www.nirsoft.net/utils/full_event_log_view.html"),
                ("(Win)Log Parser", "https://www.microsoft.com/en-us/download/details.aspx?id=24659"),
            ]),
            ("勒索解密", [
                ("腾讯管家", "https://guanjia.qq.com/pr/ls/"),
                ("360", "https://lesuobingdu.360.cn/"),
                ("奇安信", "https://lesuobingdu.qianxin.com/"),
            ]),
        ]
    }

    news = {
        "新闻资讯": [
            ("安全新闻", [
                ("freebuf", "https://www.freebuf.com/"),
                ("安全内参", "https://www.secrss.com/"),
                ("cnvd", "https://www.cnvd.org.cn/"),
                ("蚁景新闻", "https://www.yijinglab.com/news"),
            ]),
            ("国外平台", [
                ("thehackernews", "https://thehackernews.com/"),
            ]),
            ("博客社区", [
                ("个人知识库", "https://www.yuque.com/unihonest/"),
                ("freebuf", "https://www.freebuf.com/"),
                ("安全客", "https://www.anquanke.com/"),
                ("先知社区", "https://xz.aliyun.com/"),
            ]),
            ("软件镜像", [
                ("清华大学", "https://mirrors.tuna.tsinghua.edu.cn/"),
                ("中科大", "https://mirrors.ustc.edu.cn/"),
                ("阿里云", "https://developer.aliyun.com/mirror/"),
            ]),
        ]
    }

    return pentest, incident, news
