#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

# 定义菜单及其子项
def get_manu_link():
    menus_and_actions_xxsj = {
        '安全链接': [
            ('资产测绘', [
                ('fofa', 'https://fofa.info/'),
                ('微步在线', 'https://x.threatbook.com/v5/mapping'),
                ('奇安信鹰图', 'https://hunter.qianxin.com/'),
                ('360quake', 'https://quake.360.net/'),
                ('zoomeye', 'https://www.zoomeye.org/'),
                ('daydaymap','https://www.daydaymap.com/')
            ]),
            ('搜索引擎', [
                ('google', 'https://www.google.com/'),
                ('shodan', 'https://www.shodan.io/'),
                ('百度', 'https://www.baidu.com/')
            ]),
            ('代码托管', [
                ('github', 'https://github.com/'),
                ('gitee', 'https://gitee.com/')
            ]),
            ('站长工具', [
                ('chinaz', 'https://ip.tool.chinaz.com/'),
                ('ip138', 'https://www.ip138.com/'),
                ('备案', 'https://beian.miit.gov.cn/#/Integrated/index')
            ]),
            ('企业信息', [
                ('零零信安', 'https://0.zone/'),
                ('天眼查', 'https://www.tianyancha.com/'),
                ('企查查', 'https://www.qcc.com/'),
                ('爱企查', 'https://aiqicha.baidu.com/'),
                ('小蓝本', 'https://sou.xiaolanben.com/pc')
            ]),
            ('漏洞查询', [
                ('cnvd', 'https://www.cnvd.org.cn/flaw/list'),
                ('知道创宇', 'https://www.seebug.org/?s1=search#'),
                ('阿里云', 'https://avd.aliyun.com/'),
                ('长亭', 'https://stack.chaitin.com/vuldb/index'),
                ('微步', 'https://x.threatbook.com/v5/vulIntelligence'),
                ('火绒', 'https://www.huorong.cn/document/tech/new-all')
            ]),
            ('威胁情报', [
                ('微步', 'https://x.threatbook.com/'),
                ('深信服', 'https://ti.sangfor.com.cn/analysis-platform'),
                ('绿盟', 'https://ti.nsfocus.com/'),
                ('奇安信', 'https://ti.qianxin.com/'),
                ('360', 'https://ti.360.net/'),
                ('安恒', 'https://ti.dbappsecurity.com.cn/')
            ]),
            ('云沙箱', [
                ('微步', 'https://s.threatbook.com/'),
                ('virustotal', 'https://www.virustotal.com/gui/home/upload'),
                ('virscan', 'https://www.virscan.org/'),
                ('奇安信', 'https://sandbox.ti.qianxin.com/sandbox/page'),
                ('天穹', 'https://sandbox.qianxin.com/sscc-tq-web/'),
                ('360', 'https://ata.360.net/'),
                ('安恒', 'https://sandbox.dbappsecurity.com.cn/'),
                ('哈勃', 'https://habo.qq.com/')
            ]),
            # ('安全新闻', [
            #     ('freebuf', 'https://www.freebuf.com/'),
            #     ('安全内参', 'https://www.secrss.com/'),
            #     ('cnvd', 'https://www.cnvd.org.cn/'),
            #     ('蚁景新闻', 'https://www.yijinglab.com/news'),
            #     ('thehackernews', 'https://thehackernews.com/')
            # ]),
            ('博客社区', [
                ('个人知识库', 'https://www.yuque.com/unihonest/netsecdef'),
                ('知道创宇', 'https://paper.seebug.org/'),
                ('freebuf', 'https://www.freebuf.com/'),
                ('安全客', 'https://www.anquanke.com/'),
                ('先知社区', 'https://xz.aliyun.com/'),
                ('漏见网安', 'https://wechat.doonsec.com/'),
                ('cn-sec', 'https://cn-sec.com/'),
                ('sec-wiki', 'https://www.sec-wiki.com/'),
                ('安全牛', 'https://www.aqniu.com/'),
                ('补天社区', 'https://forum.butian.net/'),
                ('土司', 'https://www.t00ls.com/')
            ]),
            ('综合网站', [
                ('棱角社区', 'https://forum.ywhack.com/index.php'),
                ('one-fox', 'https://tool.one-fox.cn/'),
                ('tidesec', 'http://bypass.tidesec.com/order/')
            ])
        ]
    }
    
    return menus_and_actions_xxsj