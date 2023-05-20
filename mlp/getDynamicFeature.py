import os
import subprocess
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import re


class GetDynamicFeature:
    def textrank_all(self,opcodes):     #计算opcode的TextRank值
        # print(opcodes)
        list_of_opcodes_dic = {'add': 0, 'arg': 0, 'args': 0, 'array': 0, 'assert': 0, 'assign': 0, 'bind': 0, 'bool': 0, 'bw': 0, 'call': 0, 'case': 0, 'cast': 0, 'catch': 0, 'check': 0, 'class': 0, 'concat': 0, 'connect': 0, 'constant': 0, 'count': 0, 'cv': 0, 'data': 0, 'db': 0, 'dec': 0, 'declare': 0, 'defined': 0, 'dim': 0, 'div': 0, 'dynamic': 0, 'echo': 0, 'element': 0, 'equal': 0, 'eval': 0, 'exit': 0, 'ext': 0, 'fast': 0, 'fcall': 0, 'fe': 0, 'fetch': 0, 'free': 0, 'func': 0, 'function': 0, 'global': 0, 'identical': 0, 'include': 0, 'init': 0, 'isempty': 0, 'isset': 0, 'jmp': 0, 'jmpnz': 0, 'jmpz': 0, 'lambda': 0, 'list': 0, 'listen': 0, 'long': 0, 'method': 0, 'mod': 0, 'msql': 0, 'mul': 0, 'net': 0, 'nop': 0, 'num': 0, 'obj': 0, 'op': 0, 'post': 0, 'pre': 0, 'prop': 0, 'protocol': 0, 'qm': 0, 'recv': 0, 'ref': 0, 'require': 0, 'reset': 0, 'return': 0, 'rope': 0, 'rw': 0, 'send': 0, 'silence': 0, 'sl': 0, 'smaller': 0, 'socket': 0, 'sr': 0, 'static': 0, 'stmt': 0, 'string': 0, 'strlen': 0, 'switch': 0, 'type': 0, 'unset': 0, 'user': 0, 'val': 0, 'var': 0, 'xor': 0}
        tr4w = TextRank4Keyword()  #使用TextRank4zh中的TextRank4Keyword获取关键词及其权值
        tr4w.analyze(text=opcodes, lower=True, window=5)
        for item in tr4w.get_keywords(350, word_min_len=1):
                 for key in list_of_opcodes_dic:
                    if item.word == key:
                            list_of_opcodes_dic[key] = item.weight
        # print(list_of_opcodes_dic)
        TR_value=[]
        for i in list_of_opcodes_dic.values():
                    TR_value.append(i)
        return TR_value


    def getOPCode(self,fullfilepath):
        # print("开始生成{}路径中的PHP的opcode操作码文件".format(fullfilepath))
        (filename_name, extension) = os.path.splitext(fullfilepath)
        if extension=='.php':
            # print(filename_name)
            output = str(subprocess.check_output(
            ["php", "-d vld.active=1","-d vld.execute=0",fullfilepath],stderr=subprocess.STDOUT))
            tokens = re.findall(r'\s(\b[A-Z_]+\b)\s', output)  #opcode操作符提取正则
            t = " ".join(tokens)
            return t.replace('E O E ', '')  #由于opcode正则会匹配每个func开头的非opcode字符，在这里去除
            #file_content = load_php_opcode(fullpath)


