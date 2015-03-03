# -*- coding:utf-8 -*-
__author__ = 'wangss'

import os
import paramiko
import ftplib  # ftp


def deleteremotelogs(remotepath='', filetype='.log'):
    '遍历该路径下的所有日志文件'

    sftp = connsftp()

    for parent, dirnames, filenames in os.walk(remotepath):
        if filetype in filenames:
            sftp.remove(filenames)
        else:
            filenames + '不满足条件，没有被删除'.decode('utf-8')


def connsftp():
    s = paramiko.Transport('ip', 22)
    s.connect(username='username', password='password')
    sftp = paramiko.SFTPClient.from_transport(s)
    return sftp


print '选择要进行的操作'.decode('utf-8')
print '#####################'
print '1-清空服务器日志文件(.log)'.decode('utf-8')

print '#####################'
print '请输入操作序号'.decode('utf-8')

opertype = raw_input()
if opertype == 1 or opertype == '1':
    deleteremotelogs('/home/bea/Oracle/Middleware/user_projects/domains/base_domain/apps/ftmsln')
else:
    print '没有匹配的操作'.decode('utf-8')

