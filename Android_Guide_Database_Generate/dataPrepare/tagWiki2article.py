#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys

# reload(sys)
# sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup
# from nltk.tag.stanford import StanfordPOSTagger
# import nltk
# nltk.download()

from xml.sax.saxutils import escape, unescape

# wiki = 'tagWIKIV2.txt'
wiki = 'tag_wiki_in.csv'

#
# Preprocess the tagwiki, delete useless sign and informations, split sentence and give id to every sentence
#
file_w = open('tag_wiki_out.txt','w')
file = open(wiki)
for i, line in enumerate(file):
	# if i > 100:
	# 	break
	#
	# separate id and tagwiki
	#
	id = re.split(',', line)[0]
	onewiki = re.split(',', line)[1:]
	onewiki = ','.join(onewiki)
	onewiki = onewiki.replace('\,', ',')
	onewiki = onewiki.replace('&#xA;  ', ' ')


	#
	# delete information after line(<hr>)
	#
	onewiki = re.split('<h', onewiki)[0]
	# onewiki = re.split('<p><strong>', onewiki)[0]

	# print onewiki
	#
	# make soup
	#
	html = BeautifulSoup(onewiki.decode('utf-8'), 'html.parser')

	#
	# Delete the sentences which contain keywords
	#
	# for p in html.findAll('p'):
	# 	for hs in html.findAll(['h2', 'h3']):
	# 		hs.extract()

	#
	# delete all the code
	#
	[x.extract() for x in html.findAll('code')]

	text = (u' '.join(html.findAll(text=True)).strip())
	text = text.replace(' .', '.')
	# print text

	#
	# delete $#xA and zhuanyizifu?what?
	#
	# print text
	text = text.replace('&#xA;', '')
	text = unescape(text)
	# print text

	#
	# Delete text which contain like this (string) and <string>
	#

	text = re.sub(r'[(].*?[)]', '', text)
	text = re.sub(r'[<].*?[>]', '', text)
	text = re.sub(r'[[].*?[]]', '', text)
	text = text.strip()


	#
	# some simple sign
	#
	text = text.replace(' .', '.')
	text = text.replace(' ,', ',')
	text = text.replace('  ', ' ')
	text = text.replace('(', '')
	text = text.replace(')', '')
	text = text.replace('<', '')
	text = text.replace('>', '')
	text = text.replace('  ', ' ')
	text = text.replace(':\n', '.\n')
	text = text.replace(' : \n', '.\n')
	text = text.replace(': \n', '.\n')
	text = text.strip('\n')

	newText = ''
	for j, line in enumerate(re.split('\n', text)):
		line = line.strip('\n').strip(' ').strip('.').strip(';').strip('?').strip(' ')
		if len(re.split(' ', line)) < 3:
			# print line + 'aaaa'
			# print re.split(' ', line)
			continue
		else:
			newText += line + '. '
			# print line + 'bbb'
			# print re.split(' ', line)

	newText = newText.replace('  ', ' ')
	newText = newText.replace('  ', ' ')
	newText = newText.strip('\n').strip(' ')

	#
	# TSV output
	#
	if len(re.split(' ', newText)) >= 3:
		tsv_text = '%d	%s\n' % (int(''.join(id)), newText)
		# print tsv_text
		file_w.write(tsv_text.encode(encoding='UTF-8', errors='ignore'))

	# if len(re.split(' ', text)) >= 0:
	# 	tsv_text = '%d	%s' % (int(''.join(id)), text)
	# 	print tsv_text
	# 	file_w.write(tsv_text.encode(encoding='UTF-8', errors='ignore'))

file_w.close()
