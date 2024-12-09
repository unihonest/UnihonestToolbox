#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

# 定义菜单及其子项
def get_manu_link():
    menus_and_actions_link = {
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
            # ('杀毒软件', [
            #     ('(Win)360杀毒', 'https://sd.360.cn/download_center.html'),
            #     ('(Win)火绒', 'https://www.huorong.cn/'),
            #     ('(Win)天融信', 'http://edr.topsec.com.cn/'),
            #     ('(Win)卡巴斯基', 'https://www.kaspersky.com.cn/downloads'),
            #     ('火绒', ''),
            #     ('火绒', ''),
            #     ('火绒', ''),
            #     ('腾讯管家', '')
            # ]),
            # ('应急响应', [
            #     ('(Win)Everything', 'https://www.voidtools.com/zh-cn/downloads/'),
            #     ('(Win)SysinternalsSuite', 'https://learn.microsoft.com/en-us/sysinternals/downloads/'),
            #     ('(Win)', ''),
            #     ('(Win)', ''),
            #     ('(linux)busybox', 'https://busybox.net/'),
            #     ('火绒', ''),
            #     ('火绒', ''),
            #     ('腾讯管家', '')
            # ]),
            ('勒索解密', [
                ('360', 'https://lesuobingdu.360.cn/'),
                ('奇安信', 'https://lesuobingdu.qianxin.com/'),
                ('腾讯管家', 'https://guanjia.qq.com/pr/ls/')
            ]),
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
            ]),
            ('开源镜像', [
                ('清华大学', 'https://mirrors.tuna.tsinghua.edu.cn/'),
                ('中科大', 'https://mirrors.ustc.edu.cn/')
            ])
        ]
    }
    
    return menus_and_actions_link