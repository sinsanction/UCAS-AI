# UCAS-AI

UCAS 人工智能基础课程大作业，冬奥会领域问答机器人

该问答机器人属于检索式问答系统，采用 gensim 库和 TF-IDF 模型+余弦相似度算法。关于该问答机器人的原理，可以参考 doc 目录下的实验报告。

仅作思路参考，请不要直接照抄。

## 目录结构
1. data  
该目录下是实验使用的数据，train_set.json是训练集，test_set.json是测试集。目录“原始数据”下是老师提供的.xlsx、.csv、.ttl等格式的数据。output.json是此测试集的测试结果。
2. doc  
该目录下是实验报告和汇报使用的实验展示PPT。
3. src  
该目录下是问答机器人的源代码。


## 运行方法
1. 确认data目录下有训练集train_set.json和测试集test_set.json。
2. 在src目录下运行main.py，初次运行会在data下保存多个文件。
3. 根据output.json中的结果统计正确率。

| 文件 | 说明 |
| :--- | :--- |
| dictionary | gensim字典 |
| splitdata.json | 分词结果 |
| tfidf.index | 相似度序列 |
| tfidf.index.0 | 相似度序列缓存文件 |
| tfidf.model | TF-IDF模型 |
| output.json | 测试结果输出 |


## 注意事项
1. 实验使用的python版本为3.9.1 64-bit；gensim库版本为3.8.3；jieba库版本为0.42.1。
2. 第二次运行起会直接使用data目录下的文件构建模型，如果改变了训练集，请删除上方表格中的文件。
3. 输入、输出文件的格式均为json。


## 参考资料
1. [检索式问答机器人](https://github.com/vba34520/Retrieval-Bot)
2. [【gensim中文教程】开始使用gensim](https://blog.csdn.net/duinodu/article/details/76618638)
3. [TF-IDF算法原理及其使用详解](https://zhuanlan.zhihu.com/p/94446764)
