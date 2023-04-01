import os.path
import pickle
import re
import subprocess
import time
import joblib
from getStaticFeature import *
from getDynamicFeature import *
from pre_pickle import feature_lable
from sklearn.ensemble import RandomForestClassifier

allrealopcodes = []
filelist = {}
begin_time = time.time()
# 预训练数据
pre_feature_value=[]
label=[]
black_number=0
white_numer=0

# 训练数据所在目录，需要分为两个目录black-traindata和white-traindata
fileread_name=r"C:\Users\Lenovo\Desktop\python3Project\school\works\scout\traindata"
# 特征值提取后，需要使用pickle序列化保存成文件，以供后续读取训练，这是保存路径
prefeature_pickleload_name=r"C:\Users\Lenovo\Desktop\python3Project\school\works\scout\traindata\pre_feature.pkl"
# 模型生成保存的路径
createmodel_name=r'C:\Users\Lenovo\Desktop\python3Project\school\works\scout\traindata\rfc.pkl'

class trainModel:
    def run_trainModel(self):
        # 获取文件夹的所有文件
        self.fileread(fileread_name)

        # 统计一下一个目录下所有的php文件数量，需要先进行fileread
        # phpnumbers=self.get_phpnumbers()

        # 1、获取所有的特征值和标签，并序列化写入文件存储
        self.get_all_predata()

        # 2、然后直接pickle.load拿提取的预训练数据集直接fit就好了,这就是sklearn的事了
        self.create_model()

    def create_model(self):
        # 反序列化读取数据
        fileopen=open(prefeature_pickleload_name,"rb")
        pickle_loaddata=pickle.load(fileopen)
        # print(pickle_loaddata.feature_value)
        # print(pickle_loaddata.label_value)
        fileopen.close()
        # 开始训练,参数设置是一个玄学
        rfc=RandomForestClassifier(bootstrap=True,n_estimators=100,criterion="gini",min_samples_split=2,max_depth=None,min_samples_leaf=1,random_state=0)
        rfc.fit(pickle_loaddata.feature_value,pickle_loaddata.label_value)
        # rfc模型保存
        joblib.dump(rfc,createmodel_name)

    def get_all_predata(self):
        global pre_feature_value,label,black_number,white_numer
        for filename, fullpath in filelist.items():
            # 觉得还是做一个文件后缀检测提高效率比较好
            (_, extension) = os.path.splitext(fullpath)
            print(fullpath)
            if extension == ".php":
                # 防止一些编码错误导致程序不正常运行
                try:
                    # 对所有php文件提取opcode并存入txt文件计数
                    # catchallopcode()

                    # 提取静态特征，统计学特征检测：信息熵、重合指数、功能函数
                    entropy,ic,evilfunctions=self.run_getStaticFeature(fullpath)

                    # 提取动态特征，利用textrank方法训练提取opcode
                    textrank_value=self.run_getDynamicFeature(fullpath)

                    temp_value=[]
                    # 92个opcode动态特征值
                    for tv in textrank_value:
                        temp_value.append(tv)
                    # 6个静态统计特征值
                    temp_value.append(entropy)
                    temp_value.append(ic)
                    for ef in evilfunctions:
                        temp_value.append(ef)
                    # 汇总后加入到预处理训练集合中
                    pre_feature_value.append(temp_value)

                    # 把特征值写入后，还需要写入对应的标签，表示该特征值是webshell还是普通文本
                    if "black-traindata" in fullpath:
                        label.append(1)
                        black_number+=1
                    elif "white-traindata" in fullpath:
                        label.append(0)
                        white_numer+=1
                except:
                    print(filename+" error!")
                    continue

        # 提取完所有的特征值和标签后使用pickle序列化写入文件中
        self.pikle_dump()

    # 提取完所有的特征值和标签后使用pickle序列化写入文件中
    def pikle_dump(self):
        print(pre_feature_value)
        # print(len(pre_feature_value))
        print(label)
        print(len(label))
        print("black: "+str(black_number)+" ,white: "+str(white_numer))
        pickle_class=feature_lable(pre_feature_value,label)
        fileopen=open(prefeature_pickleload_name,"wb")
        pickle.dump(pickle_class,fileopen)
        fileopen.close()


    def catchallopcode(self):
        global allrealopcodes, begin_time
        for key, fullpath in filelist.items():
            (filename, extension) = os.path.splitext(fullpath)
            # print(filename,extension)
            # 注意一下下面.php的类型
            if extension == ".php":
                # print(filename)
                output = subprocess.check_output(["php", "-dvld.active=1", "-dvld.execute=0", fullpath],
                                                 stderr=subprocess.STDOUT).decode("gbk")
                # print(output)
                getallopcode = re.findall(r"\s(\b[A-Z_]+\b)\s", output)
                # print(getallopcode)
                # print(len(getallopcode))
                # stropcode=" ".join(getallopcode).replace("E O E ","")
                # print(stropcode)
                for opcode in getallopcode:
                    if opcode not in allrealopcodes:
                        allrealopcodes.append(opcode)
        allcodesset = set(allrealopcodes)
        allcodesset.remove("E")
        allcodesset.remove("O")
        # allrealopcodes=np.unique(allrealopcodes)
        # allrealopcodes.remove('E')
        # allrealopcodes.remove('O')
        # print(allrealopcodes)
        # print(len(allrealopcodes))
        print(allcodesset)
        allopcodesdict = dict.fromkeys(allcodesset, 0)
        # 将所有opcode写入文件中
        with open("../test-train.txt", "w") as opcodes:
            # with open("webshell-allrealopcodes.txt", "w") as opcodes:
            # with open("wordpress-allrealopcodes.txt", "w") as opcodes:
            #     opcodes.write(str(allrealopcodes) + "\n")
            opcodes.write(str(allopcodesdict) + "\n")
            opcodes.write(str(len(allrealopcodes)) + "\n")
            end_time = time.time()
            # print("运行时间：" + str(end_time - begin_time))
            opcodes.write(str(end_time - begin_time) + "\n")
        opcodes.close()

    def fileread(self,filepath):
        global filelist
        for root, dirs, files in os.walk(filepath):
            # print(root,dirs,files)
            for filename in files:
                filepath = os.path.join(root, filename)
                filelist[filename] = filepath
            # print(filelist)

    def run_getStaticFeature(self,fullpath):
        staticfeature = getStaticFeature()
        entropy,ic,evilfunctions=0,0,()
        # 尝试打开文件获取内容
        try:
            openfile = open(fullpath, "r", encoding="utf-8")
            content = openfile.read()
            # print(content)
            openfile.close()
            # 获取信息熵
            entropy = staticfeature.information_entropy(content)
            # print(entropy)
            # 获取重合指数
            ic = staticfeature.coincidence_index(content)
            # print(ic)
            # 获取恶意特征函数次数
            evilfunctions = staticfeature.evil_functions(content)
            # print(evilfunctions)
            return entropy, ic, evilfunctions
        except:
            print("run_getStaticFeature error!")

    def run_getDynamicFeature(self,fullpath):
        dynamicfeature = getDynamicFeature()
        opcodes = dynamicfeature.get_opcodes(fullpath)
        # print(opcodes)
        # 这里是准备工作，使用textrank算法尝试提取出webshell会存在的所有关键词，进行了分词+小写的处理(92个，后续可能会更改)
        # textrank_opcodes = dynamicfeature.get_textrankopcodes(opcodes, textrank_opcodes)
        textrank_value=dynamicfeature.get_textrankvalue(opcodes)
        # print(textrank_value)
        return textrank_value

        # # 这里是把textrank算法提取的所有关键词进行txt文件保存，提前处理工作，不需要关注
        # textrank_opcodes_set = set(textrank_opcodes)
        # textrank_opcodes_dict = dict.fromkeys(textrank_opcodes_set, 0)
        # # with open("textrank_opcodes_test.txt","w") as files:
        # # with open("textrank_opcodes_webshells.txt","w") as files:
        # # with open("textrank_opcodes_normal.txt","w") as files:
        # with open("../textrank_opcodes_webshelltestsamples.txt", "w") as files:
        #     files.write(str(textrank_opcodes_dict) + "\n")
        #     files.write(str(len(textrank_opcodes_dict)) + "\n")
        # files.close()

    def get_phpnumbers(self):
        phpnumber=0
        for key, fullpath in filelist.items():
            (filename, extension) = os.path.splitext(fullpath)
            if extension==".php":
                phpnumber+=1
        print(phpnumber)
        return phpnumber


