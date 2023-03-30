import joblib
import sys
import os
import time
from trainModel import *
import os
from Logger import *

filelist= {}
pre_feature_value = []
checked_filename=[]
trainmodel = trainModel()

# 检测相关的一些路径,PS：训练模型的一些路径需要到trainModel.py中修改
# 模型加载路径
loadmodel_name=r"C:\Users\Lenovo\Desktop\python3Project\school\works\scout\traindata\rfc.pkl"
# 需要进行检测的文件目录
filecheck_name=r"C:\Users\Lenovo\Desktop\python3Project\school\works\scout\check"
# filecheck_name=r"C:\Users\Lenovo\Desktop\python3Project\school\works\scout\webshell-test-samples"

def run_check():
    # 获取需要检测的文件夹的所有文件
    fileread(filecheck_name)
    # 提取特征值哦
    get_feature()
    # print(pre_feature_value)
    # 检测启动
    check()

def check():
    # 加载模型
    rfc=joblib.load(loadmodel_name)
    # print(rfc)
    # 模型预测
    predict_result=rfc.predict(pre_feature_value)
    print(predict_result)
    # print(checked_filename)
    for i in range(len(checked_filename)):
        if predict_result[i] == 0:
            print(checked_filename[i]+" is normal")
        elif predict_result[i] == 1:
            print(checked_filename[i]+ " is webshell")
    print(len(checked_filename))




def get_feature():
    global pre_feature_value
    for filename, fullpath in filelist.items():
        # 觉得还是做一个文件后缀检测提高效率比较好
        (_, extension) = os.path.splitext(fullpath)
        if extension == ".php":
            try:

                # 获取静态统计特征
                entropy, ic, evilfunctions = trainmodel.run_getStaticFeature(fullpath)
                # 获取动态opcode特征
                textrank_value = trainmodel.run_getDynamicFeature(fullpath)
                # 整合汇总后加入到预处理训练集合中

                temp_value = []
                # 92个opcode动态特征值
                for tv in textrank_value:
                    temp_value.append(tv)
                # 6个静态统计特征值
                temp_value.append(entropy)
                temp_value.append(ic)
                for ef in evilfunctions:
                    temp_value.append(ef)
                pre_feature_value.append(temp_value)
                # 顺便存个文件名
                checked_filename.append(fullpath)
            except:
                print(filename + " error!")
                continue
        else:
            continue

def fileread(filepath):
    global filelist
    for root, dirs, files in os.walk(filepath):
        # print(root,dirs,files)
        for filename in files:
            filepath = os.path.join(root, filename)
            filelist[filename] = filepath
        # print(filelist)

def log():
    # 自定义目录存放日志文件
    log_path = './Logs/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    # 日志文件名按照程序运行时间设置
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)
    # 记录 traceback 异常信息
    sys.stderr = Logger(log_file_name)


if __name__ == "__main__":
    # 开启日志功能
    log()

    # 1、训练模块
    # 要训练模型的时候把注释去掉,同时下面的php-webshell检测可以注释掉
    # trainmodel.run_trainModel()

    #2、检测模块
    # 开炮
    run_check()


