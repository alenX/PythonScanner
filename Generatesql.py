# -*- coding:utf-8 -*-
__author__ = 'wangss'
import sys


def addcolumn(file_cont, result_path_cont):
    table_name_list = []
    for i in file_cont:
        if len(i.strip('\n').strip(' ').split(' ')) == 1:  # 说明是表名
            table_name_list.append(i.strip('\n'))
        else:
            cont = i.split(' ')
            table_name = table_name_list[-1].strip('\n').strip(' ')
            column_name = cont[1].strip('\n')
            column_type = cont[2].strip('\n')
            comment = cont[0].strip('\n')
            result_path_cont.writelines('declare vCount1 int := 0;\n')
            result_path_cont.writelines('vCount2 int := 0;\n')
            result_path_cont.writelines('begin\n')
            result_path_cont.writelines(
                "select count(1) into vCount1 from user_all_Tables where upper(Table_Name) = upper('" + table_name + "');\n")
            result_path_cont.writelines("if(vCount1 > 0 ) then  /*如果表存在才增加*/\n")
            result_path_cont.writelines(
                "select count(1) into vCount2 from user_col_comments where upper(TABLE_NAME) = upper('" + table_name + "') and UPPER(COLUMN_NAME) = upper('" + column_name + "');\n")
            result_path_cont.writelines("if(vCount2 < 1 ) then\n")
            result_path_cont.writelines(
                "execute immediate('alter table " + table_name + " add " + column_name + "   " + column_type + " ');\n")
            # result_path_cont.writelines("execute immediate('comment on  column " + table_name + '.' + column_name + ' is "'+comment+'"'+" ' "+');\n'+"" )
            result_path_cont.writelines(" end if;\n")
            result_path_cont.writelines(" end if;\n")
            result_path_cont.writelines(" end ;\n")
            result_path_cont.writelines('---------------------------------------------\n')
    file_cont.close()
    result_path_cont.close()


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        file_path = args[1]
        result_path = 'D:\\sql_result.sql'
    elif len(args) == 3:
        file_path = args[1]
        result_path = args[2]
    else:
        file_path = 'D:\\sql.sql'  # 文件目录
        result_path = 'D:\\sql_result.sql'
    file_cont = open(file_path, 'r')
    result_path_cont = open(result_path, 'w')
    try:
        addcolumn(file_cont, result_path_cont)
    except:
        print 'Errors'
