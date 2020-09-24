from gensim import corpora
from gensim.similarities import Similarity
import jieba
import re
import sys


def remove_punctuation(line):
    # 保留文字
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('', line)
    return line


def main():
    stopword = open('D:\code/test\哈工大停用词表.txt', encoding='utf8')  # 获取停用词列表
    stopwordlist = list(jieba.cut(stopword.read()))
    print(stopwordlist)
    try:
        orig_path, add_path, save_path = sys.argv[1:4]
    except Exception as e:
        print(sys.argv)
        print(e)
   # save_path = 'D:\code/test/out.txt'
    # 源文本预处理
  #  orig_path = 'D:\code/test/orig.txt'
    orig_file = open(orig_path, 'r', encoding="utf-8")
    text = orig_file.read()
    text = remove_punctuation(text)
    text = list(text)
    afterswlis = []
    for each in text:
        if each not in stopwordlist:
            afterswlis.append(each)
        else:
            continue
    text = afterswlis
    text ="".join(text)
    orig_file.close()
    # 预处理查重文本
   # add_path = 'D:\code/test/orig_0.8_dis_15.txt'
    add_file = open(add_path, 'r', encoding="utf-8")
    add_text = add_file.read()
    add_file.close()
    add_text = remove_punctuation(add_text)
    add_text = list(add_text)
    afterswlis = []
    for each in add_text:
        if each not in stopwordlist:
            afterswlis.append(each)
        else:
            continue
    add_text = afterswlis
    add_text = "".join(add_text)
    # 文本转向量
    texts = [jieba.lcut(text)]
    dictionary = corpora.Dictionary(texts)
    num_features = len(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    add_vec = dictionary.doc2bow(jieba.lcut(add_text))
    # 向量计算相似度
    similarity = Similarity('-Similarity-index', corpus, num_features)
    # 转换类型，切片保留两位小数
    a = similarity[add_vec]
    b = a[0]
    b = str(b).split('.')[0] + '.' + str(a).split('.')[1][:2]
    print("相似的计算结果：%s" % b)
    # 输出结果写入指定文档
    f = open(save_path, 'w', encoding="utf-8")
    f.write("相似的计算结果：%s" % b)
    f.close()


if __name__ == '__main__':
    main()