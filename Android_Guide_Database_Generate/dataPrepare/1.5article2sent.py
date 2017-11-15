#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import os
import re
import string

from pycorenlp import *
import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

import codecs
import chardet
######################data preprocess#####################
def id_tag_dict():
	data_path = os.pardir + '/data'

	id_tag = data_path+'/androidAPI_id_tag.csv'

	#
	# make id_tag dictionary
	#
	file = open(id_tag,'r',encoding='utf-8')
	id_tag_dict = {}
	for i, line in enumerate(file):
		id = line.split(',')[0]
		tag = line.split(',')[1].strip()

		#
		# make dictionary
		#
		id_tag_dict[int(id)] = tag
	return id_tag_dict
def main():
	data_path = os.pardir + '/data'
	allSent = []
	file_w = open(data_path+'/androidAPIallSent.txt','w',encoding='utf-8')
	wiki = data_path+'/tag_AndroidAPI_out.txt'
	file = open(wiki,'r',encoding='utf-8')
	for i, line in enumerate(file):

		idstr=line.split('\t')[0]
		otherstr=line.split('\t')[1:]
		id = int(idstr)

		onewiki = (' '.join(otherstr)).split('.')

		#
		# if sentence lower than 3 word, delete it
		#
		for j, oneSent in enumerate(onewiki):
			# print oneSent
			# print len(oneSent)
			if len(oneSent.split(' ')) < 3 or len(oneSent) < 3:
				# print oneSent
				del onewiki[j]

		myid_tag_dict = id_tag_dict()

		#
		# change it to the tag if it is the first word, add '.' to the end, if sentence lower than 3 word, delete it, stripe every sentences,
		#
		for j, oneSent in enumerate(onewiki):

			#
			# change 'it' to the 'tag' if 'it' is the first word, add '.' to the end, give No. to every sentence
			#
			oneSent = oneSent.strip('\n').strip('.') + '.'
			oneSent = oneSent.strip().strip('.').replace(' …', '').replace('… ', ' ').\
				replace(' ↔', '').replace('Λ', '').replace('Μ', '').replace(' –', '').replace(' —', '').replace('–', '-').\
						   replace('you’re', 'you are').replace('What’s ', 'What is').replace('’', '\'').\
						   replace('it’s', 'It is').replace('It’s', 'It is').replace('®', '').replace('™', '').replace('ü', 'u').\
						   replace('Θ', '0').replace(' --', '').replace('“', '\'').replace('”', '\'').encode(encoding='UTF-8')
			# if chardet.detect(oneSent)['encoding'] not in ( 'ascii', 'utf-8'):
			# 	continue
			# else:
			# 	# print oneSent + '    before aaaaaaaaaaaaaaa'

			temptext=oneSent
			if type(oneSent) is bytes:
				temptext="".join(map(chr,oneSent))


			temptext=temptext.strip()
			if temptext is "":
				continue

			#清除非ASCII符号
			temptext=''.join([i if ord(i) < 128 else ' ' for i in temptext])
			dirty=temptext

			temptext=re.sub(r'[\0\200-\377]','',dirty)
			temptext=str(temptext)


			# print(type(temptext))



			# headertext=temptext.split(' ')[0]
            #
            #
			# if headertext.strip() == 'It':
			# 	temptext.replace('It',myid_tag_dict[id].strip(),1)
			# 	# temptext = ('%d_%d	%s %s%s') % (id, j, temptext.split(' ')[0].replace('It', myid_tag_dict[id]).strip(), temptext.split(' ', 1)[1], '.')
			# elif headertext.strip() == 'It\'s':
			# 	temptext.replace('It\'s', myid_tag_dict[id].strip(), 1)
			# 	# temptext = ('%d_%d	%s %s%s') % (id, j, temptext.split(' ')[0].replace('It\'s', myid_tag_dict[id].strip() + '\'s'), temptext.split(' ', 1)[1],'.')
			# elif headertext.strip() == 'Its':
			# 	temptext.replace('Its', myid_tag_dict[id].strip(), 1)
			# 	# temptext = ('%d_%d	%s %s%s') % (id, j, temptext.split(' ')[0].replace('Its', myid_tag_dict[id].strip() + '\'s'), temptext.split(' ', 1)[1],'.')
			# else:
			# 	# temptext = ('%d_%d	%s%s') % (id, j, temptext.strip(), '.')
			# 	temptext=temptext.strip()

			temptext = ('%d_%d	%s%s') % (id, j, temptext.strip(), '.')
			a1re=re.compile(r'\.+')
			temptext=a1re.sub('.',temptext)

			oneSent=temptext
			# print oneSent + '    after bbbbbbbbbbbbbb'
			allSent.append(oneSent)
			file_w.write(oneSent + '\n')
		print(i)
	file.close()
main()