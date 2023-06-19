# WebshellScout

一个基于随机森林（1+1+4+92种特征）进行机器学习的php-webshell检测项目，后续可能添加神经网络进行训练，UI制作主要基于Python内置库tkinter，持续完善优化中~

学习过程：https://www.yuque.com/sakura501/school/wc5qr9qeq7mdhfls

飞书文档：https://kjd3xtsq9r.feishu.cn/docx/I1D9dwEyQoD876x4lx9c8aHanyg

发现了一个好东西，阿里云的学习赛：https://tianchi.aliyun.com/competition/entrance/532068/introduction

## 目录&文件说明

Logs：存放控制台输出的日志记录，具体结构在Logger.py中

traindata：包括有black-traindata和white-traindata两个目录存放webshell训练集和normal训练集

testdata1、testdata2: 存放待模型去检测的测试数据集。

- rf文件夹：存放随机森林模型的相关文件
    - getDynamicFeature.py：包括有获取opcode动态特征值的各种函数（现在只搞了92种）
    - geStaticFeature.py：包括有获取信息熵、重合指数和四种恶意特征函数统计静态特征值的各种函数（1+1+4）
    - pre_feature.pkl为训练集中提取的特征值的序列化数据，具体结构可见pre_pickle.py
    - trainmodel.py 模型实现以及一些功能函数实现

- mlp文件夹：存放多层感知机模型的相关文件
    - getDynamicFeature.py：包括有获取opcode动态特征值的各种函数（现在只搞了92种）
    - geStaticFeature.py：包括有获取信息熵、重合指数和四种恶意特征函数统计静态特征值的各种函数（1+1+4）
    - getData.py 实现获取文件所有特征的函数
    - deeplearn.py 模型实现以及一些功能函数实现

- model_saved
    - randomforest.pkl 训练好的rf模型
    - mlp.pth 训练好的的mlp模型

main.py：主程序，可直接运行。

requirements.txt：直接pip freeze导出太多了，包含了一堆不太需要的依赖，所以我自己手写了，不知道有没有漏。

webshell-test-samples：大概是参考论文作者的测试数据集，不太清楚其中是否全为webshell。

img：存放了tkinter需要使用的一些图片。

## 设计&代码说明
### 总体设计
![初期设计](https://files.catbox.moe/vex81y.png)

### 主窗口
![主窗口](https://files.catbox.moe/f9iz8k.png)

### 随机森林训练模块
主要代码思想在trainModel.py中。

随机森林的训练参数未做优化调整，为默认值；

特征值提取序列化保存路径也为默认值:traindata/pre_feature-default.pkl，需要可修改；

模型保存路径和训练数据集路径可选择；

点击开始训练即可提取特征值&生成随机森林模型，同时会拿生成的模型对训练的数据做一次预测，输出四个模型标准值。（发现自己预测自己无任何意义，命中率百分之百😝）

后续补充的话想输出排名前十或者二十的特征值看看。

**注意：选择的训练数据路径需要有black-traindata和white-traindata两个目录，除了这两个目录可以放php文件外，训练路径下不能出现其他php文件！**

![随机森林训练模块](https://files.catbox.moe/a3dvmw.png)

### 随机森林检测
主要代码逻辑在main.py，run_check函数为主要检测步骤。

可以选择测试集检测路径。

可以选择加载模型路径。

点击开始检测会开始提取前面输入的测试集检测路径的特征值，然后交给加载的随机森林模型进行分类，输出结果到UI中。

后续补充会展示模型的四个标准值。

![随机森林检测模块](https://files.catbox.moe/wv8a0b.png)

### tkinter的主要思想
主窗口：父窗口有四个功能按钮Button，主要放置在Canvas画布上，点击后可以弹出对应功能子窗口，进行功能使用；打开子窗口可以隐藏父窗口，关闭子窗口的同时能够返回父窗口。

随机森林检测功能模块：这个子窗口也是主要放置在Canvas画布上，然后有多个Button（点击触发反馈）、Entry（展示路径）和Listbox（展示结果）。

其他：待补充~

## 训练&测试数据收集

```
webshell主要用了下面的：
https://github.com/JohnTroony/php-webshells（aspydrv.php、erne.php、GFS_web-shell.php、mysql_tool.php、PHPRemoteView.php、PhpSpy.php、punk-nopass.php、tryag.php有点问题
https://github.com/tennc/webshell/tree/master/php
https://github.com/xl7dev/WebShell/tree/master/Php
https://github.com/JoyChou93/webshell/tree/master/PHP
https://github.com/DeEpinGh0st/Webshell-bypass-collection
https://github.com/bartblaze/PHP-backdoors
https://github.com/webshellpub/awsome-webshell/tree/master/php
（大致有803个？好少哦。应该够了吧😥不想找了，现在又1113个了，那差不多了。鱼龙混杂的，也不清楚这些样本的真实性如何。
----------------然后收集正常的-------------
https://github.com/WordPress/wordpress-develop（如果是这个的话，大概有1742个php文件
-------------------再放点测试集合------------
https://github.com/laravel/laravel（正常框架
https://github.com/x-o-r-r-o/PHP-Webshells-Collection（这个好像跟前面的phpwebshells也差不多
```
## 待解决的问题OR完善

- [ ] 随机森林调参优化
- [x] 随机森林训练模块UI制作
- [x] 随机森林检测模块UI制作
- [x] 神经网路训练模块UI制作
- [x] 神经网络检测模块UI制作
- [ ] 对于编码错误或者无法检测的php文件输出检测error到控制台和UI中。

我训练了traindata目录下的所有数据，成功训练了829个php-webshell和1741个正常php文件。本来php-webshell是有1113个的，但是因为编码错误或者vld拓展解析不了失败了200多个。我设置的默认编解码方式是gbk，出错的话会直接跳过进行摆烂行为。暂时不知道如何解决。

