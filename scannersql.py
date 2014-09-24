__author__ = 'wangss'
keyword = ['INSERT', 'COMMENT', 'ALTER']
sencondKey = ['ADD', 'MODIFY', 'INTO', 'ON']

# 待补充，校验部分，增加对sql的正确性、格式校验
def parse(string):
    for i in keyword:
        if string.strip()[0:len(i)] == i:
            if i == keyword[0]:
                insertparse(string)
            elif i == keyword[1]:
                pass
            elif i == keyword[2]:
                alterparse(string)
            else:
                pass


def insertparse(string):
    pass


def alterparse(string):
    for i in string.split():
        for sencond in sencondKey:
            if i == sencond:
                if i == sencondKey[0]:
                    alteradd(string, i)
                elif i == sencondKey[1]:
                    alteradd(string, i)
                else:
                    pass


# 增加数据库某列
def alteradd(string, key):
    tablename = string.split('TABLE')[1].split()[0]
    columnname = string.split(key)[1].split()[0]
    print 'declare vCount1 int := 0;'
    print '        vCount2 int := 0;'
    print 'begin'
    print "select count(1) into vCount1 from user_all_Tables where upper(Table_Name) = upper('" + tablename + "');"
    print 'if(vCount1 > 0 ) then'
    print "select count(1) into vCount2 from user_col_comments where upper(TABLE_NAME) = upper('" + tablename + "') and UPPER(COLUMN_NAME) = upper('" + columnname + "');"
    print 'if(vCount2 < 1 ) then'
    print "execute immediate('" + string + "');"
    print '                end if;'
    print '  end if;'
    print 'end;'


# 文档输出部分功能


def altermodify(string):
    pass


if __name__ == '__main__':

    # outputfilepath = sys.argv[4]
    # 文档处理部分待增加
    sourcefilepath = 'D:/test.log'
    sourcefile = open(sourcefilepath)
    # outputfile = open(outputfilepath)
    for i in sourcefile.readlines():  #暂时只支持单行文件，多行存在sql校验问题,校验待补充
        parse(i)
    sourcefile.close()
    # outputfile.close()