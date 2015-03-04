# -*- coding:utf-8 -*-
__author__ = 'wangss'
import os

import paramiko


class ConfContext(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def parsecontext(self):
        with open(self.filepath, 'r') as fp:
            cfcont = {}
            for d in fp:
                l = d.split('=')
                if len(l) != 2:
                    continue
                if l[0] in ['ip', 'user', 'pw']:
                    cfcont[l[0]] = l[1].strip()
                else:
                    cfcont[l[0]] = l[1].strip()[1:-1]
            return cfcont


class SftpTrans(object):
    def __init__(self, ip, user, pw):
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
            return map(lambda x: x.replace(oldpath, outpath).replace('.java', '.class'), changedfiles[1:])
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

ip = confmap['ip']
user = confmap['user']
pw = confmap['pw']

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
    temppath = ''.join(map(lambda x: '/' + x, localoutjspath.split('/'))[:-2])[1:]
    remotepath = ''.join(map(lambda x: '/' + x, j.replace(temppath, remotejspath).split('/')[
                                                :-1]))[1:]
    files[j] = remotepath

for j in SftpTrans.getoutputfile(changedjsp, localjspath, localoutjspath):
    temppath = ''.join(map(lambda x: '/' + x, localoutjspath.split('/'))[:-2])[1:]
    remotepath = ''.join(map(lambda x: '/' + x, j.replace(temppath, remotejspath).split('/')[
                                                :-1]))[1:]
    files[j] = remotepath

st = SftpTrans(ip, user, pw)
s = paramiko.Transport(ip, 22)
s.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(s)
print '修改的文件数量合计为：'.decode('utf-8') + str(len(files.keys()))
for i in files.keys():
    print i

print '是否确认全部上传服务器？Y or N \n '.decode('utf-8')
flag = raw_input()
if flag == 'Y' or flag == 'y':
    for k in files.keys():
        i = k.split('/')[-1]
        local_dir = k.replace(i, '')[:-1]
        remote_dir = files[k] + '/'
        sftp.put(os.path.join(local_dir, i), os.path.join(remote_dir, i))
    print '上传成功！'.decode('utf-8')
else:
    print '没有上传'.decode('utf-8')