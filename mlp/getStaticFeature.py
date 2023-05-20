import string
import math
import nltk
import re
# nltk.download('punkt')


class GetStaticFeature:
    def getIC(self,filePath): #计算重合指数
        with open(filePath,'r') as f:
            data=f.read()
            data=data.lower()  #需不需要转小写??
            # print(data)
            letter = "abcdefghijklmnopqrstuvwxyz"
            letter_dic={}
            for c in letter:
                letter_dic[c]=0
            N=0
            for c in data:
                if c in letter:
                    N+=1
                    letter_dic[c]+=1
            # print(letter_dic)
            # print(N)
            sum=0
            for c in letter:
                n_c=letter_dic[c]
                sum+=n_c*(n_c-1)
            # print(sum)
            # print(N*(N-1))
            IC=(sum/(N*(N-1)))
            return IC

    def getKeywords(self,filepath): #统计特征函数
        ##四种类型的函数
        RCE = ['assert', 'eval', 'python_eval', 'shell', 'array_map', 'call_user_func', 'system', 'preg_replace',
                    'passthru', 'shell_exec', 'exec', 'proc_open', 'popen', 'curl_exec', 'curl_multi_exec',
                    'parse_ini_file', 'show_source','create_function','ob_start']
        FR = ['file_get_contents', 'is_file', 'fopen', 'fclose', 'fwrite', 'wget', 'lynx', 'curl',
                    'posix_getpwuid', 'posix_getgrgid', 'fileowner', 'filegroup']
        mysql = ['mysql_connect', 'mysql_query', 'mysql_num_fields', 'mysql_close', 'mysql_fetch_array',
                    'mysql_fetch_assoc', 'mysql_num_rows', 'mysql_result', 'mysql_affected_rows', 'mysql_select_db',
                    'mssql_connect', 'mssql _query', 'mssql_num_fields', 'mssql_field_name', 'mssql_fetch_array',
                    'mysql_close']
        cyber = ['gzdeflat', 'gzcompress', 'gzuncompress', 'gzdecode', 'str_rot13', 'gzencode', 'base64_decode',
                    'base64_encode']
        data=open(filepath, 'r').read()
        dataAfterRE = re.sub('[^\w ]', ' ', data)
        # print(nltk.word_tokenize(dataAfterRE))
        words=nltk.word_tokenize(dataAfterRE)
        # print(jieba.lcut(dataAfterRE))
        num1=num2=num3=num4=0
        for word in words:
            if len(word) <2: continue
            if word in RCE:
                num1+=1
                continue
            if word in FR:
                num2+=1
                continue
            if word in mysql:
                num3+=1
                continue
            if word in cyber:
                num4+=1
                continue
        return(num1,num2,num3,num4)



    def getEntropy(self,filepath):     #计算信息熵
        contents=open(filepath,'r').read()
        dataAfterRE = re.sub('[^\w ]', ' ', contents)
        dataAfterRE=dataAfterRE.replace(' ','')
        # print(dataAfterRE)
        charList=string.ascii_letters+string.digits+'_' #信息熵的分类
        # print(charList)
        entropy=0.0
        for char in charList:
            p_x=float(dataAfterRE.count(char)/len(dataAfterRE))
            if p_x>0:
                entropy+=-(p_x*math.log(p_x,2))
        return entropy


# getStaticFeature1 = getStaticFeature()
# a = ()
# a = getStaticFeature1.evil_functions("D:\\desktop\\PKI大作业\\scout-main\\check\\1.php")