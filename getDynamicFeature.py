import os
import re
import subprocess
import numpy as np
from textrank4zh import TextRank4Keyword,TextRank4Sentence
import networkx

class getDynamicFeature:
    def get_opcodes(self,fullpath):
        (filename, extension) = os.path.splitext(fullpath)
        # 注意一下下面.php的类型
        if extension == ".php":
            try:
                output = subprocess.check_output(["php", "-dvld.active=1", "-dvld.execute=0", fullpath],
                                                 stderr=subprocess.STDOUT).decode("utf-8")
                # print(output)
                getopcodes = re.findall(r"\s(\b[A-Z_]+\b)\s", output)
                # 感觉不能进行去重，后面要使用textrank算法画图，大概率有影响。
                # getopcodes=np.unique(getopcodes)
                # getopcodes=getopcodes.tolist()
                # 同时，由于textrank算法传入的一般为字符串，所以这里需要处理一下
                getopcodes=" ".join(getopcodes).replace("E O E ",'')
                # 这里获取的都是未经转换过的最原始的大写的opcodes
                return getopcodes
            except:
                print("get_opcodes error!")

    # 在进行textrank算法提取特征值之前，这里我们可以尝试提取webshell中opcodes的常常出现的关键词，这里opcode组成的文本经过了textrank的分词处理后的关键词
    def get_textrankopcodes(self,opcodes,textrank_opcodes):
        tr4kw=TextRank4Keyword()
        tr4kw.analyze(text=opcodes,lower=True,window=2)
        for item in tr4kw.get_keywords(num=200,word_min_len=1):
            textrank_opcodes.append(item.word)
        return textrank_opcodes

    def get_textrankvalue(self,opcodes):
        # 前面get_textrankopcodes中提取到的webshell中存在的92个关键词，即92层特征
        textrank_opcodes_dict={'add': 0, 'arg': 0, 'args': 0, 'array': 0, 'assert': 0, 'assign': 0, 'bind': 0, 'bool': 0, 'bw': 0, 'call': 0, 'case': 0, 'cast': 0, 'catch': 0, 'check': 0, 'class': 0, 'concat': 0, 'connect': 0, 'constant': 0, 'count': 0, 'cv': 0, 'data': 0, 'db': 0, 'dec': 0, 'declare': 0, 'defined': 0, 'dim': 0, 'div': 0, 'dynamic': 0, 'echo': 0, 'element': 0, 'equal': 0, 'eval': 0, 'exit': 0, 'ext': 0, 'fast': 0, 'fcall': 0, 'fe': 0, 'fetch': 0, 'free': 0, 'func': 0, 'function': 0, 'global': 0, 'identical': 0, 'include': 0, 'init': 0, 'isempty': 0, 'isset': 0, 'jmp': 0, 'jmpnz': 0, 'jmpz': 0, 'lambda': 0, 'list': 0, 'listen': 0, 'long': 0, 'method': 0, 'mod': 0, 'msql': 0, 'mul': 0, 'net': 0, 'nop': 0, 'num': 0, 'obj': 0, 'op': 0, 'post': 0, 'pre': 0, 'prop': 0, 'protocol': 0, 'qm': 0, 'recv': 0, 'ref': 0, 'require': 0, 'reset': 0, 'return': 0, 'rope': 0, 'rw': 0, 'send': 0, 'silence': 0, 'sl': 0, 'smaller': 0, 'socket': 0, 'sr': 0, 'static': 0, 'stmt': 0, 'string': 0, 'strlen': 0, 'switch': 0, 'type': 0, 'unset': 0, 'user': 0, 'val': 0, 'var': 0, 'xor': 0}
        tr4kw=TextRank4Keyword()
        # 开启了小写转换、窗口值为2即两个单词之间的边默认值为2即共现2个单词
        tr4kw.analyze(text=opcodes,lower=True,window=2)
        # 获取最重要的num个值的最小长度为word_min_len的关键词
        for item in tr4kw.get_keywords(num=100,word_min_len=1):
            # print(item.word,item.weight)
            if item.word in textrank_opcodes_dict:
                textrank_opcodes_dict[item.word]=item.weight
        # 只传回对应的值，不需要dict
        textrank_opcodes_value=[]
        for key,value in textrank_opcodes_dict.items():
            textrank_opcodes_value.append(value)
        return textrank_opcodes_value



