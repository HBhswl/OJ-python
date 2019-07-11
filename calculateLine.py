path = 'utils.py'
with open(path,'r',encoding='utf-8') as f:
    code_lines = 0       #代码行数
    comment_lines = 0    #注释行数
    blank_lines = 0      #空白行数  内容为'\n',strip()后为''
    is_comment = False
    start_comment_index = 0 #记录以'''或"""开头的注释位置
    for index,line in enumerate(f,start=1):
        line = line.strip() #去除开头和结尾的空白符

        #判断多行注释是否已经开始　
        if not is_comment:
            if line.startswith("'''") or line.startswith('"""'):
                is_comment = True
                start_comment_index = index

            #单行注释
            elif line.startswith('#'):
                comment_lines += 1
            #空白行
            elif line == '':
                blank_lines += 1
            #代码行
            else:
                code_lines += 1


        #多行注释已经开始
        else:
            if line.endswith("'''") or line.endswith('"""'):
                is_comment = False
                comment_lines += index - start_comment_index + 1
            else:
                pass

print("注释:%d" % comment_lines)
print("空行:%d" % blank_lines)
print("代码:%d" % code_lines)