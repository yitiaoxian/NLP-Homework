__author__ = '...'

import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SentenceSplitter
from pyltp import Parser

class RoleRelation:
    ltp_model_path = "E:\\NLP-homework\\ltp-data-v3.3.1\\ltp_data"
    # ltp模型路径
    book_root_path = "E:\\NLP-homework\\book"
    # 书籍路径
    relation_root_path = "E:\\NLP-homework\\RoleRelation"
    #人物关系路径
    nh_relation_root_path = "E:\\NLP-homework\\NHRelation"
    #

    seg = Segmentor()#分词
    seg.load(ltp_model_path + '/cws.model')
    postagger = Postagger()  # 初始化实例
    postagger.load(ltp_model_path + '/pos.model')  # 加载模型
    parser = Parser()  # 初始化实例
    parser.load(ltp_model_path + '/parser.model')  # 加载模型

    def getAllPath(self):
        print("---getAllPath start ---")
        txtpathlist = []
        dirlist = os.listdir(self.book_root_path)

        for dirname in dirlist:
            print("dirname:",dirname)
            fileposition = self.book_root_path + "\\" +dirname
            txtpathlist.append(fileposition)

        #print("getAllPath  txtpathlist长度",txtpathlist)
        #print("---getAllPath end ---")
        return txtpathlist

    def segmentor(self, sentence="测试，测试自然语言处理。"):
        """
        ltp的分词模型
        :return:
        :param sentence:
        """
        print("---segmentor start ---")
        words = self.seg.segment(sentence)
        words_list = list(words)
        for word in words_list:
             print(word)
        # self.seg.release()
        print("---segmentor end ---")
        return words_list

    def posttagger(self,words):
        print("---posttagger start ---")
        postags = self.postagger.postag(words)  # 词性标注
        # for word,tag in zip(words,postags):
        #     print (word, '/' , tag)
        # postagger.release()  # 释放模型
        print("---posttagger end ---")
        return list(postags)

    def myparse(self,words,postages):
        print("---myparse start ---")

        arcs = self.parser.parse(words,postages)
        #句法分析
        #arc.head表示依存父节点词的索引，arc.relation表示依存弧的关系
        for word in words:
            print(word)
        #print("句法分析：")
        for arc in arcs:
            print("myparse arc.head:",arc.head,"  arc.relation:",arc.relation)
        #print()
        SOVS = []

        for index_subject in range(len(arcs)):
            if arcs[index_subject].relation == "SBV":
                predicate = words[arcs[index_subject].head-1]#谓语
                subjects = [words[index_subject]]#主语
                myobjects = []

                index_myobject = -1
                for index_coo in range(len(arcs)):
                    if arcs[index_coo].relation == "COO" and arcs[index_coo].head == index_subject + 1:
                        subjects.append(words[index_coo])#并列主语
                    elif arcs[index_coo].relation == "VOB" and arcs[index_coo].head == arcs[index_subject].head:
                        index_myobject = index_coo
                        myobjects.append(words[index_coo])
                    elif index_myobject > 0 and arcs[index_coo].relation == "COO" and arcs[index_coo].head == index_myobject+1:
                        myobjects.append(words[index_coo])
                for subj in subjects:
                    if len(myobjects) > 0:
                       for myobject in myobjects:
                           print("myparse 1:",subj,predicate,myobject)
                           SOVS.append((subj,predicate,myobject))
                    else:
                        print("myparse 2:",subj,predicate)
                        SOVS.append((subj,predicate))

        print()
        print("---myparse end ---")
        return SOVS

    def getRoleRelation(self,path="E:\\NLP-homework\\book\\ThethreebodyproblemI.txt"):
        print("---getRoleRelation start ---")

        rf = open(path,"r",encoding="UTF-8")
        lines = rf.readlines()
        #print("getRoleRelation lines:",lines)
        rf.close()
        SOVS = []
        for line in lines:
            #print("getRoleRelation line:",line)
            line = line.replace("\n","").replace("\r","")
            if line != "":
                sents = SentenceSplitter.split(line)
                for sent in sents:
                    #print ("getRoleRelation :",sent)
                    words = self.segmentor(sent)
                    postags = self.posttagger(words)
                    SOVS += self.myparse(words,postags)
        print("---getRoleRelation end ---")
        return SOVS

    def getAllRoleRelation(self):
        print("---getAllRoleRelation start ---")
        dirlist = os.listdir(self.book_root_path)
        for dirname in dirlist:
            #print("getAllRoleRelation 1:",dirname)
            fileposition = self.book_root_path+"\\"+dirname
            #print("getAllRoleRelation fileposition:",fileposition)
            SOVS = self.getRoleRelation(fileposition)
            if len(SOVS) > 0:
                print()
                "=====start========"
                for sov in SOVS:
                    for s in sov:
                        print(s,)
                    print()
                print()
                "======end======"
                self.writeRelation(SOVS, dirname, self.relation_root_path + "/" + dirname)
        print("---getAllRoleRelation end ---")

    def writeRelation(self,SOVS,filename,path):
        print("---writeRelation start ---")
        print("writeRelation:filename",filename,"path :",path)
        wf = open(path,"w",encoding="utf-8")
        for sov in SOVS:
            for s in sov:
                wf.write(s+" ")
            wf.write("\n")
        wf.close()
        print("---writeRelation end ---")

    def getNH(self,path="E:\\NLP-homework\\book\\ThethreebodyproblemI.txt"):
        print("---getNH start ---")
        rf = open(path, "r",encoding="utf-8")
        lines = rf.readlines()
        rf.close()
        names = []
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            if line != "":
                sents = SentenceSplitter.split(line)
                for sent in sents:
                    print("getNH 1:" , sent)
                    words = self.segmentor(sent)
                    postags = self.posttagger(words)
                    for word, tag in zip(words, postags):
                        if tag == "nh":
                            print("getNH 2:",word, '/', tag)
                            names.append(word)
        print("---getNH end ---")
        return list(set(names))

    def getAllNH(self):
        print("---getAllNH start ---")
        txtlist = os.listdir(self.book_root_path)
        names_book = []
        for txtname in txtlist:
            #print("getAllNH 1:",txtname)
            txtpath = self.book_root_path+"\\"+txtname
            names_chapter = self.getNH(txtpath)
            names_book += names_chapter
        print("getAllNH",names_book)
        self.saveNames(list(set(names_book)))
        print("---getAllNH end ---")

    def saveNames(self,names,path = nh_relation_root_path+"/allnames.txt"):
        '''
        存放名字
        :param names:
        :param path:
        :return:
        '''
        print("---savaNames start ---")

        wf = open(path, "w",encoding="utf-8")
        for name in names:
            wf.write(name + "\n")
        wf.close()
        print("---savaNames end ---")


    def loadNameDict(self,path = nh_relation_root_path+"/allnames.txt"):
        print("---loadNameDict start ---")

        rf = open(path,"r",encoding="utf-8")
        name_dict = {}
        lines = rf.readlines()
        print(len(lines))
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            name_dict[line] = 1
        print("---loadNameDict end ---")

        return name_dict

    def fliterRelation(self,names_dict,path=relation_root_path + "/TheThreebodyproblemI.txt"):
        print("---fliterRelation start ---")

        rf = open(path,"r",encoding="utf-8")
        lines = rf.readlines()
        print(len(lines))
        nhline = []
        rf.close()
        for line in lines:
            line = line.replace("\n","").replace("\r","")
            spline = line.split(" ")
            if len(spline) > 0:
                if names_dict.__contains__(spline[0]):
                    nhline.append(line)
                    print(line)
        print("---fliterRelation end ---")

        return nhline

    def fliterAllRelation(self):
        """
        过滤掉主谓宾中非人名的主语
        :return:
        """
        print("---fliterAllRelation start ---")

        names_dict = self.loadNameDict()#加载添加的人名词典
        darlist = os.listdir(self.relation_root_path)
        for dirname in darlist:
            print("fliterAllRelation",dirname)
            #path = self.relation_root_path + "\\"+dirname
            path = self.relation_root_path
            txtlist = os.listdir(path)
            for txtname in txtlist:
                print("fliterAllRelation",txtname)
                nhline_chapter = self.fliterRelation(names_dict,path+"/"+txtname)
                #self.savaNames(nhline_chapter,self.nh_relation_root_path+"/"+dirname+"/"+txtname)
                self.saveNames(nhline_chapter, self.nh_relation_root_path + "/" + dirname )# savaNHRelation
        print("---fliterAllRelation end ---")


rr = RoleRelation()
rr.getAllRoleRelation()
rr.fliterAllRelation()