# -*- coding:utf-8 -*-
__author__ = 'wangss'
import os
import sys
import time


def getchangepath(pathlist, filetype):
    i = len(pathlist)
    name = time.strftime('%Y-%m-%d-%H-%I-%M-%S', time.localtime(time.time()))
    writefile = open('D:\\' + name + '.log', 'w')
    changefileamount = 0
    for j in range(i):
        path = pathlist[j]
        _type = filetype[j]
        for parent, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(_type) and os.stat(os.path.join(parent, filename)).st_mode == 33206:
                    name = "ChangedFile---" + os.path.join(parent, filename)
                    writefile.write(name+'\n')
                    changefileamount += 1
    print '修改文件总数' + str(changefileamount)
    writefile.write('修改文件总数' + str(changefileamount)+'\n')
    writefile.close()