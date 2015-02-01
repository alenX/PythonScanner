# -*- coding:utf-8 -*-
__author__ = 'wangss'
import pysftp
import os


class ConfContext(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def parsecontext(self):
        with open(self.filepath, 'r') as fp:
            cfcont = {}
            for i in fp:
                l = i.split('=')
                if len(l) != 2:
                    raise IndexError
                cfcont[l[0]] = l[1].strip()[1:-1]
            return cfcont


class SftpTrans(object):
    def __int__(self, ip, user, pw):
        self.ip = ip
        self.user = user
        self.pw = pw

    @staticmethod
    def getchangefiles(filepath, filetype):  # 根据文件类型获取本地修改文件
        result = [filetype]
        for parent, dirnames, filenames in os.walk(filepath):
            for filename in filenames:
                if filename.endswith(filetype) and os.stat(os.path.join(parent, filename)).st_mode == 33206:  # 可写属性
                    name = os.path.join(parent, filename)
                    result.append(name.replace('\\', '/'))
        return result

    @staticmethod
    def getoutputfile(changedfiles, oldpath, outpath):
        if changedfiles[0] == '.java':
            return map(lambda x: x.replace(oldpath, outpath).replace('.java', '.calss'), changedfiles[1:])
        else:
            return map(lambda x: x.replace(oldpath, outpath), changedfiles[1:])


cf = ConfContext('F:/sftptrans.conf')
confmap = cf.parsecontext()

localjavapath = confmap['localjavapath']
localjspath = confmap['localjspath']
localoutjavapath = confmap['localoutjavapath']
localoutjspath = confmap['localoutjspath']
remotejavapath = confmap['remotejavapath']
remotejspath = confmap['remotejspath']

changedjava = SftpTrans.getchangefiles(localjavapath, '.java')
changedjs = SftpTrans.getchangefiles(localjspath, '.js')
changedjsp = SftpTrans.getchangefiles(localjspath, '.jsp')

files = {}
for j in SftpTrans.getoutputfile(changedjava, localjavapath, localoutjavapath):
    temppath = ''.join(map(lambda x: '/' + x, localoutjavapath.split('/'))[:-2])[1:]
    remotepath = ''.join(map(lambda x: '/' + x, j.replace(temppath, remotejavapath).split('/')[
                                                :-1]))[1:]
    files[j] = remotepath
for j in SftpTrans.getoutputfile(changedjs, localjspath, localoutjspath):
    temppath = ''.join(map(lambda x: '/' + x, localoutjavapath.split('/'))[:-2])[1:]
    remotepath = ''.join(map(lambda x: '/' + x, j.replace(temppath, remotejavapath).split('/')[
                                                :-1]))[1:]
    files[j] = remotepath
for j in SftpTrans.getoutputfile(changedjsp, localjspath, localoutjspath):
    temppath = ''.join(map(lambda x: '/' + x, localoutjavapath.split('/'))[:-2])[1:]
    remotepath = ''.join(map(lambda x: '/' + x, j.replace(temppath, remotejavapath).split('/')[
                                                :-1]))[1:]
    files[j] = remotepath

for k in files.keys():
    print k, files[k]