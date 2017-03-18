#coding=utf-8
import os  
import string  
import re

def get_doc_path_list():
    document_path = "/Users/luojiahua/Downloads/Automatic-Text-Summarizer-master/Data/Summaries - Multi-Doc Split/Documents/"
    doclist = os.listdir(document_path)
    length = len(doclist)
    doc_path_list = []
    for i in xrange(1, length):
        doc_path = document_path + doclist[i]
        doc_path_list.append(doc_path)
    return doc_path_list


def get_file_path_list(doc_path):
    file_list = os.listdir(doc_path)
    length = len(file_list)
    file_path_list = []
    for i in xrange(1, length):
        file_path = doc_path + '/' + file_list[i]
        file_path_list.append(file_path)
    return file_path_list
  

def LoadDataFromFile(path):  
    """param path:短文本存放路径"""
  
    #转换为绝对路径
    fp = open(path, 'r')  
    doc = fp.read()
    doc = doc.replace('\n', ' ')
    doc = re.sub('\. ', '.\n', doc)
    doc = re.sub(';', '\n', doc)
    doc = doc.replace('\r ', '')
    fp.close() 
    Docs = doc.split('\n') 
    # print "Done, load ", len(Docs), " docs from the file"  
    return Docs  

  
def LoadStopWords():  
    """ 
    从指定路径读取停用词表 
    return:停用词列表 
    """  
    path = os.getcwd()  
    path += "/StopWords.txt"  
    fp = open(path, 'r')  
    #获取停用词列表  
    StopWordsList = [line.strip('\n') for line in fp]  
    fp.close()  
    return StopWordsList  
  
  
def LoadDictionary():  
    """ 
    从指定路径加载训练词典 
    """  
    path = os.getcwd() + "/dictionary.txt"  
    fp = open(path, 'r')  
    Dictionary = dict()  
    for line in fp:  
        elements = line.strip('\n').split(" ")  
        #词的id  
        k = string.atoi(elements[0])  
        #词本身  
        v = elements[1]  
        Dictionary[k] = v  
    fp.close()  
    return Dictionary  