#coding=utf-8
import re
import nltk
from gensim import corpora
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def doc_lable_filter(doc):
	"""
	过滤文档的标签
	"""
	doc = doc.replace('\n', ' ').replace('\t','')
	doc = re.sub(r'<.*?>', '', doc)
	return doc


def get_text_count(doc):
	doc = doc.replace('\t','')
	m = re.findall('<TEXT>.*?</TEXT>', doc)
	print len(m)


def get_text(doc):
	"""
	获取文本内容
	"""
	doc = doc.replace('\n', ';').replace('\t','')
	m = re.findall('<TEXT>.*?</TEXT>', doc)
	if m:
		doc = doc_lable_filter(m[0])
		return doc
		# print text
	else:
		return 'false'


def get_headline(doc):
	doc = doc.replace('\n', ' ').replace('\t','')
	m = re.findall('<HEADLINE>.*?</HEADLINE>', doc)
	if m:
		headline = doc_lable_filter(m[0])
		return headline
	else:
		print 'false'


def doc_tokenize(doc):
	"""
	文档词条化并去掉标点符号
	"""
	tokens = nltk.word_tokenize(doc)
	english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '_']
	tokens = [word for word in tokens if not word in english_punctuations]
	return tokens


def stemmer(tokens):
	"""
	文档词干化
	"""
	st = nltk.LancasterStemmer()
	tokens = [st.stem(word) for word in tokens]
	return tokens


def generate_dictionary(tokens_list):
	"""
	构造词典
	""" 
	print 'Generating dictionary...'
	dictionary = corpora.Dictionary(tokens_list)
	print 'Total number of word is: ', len(dictionary)
	return dictionary


