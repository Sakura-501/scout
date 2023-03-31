# WebshellScout

一个基于随机森林（1+1+4+92种特征）进行机器学习的php-webshell检测项目，后续可能添加神经网络进行训练，UI制作主要基于Python内置库tkinter，持续优化中~

## 目录&文件说明

Logs：存放控制台输出的日志记录，具体结构在Logger.py中

traindata：包括有black-traindata和white-traindata两个目录存放webshell训练集和normal训练集，pre_feature.pkl为训练集中提取的特征值的序列化数据，具体结构可见pre_pickle.py，rfc.pkl是使用joblib存储的RandomForestClassifier模型

check: 存放待模型去检测的测试数据集，也可自行更改目录。

getDynamicFeature.py：包括有获取opcode动态特征值的各种函数（现在只搞了92种）

geStaticFeature.py：包括有获取信息熵、重合指数和四种恶意特征函数统计静态特征值的各种函数（1+1+4）

main.py：包含多种模块，1是随机森林训练模块，2是随机森林检测模块；现在已完成随机森林检测模的UI制作，可直接运行。

trainModel.py：训练模块的主要内容，可由main.py处进行调用训练。

requirements.txt：直接pip freeze导出太多了，包含了一堆不太需要的依赖，所以我自己手写了，不知道有没有漏。

test：存放了一些自行练习测试demo的东西。

webshell-test-samples：大概是参考论文作者的测试数据集，不太清楚其中是否全为webshell。

img：存放了tkinter需要使用的一些图片。

## 运行&代码说明
### 检测
运行主要在main.py，包含有trainmodel.run_trainModel(随机森林训练)和run_check(随机森林检测)。

如果只使用检测模块，直接`python main.py`即可（现在主要完成了随机森林检测模块，主要tkinter的逻辑在run_tkinter_root函数中）

### tkinter的主要思想
主窗口：父窗口有四个功能按钮Button，主要放置在Canvas画布上，点击后可以弹出对应功能子窗口，进行功能使用；打开子窗口可以隐藏父窗口，关闭子窗口的同时能够返回父窗口。

随机森林检测功能模块：这个子窗口也是主要放置在Canvas画布上，然后有多个Button（点击触发反馈）、Entry（展示路径）和Listbox（展示结果）。

其他：待补充~

### 训练
如果需要训练模型，运行前需要修改目录和文件的路径，trainModel.py中。

还需要在traindata目录中创建两个目录（如果没有）：black-traindata和white-traindata，分别存放webshell训练集和normal训练集。

后续完成训练模块的编写~

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
## 设计&成果展示
![初期设计](https://files.catbox.moe/vex81y.png)

![主窗口](https://files.catbox.moe/f9iz8k.png)

![随机森林检测模块](https://files.catbox.moe/wv8a0b.png)


## 一些废话

我训练了traindata目录下的所有数据，成功训练了829个php-webshell和1741个正常php文件。本来php-webshell是有1113个的，但是因为编码错误或者vld拓展解析不了失败了200多个。我设置的默认编解码方式是gbk，出错的话会直接跳过进行摆烂行为。暂时不知道如何解决。

现在输出是在cmd和日志中，后续应该可以做成ui吧😕

最后附上自己的学习过程：

https://www.yuque.com/sakura501/school/wc5qr9qeq7mdhfls

## 待解决的问题OR完善
随机森林检测模块UI制作√

随机森林训练模块UI制作

对于编码错误或者无法检测的php文件输出检测error到控制台和UI中

