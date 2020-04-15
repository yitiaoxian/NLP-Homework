from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser

def sentence_splitter(sentence):
    """
    将文本分割为独立的句子
    :param sentence:文本内容
    :return :单个句子
    """

    single_sentence = SentenceSplitter.split(sentence)
    #分句
    print( '\n'.join(single_sentence))

def word_splitter(sentence):
    '''
    分词
    :param sentence:
    :return: 单个词
    '''
    segmentor = Segmentor()
    #初始化实例
    segmentor.load('E:\\NLP-Project\\ltp-data-v3.3.1\\ltp_data\\cws.model')
    #加载模型
    words = segmentor.segment(sentence)
    #分词
    '''
    默认的输出可以是 print '\t'.join(words)
    '''
    words_list = list(words)
    '''
    转换为list
    for word in words_list:
        print word
    '''
    segmentor.release()
    #释放模型
    return words_list

def word_tags(words):
    '''
    词性标注
    :param words:已经分好了的词
    :return:
    '''
    postagger = Postagger()
    #初始化实例
    postagger.load('E:\\NLP-Project\\ltp-data-v3.3.1\\ltp_data\\pos.model')
    postags = postagger.postag(words)
    #词性标注
    #print("词性标注结果")
    #for word, tag in zip(words, postags):
    #   print (word+'/'+tag)

    postagger.release()
    return postags

def name_recognition(words,postags):
    '''
    命名实体识别
    :param words:分词结果
    :param postags:标注结果
    :return:
    '''
    recognizer = NamedEntityRecognizer()
    #初始化实例
    recognizer.load('E:\\NLP-Project\\ltp-data-v3.3.1\\ltp_data\\ner.model')
    #模型加载
    netags = recognizer.recognize(words,postags)
    #识别命名实体

    result = ''
    for i in range(0,len(netags)):
        if i<len(words)-2:
            if 's' in netags[i]:
                if 'O' in netags[i+1] and words[i+1] != '' and words[i+1] != ',':
                    if 's' in netags[i+2] :
                        result += words[i]+words[i+1]+words[i+2]+""
    print(result)
    # for word, ntag in zip(words, netags):
    #     print word + '/' + ntag
    recognizer.release()
    return netags

def parse(words,postags):
    '''
    依存句法分析
    :param words:
    :param postags:
    :return:
    '''
    parser = Parser()
    #初始化实例
    parser.load('E:\\NLP-Project\\ltp-data-v3.3.1\\ltp_data\\parser.model')
    #加载parser的模型数据
    arcs = parser.parse(words,postags)
    #句法分析
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    parser.release()  # 释放模型

#测试命名实体的识别
print('测试命名实体识别')
words = word_splitter('学习 Python 与其他语言最大的区别就是，Python 的代码块不使用大括号 {} 来控制类，函数以及其他逻辑判断。python 最具特色的就是用缩进来写模块。')
tags = word_tags(words)
name_recognition(words,tags)

parse(words,tags)