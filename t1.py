#coding=utf-8
import nltk
import os
import re
import LoadData
import Preprocess
from nltk.corpus import treebank, stopwords
from gensim import corpora, models, similarities

def text_lable_filter(text):
	text = re.sub(r'<.*?>', '', text)
	return text

# # dir_path = "/Users/luojiahua/Desktop/LDA/DUC2007_Summarization_Documents/duc2007_testdocs/main/D0710C/"
# def get_sentence_list():
# 	"""
# 	获取一个doc里面所有txt的内容，
# 	一个句子一行
# 	所有句子作为一个列表
# 	"""
# 	doc_path_list = LoadData.get_doc_path_list()
# 	# for i in xrange(0, len(doc_path_list)):
# 	file = []
# 	for i in xrange(0, 1):
# 		doc_path =  doc_path_list[i]
# 		file_path_list = LoadData.get_file_path_list(doc_path)
# 		for j in xrange(0, len(file_path_list)):
# 			file_path =  file_path_list[j]
# 			file = file + LoadData.LoadDataFromFile(file_path)
# 	return file

def get_file_list():
	"""
	获取一个doc里面所有txt的内容，
	一个句子一行
	一个txt文档一个列表
	"""
	doc_path_list = LoadData.get_doc_path_list()
	# for i in xrange(0, len(doc_path_list)):
	file_list = []
	for i in xrange(0, 1):
		doc_path =  doc_path_list[i]
		file_path_list = LoadData.get_file_path_list(doc_path)
		for j in xrange(0, len(file_path_list)):
			file_path =  file_path_list[j]
			file = LoadData.LoadDataFromFile(file_path)
			file_list.append(file)
	return file_list


def doc_tokenize(sentence):
	"""
	句子列表词条化
	"""
	tokens = nltk.word_tokenize(sentence)
	return tokens


def tokens_filtered_stopwords(token_list):
	english_stopwords = stopwords.words('english')
	english_stopwords = english_stopwords + ['ms', 'mr', 'd.', 'd.c']
	token_list_filter_stopwords = [token for token in token_list if not token in english_stopwords]
	return token_list_filter_stopwords


def tokens_filtered_punct(token_list):
	english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '``', "''", '--']
	token_list_filter_punct = [token for token in token_list if not token in english_punctuations]
	return token_list_filter_punct

def test(file_list):
	# file_list = get_file_list()
	# print file_list
	token_list_set = []
	for file in file_list:
		sentence_tokenized = []
		for sentence in file:
			sentence_tokenized += doc_tokenize(sentence)
		token_list_set.append(sentence_tokenized)
	f = open('1.txt', 'w')
	for x in token_list_set:
		for i in x:
			f.write(i+', ')
	f.close()
	token_list_set = [Preprocess.stemmer(token_list) for token_list in token_list_set]
	token_list_set = [[word for word in tokens_filtered_stopwords(token_list)] for token_list in token_list_set]
	token_list_set = [[word for word in tokens_filtered_punct(token_list)] for token_list in token_list_set]
	token_list_set = [[word for word in tokens_filtered_stopwords(token_list)] for token_list in token_list_set]
	# token_list = [[], token_list]
	# dictionary = Preprocess.generate_dictionary(token_list_set)
	all_stems = sum(token_list_set, [])
	# print all_stems
	# print all_stems

	stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
	# print stems_once
	texts = [[stem for stem in text if stem not in stems_once] for text in token_list_set]
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	# print corpus
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
	# corpus_lsi = lsi[corpus_tfidf]
	lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=3)
	corpus_lda = lda[corpus_tfidf]



doc_path = '/Users/luojiahua/Desktop/LDA/DUC2007_Summarization_Documents/duc2007_testdocs/main/'
doc_path_list = []
doc_list = os.listdir(doc_path)
for x in xrange(1, len(doc_list)):
	doc_path_list.append(doc_path+doc_list[x])
print doc_path_list[3]
file_path_list = []
file_name_list = os.listdir(doc_path_list[3])
file_path_list = [doc_path_list[3] + '/' + file for file in file_name_list]
file_list = []
for file_path in file_path_list:
	f = open(file_path)
	file = f.read()
	file = Preprocess.get_text(file)
	sentence_list = file.split(".;")
	file_list.append(sentence_list)
test(file_list)
# 	file_list.append(file)
# token_list_set = []

# for file_path in file_path_list:
	# f = open(file_path)
	# file = f.read()
