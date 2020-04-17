import nltk

__author__ = "xiao"

from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SentenceSplitter

import os

class Books:
    '''
    获取每一章节的主要人物和整本书的主要人物
    '''
    ltp_model_path = "E:\\NLP-homework\\ltp-data-v3.3.1\\ltp_data"
    # ltp模型路径
    book_root_path = "E:\\NLP-homework\\book"
    # 书籍路径
    mainrole_root_path = "E:\\NLP-homework\\MainRole"
    # 主要人物路径
    mainloc_root_path = "E:\\NLP-homework\\MainLocation"
    #主要地点路径

    seg = Segmentor()
    seg.load(ltp_model_path + '/cws.model')
    postagger = Postagger()  # 初始化实例
    postagger.load(ltp_model_path + '/pos.model')  # 加载模型

    def readBookLines(self,path):
        rf = open(path,"r",encoding="utf-8")
        lines = rf.readlines()
        rf.close()

        return lines

    def writeTxt(self,path,namelist):
        print("path",path,"   namelist:",namelist,"结果写入")
        wf = open(path,"w",encoding="utf-8")
        for name,times,freq in namelist:
            wf.write(str(name)+" "+str(times)+" "+str(freq)+"\n")
        wf.close()
        print(namelist," writeTxt over")

    def segmentor(self,sentence = "这是测试"):
        words = self.seg.segment(sentence)
        words_list = list(words)
        #for word_list in words_list:
           # print("segmentor 1:", word_list)
        return words_list

    def postagNLNS(self,word_list):
        '''
        ltp词性标注
        nl 位置名
        ns 地名
        :param word_list:
        :return:
        '''
        postags = self.postagger.postag(word_list)#词性标注
        locations_list = []
        for word,tag in zip(word_list,postags):
            if (tag == "nl" or tag == "ns") and len(word)> 3:
                #print("postagNLNS :",word," ",tag)
                locations_list.append(word)
        return locations_list

    def postagNH(self,word_list):
        postags = self.postagger.postag(word_list)
        name_list = []
        for word ,tag in zip(word_list,postags):
            if tag == "nh" and len(word)> 3:
                print("postagNH :",word,'/',tag)
                name_list.append(word)
        print("postagNH name_list",name_list)
        print("postagNH list(postags)",list(postags))
        return list(postags),name_list

    def getTopTen(self,namelist):
        resultitf = []
        resultname = []
        top10Name = []
        chapter_fdist = nltk.FreqDist(namelist)
        #nltk
        top_name_list = sorted(chapter_fdist.items(), key=lambda x: x[1], reverse=True)
        for name, num in top_name_list[0:10]:
            tmplist = [name] * num
            top10Name += tmplist
            resultname.append(name)
        chapter_fdist_ten = nltk.FreqDist(top10Name)
        for name1, num1 in sorted(chapter_fdist_ten.items(), key=lambda x: x[1], reverse=True):
            print(name1, num1, round(float(chapter_fdist_ten.freq(name1)), 2))
            resultitf.append((name1, num1, round(float(chapter_fdist_ten.freq(name1)), 2)))
        return resultitf,resultname

    def mainLocation(self,filename = "Thethreebodyproblem.txt"):
        lines = self.readBookLines(self.book_root_path+"/"+filename)
        print("mainLocation:","filename", filename)
        lo_list_book =[]
        for line in lines :
            if line != "":
                sents = SentenceSplitter.split(line)
                for sent in sents:
                    words_line = self.segmentor(sent)
                    lo_list_line = self.postagNLNS(words_line)
                    lo_list_book += lo_list_line
        top_itf_book,top_loc_book = self.getTopTen(lo_list_book)
        lo_list_book += top_loc_book
        self.writeTxt(self.mainloc_root_path+"/"+filename,top_itf_book)

    def mainName(self,filename):
        lines = self.readBookLines(self.book_root_path+"\\"+filename)
        print("mainName 1 :",filename)
        name_list_book = []
        for line in lines:
            if line != "":
                sents = SentenceSplitter.split(line)
                for sent in sents:
                    words_line = self.segmentor(sent)
                    postags_line,name_list_line = self.postagNH(words_line)
                    name_list_book += name_list_line
        print("mainName 0 name_list_book",name_list_book)
        top_itf_book,top_name_book = self.getTopTen(name_list_book)
        print("mainName 2 top_name_book:", top_name_book)
        print("mainName 3 top_itf_book:", top_itf_book)
        self.writeTxt(self.mainrole_root_path+'\\'+filename,top_itf_book)

    def getAllMainName(self):
        filenames = os.listdir(self.book_root_path)
        print("getAllMainName1:",filenames)
        for filename in filenames:
            print("getAllMainName2 : ",filename)
            self.mainName(filename)
    def getAllMainLoc(self):
        filenames = os.listdir(self.book_root_path)
        for filename in filenames:
            print("getAllMainLoc : ", filename)
            self.mainLocation(filename)
import time
start = time.time()
book = Books()
book.getAllMainLoc()
book.getAllMainName()
end = time.time()
print("主要人物处理时间：",end - start)