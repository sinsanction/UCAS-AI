import json
import jieba
import gensim
import os


def split_word(sentence):
    words = jieba.cut(sentence)
    result = [word for word in words]
    return result


# 文件路径
train_filepath      = '../data/train_set.json'      # 训练集路径
test_filepath       = '../data/test_set.json'       # 测试集路径
output_filepath     = '../data/output.json'         # 输出路径

splitdata_filepath  = '../data/splitdata.json'  # 分词结果路径
dictionary_filepath = '../data/dictionary'      # gensim字典路径
model_filepath      = '../data/tfidf.model'     # tfidf模型路径
index_filepath      = '../data/tfidf.index'     # 相似度比较序列路径


with open(train_filepath, encoding='utf-8') as train_file:
    data = json.load(train_file)


# 生成分词结果
print("> 正在分词")
content = []
if os.path.exists(splitdata_filepath):
    with open(splitdata_filepath, encoding='utf-8') as f:
        content = json.load(f)
else:
    for value in data:
        question = value['question']
        content.append(split_word(question))
    with open(splitdata_filepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False))


# 生成gensim字典
print("> 正在生成gensim字典")
if os.path.exists(dictionary_filepath):
    dictionary = gensim.corpora.Dictionary.load(dictionary_filepath)
else:
    dictionary = gensim.corpora.Dictionary(content)
    dictionary.save(dictionary_filepath)
num_features = len(dictionary)
corpus = [dictionary.doc2bow(line) for line in content]


# 生成tfidf模型
print("> 正在生成TF-IDF模型")
if os.path.exists(model_filepath):
    tfidf = gensim.models.TfidfModel.load(model_filepath)
else:
    tfidf = gensim.models.TfidfModel(corpus)
    tfidf.save(model_filepath)


# 生成tfidf相似度比较序列
print("> 正在生成TF-IDF相似度比较序列")
if os.path.exists(index_filepath):
    index = gensim.similarities.Similarity.load(index_filepath)
else:
    index = gensim.similarities.Similarity(index_filepath, tfidf[corpus], num_features)
    index.save(index_filepath)


# 导入测试集进行测试
with open(test_filepath, encoding='utf-8') as test_file:
    test_data = json.load(test_file)
print("> 正在使用测试集测试，共有" + str(len(test_data)) + "个问题")

output = []
for value in test_data:
    question = value['question']         # 获得问题
    sentence = split_word(question)      # 分词
    vec = dictionary.doc2bow(sentence)   # 转词袋表示
    sims = index[tfidf[vec]]             # 相似度比较
    sorted_sims = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    i = sorted_sims[0][0]                # 最相似的问题的序号
    # 输出问答对
    output.append({'question:':value['question'], 'answer':data[i]['answer']}) 

with open(output_filepath, 'w', encoding='utf-8') as output_file:
    output_file.write(json.dumps(output, ensure_ascii=False))
print("  测试完成，输出见outut.json")


# 允许用户继续输入问题
sentences = input('Question: ')
while True:
    sentences = split_word(sentences)    # 分词
    vec = dictionary.doc2bow(sentences)  # 转词袋表示
    sims = index[tfidf[vec]]             # 相似度比较
    sorted_sims = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    i = sorted_sims[0][0]                # 最相似的问题的序号
    print(data[i]['answer'])
    sentences = input('Question: ')
