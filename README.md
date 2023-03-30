# WebshellScout

一个基于随机森林进行机器学习的php-webshell检测项目，持续优化中~

## 目录&文件说明

Logs：存放控制台输出的日志记录，具体结构在Logger.py中

traindata：包括有black-traindata和white-traindata两个目录存放webshell训练集和normal训练集，pre_feature.pkl为训练集中提取的特征值的序列化数据，具体结构可见pre_pickle.py，rfc.pkl为使用joblib存储的RandomForestClassifier模型

getDynamicFeature.py：包括有获取opcode动态特征值的各种函数（现在只搞了92种）

geStaticFeature.py：包括有获取信息熵、重合指数和四种恶意特征函数统计静态特征值的各种函数

main.py：包含两种模块，1是训练模块，2是检测模块（不需要的话注释掉即可）

trainModel.py：训练模块的主要内容，可由main.py处进行调用训练。

requirements.txt：直接pip freeze导出太多了，包含了一堆不太需要的依赖，所以我自己手写了，不知道有没有漏。

## 运行说明

运行主要在main.py，包含有trainmodel.run_trainModel()和run_check模块。

运行前需要修改目录和文件的路径，主要在main.py和trainModel.py中。

还需要在traindata目录中创建两个目录：black-traindata和white-traindata，分别存放webshell训练集和normal训练集。

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

## 一些废话

我训练了traindata目录下的所有数据，成功训练了829个php-webshell和1741个正常php文件。本来php-webshell是有1113个的，但是因为编码错误或者vld拓展解析不了失败了200多个。

现在输出是在cmd和日志中，后续应该可以做成ui吧😕

项目有待优化~~~~

最后附上小小的学习过程：

https://www.yuque.com/sakura501/school/wc5qr9qeq7mdhfls