# doc = Preprocess.doc_lable_filter(doc)
# tokens = Preprocess.doc_tokenize(doc)
# print tokens
# doc_tokens_set = []
# doc_headline_set = []
# for x in dirlist:
# 	file_path = dir_path + x
# 	# print file_path
# 	file = open(file_path)
# 	doc = file.read()
# 	text = Preprocess.get_text(doc)
# 	headline = Preprocess.get_headline(doc)
# 	doc_tokens = Preprocess.doc_tokenize(text)
# 	doc_stemmed_tokens = Preprocess.stemmer(doc_tokens)
# 	doc_tokens_set.append(doc_stemmed_tokens)
# 	doc_headline_set.append(headline)
# print len(doc_tokens_set)
# print len(doc_headline_set)
# dic = Preprocess.generate_dictionary(doc_tokens_set)
# # print dic.token2id
# '''
# 将用字符串表示的文档转换为用id表示的文档向量
# '''
# corpus = [dic.doc2bow(doc_stemmed_tokens) for doc_stemmed_tokens in doc_tokens_set]
# tfidf = models.TfidfModel(corpus)
# corpus_tfidf = tfidf[corpus]
# lsi = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=5)
# corpus_lsi = lsi[corpus_tfidf]
# for x in corpus_lsi:
# 	print x



# index = similarities.MatrixSimilarity(lsi[corpus])
# print doc_headline_set[10]
# ml_c = doc_tokens_set[10]
# ml_b = dic.doc2bow(ml_c)
# ml_lsi = lsi[ml_b]
# print ml_lsi
# sims = index[ml_lsi]
# sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print sort_sims[0:10]
# print doc_headline_set[10]
# print doc_headline_set[8]
# print doc_headline_set[14]
# file = open(dir_path+dirlist[2])
# print dir_path + dirlist[2]
# text = file.read()
# text = text.replace('\n', ' ').replace('\t','')
# text = Preprocess.get_text(text)
# print text
# tokens = nltk.word_tokenize(text)
# print tokens
# tokens = Preprocess.doc_tokenize(text)
# # print tokens
# tokens = Preprocess.stemmer(tokens)
# tokens = [[], tokens]
# print Preprocess.generate_dictionary(tokens)
# tokens = list(tokens)
# m = re.findall('<TEXT>.*?</TEXT>', text)
# if m:
# 	text = text_lable_filter(m[0])
# 	# print text
# else:
# 	print 'false'
# print os.getcwd()


# class LDAModel(object):
# 	"""docstring for LDAModel"""
# 	alpha = float
# 	beta = float
# 	D = int 	#文档数目
# 	K = int 	#主题个数
# 	W = int 	#词的个数
# 	Number_of_Iterations = int
# 	SaveStep = int

# 	Dictionary = object
# 	Z = object
# 	W = object
# 	IDListset = object

# 	nw = object
# 	nd = object
# 	nwsum = object
# 	ndsum = object
# 	theta = object
# 	phi = object
# 	def __init__(self, alpha, beta, Number_of_Iterations, SaveStep, K):
# 		super(LDAModel, self).__init__()
# 		self.alpha = alpha
# 		self.beta = beta
# 		self.Number_of_Iterations = Number_of_Iterations
# 		self.SaveStep = SaveStep
# 		self.K = K
# 		self.nwsum = ListUtil.Initial(self.K)
# sentence = "A number of countries are already planning to hold the euro as part of their foreign currency reserves, the magazine quoted European Central Bank chief Wim Duisenberg as saying."
# tokens = nltk.word_tokenize(sentence)
# print tokens
# english_stopwords = stopwords.words('english')
# texts_filtered_stopwords = [word for word in tokens if not word in english_stopwords]
# english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
# texts_filtered_stopwords = [word for word in texts_filtered_stopwords if not word in english_punctuations]
# st = LancasterStemmer()
# text_stemmed = [st.stem(word) for word in texts_filtered_stopwords]
# print text_stemmed

# print tokens
# tagged = nltk.pos_tag(tokens)
# tokens = nltk.word_tokenize(sentence)
# print tagged[0:6]
# entities = nltk.chunk.ne_chunk(tagged)
# print entities
# tree = treebank.parsed_sents('wsj_0001.mrg')[0]
# tree.draw()
# file = open('D0703.scu')
# text = file.readline()
# text = re.sub(r"<.*?>","", text)
# print text
# tokens = nltk.word_tokenize(text)
# print tokens
