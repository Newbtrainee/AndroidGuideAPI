#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from pycorenlp import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import codecs
import chardet
######################data preprocess#####################
def id_tag_dict():
	id_tag = 'id_tag.csv'

	#
	# make id_tag dictionary
	#
	file = open(id_tag)
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
	allSent = []
	file_w = open('allSent.txt','w')
	wiki = 'tag_wiki_out.txt'
	file = open(wiki)
	for i, line in enumerate(file):

		#
		# separate id and tagwiki
		#
		id = int(line.split('\t')[0])
		onewiki = (' '.join(line.split('\t')[1:])).split('. ')

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
						   replace('it’s', 'it is').replace('®', '').replace('™', '').replace('ü', 'u').\
						   replace('Θ', '0').replace(' --', '').replace('“', '\'').replace('”', '\'').encode(encoding='UTF-8')
			if chardet.detect(oneSent)['encoding'] != 'ascii':
				continue
			else:
				# print oneSent + '    before aaaaaaaaaaaaaaa'
				if oneSent.split(' ')[0] == 'It':
					oneSent = ('%d_%d	%s %s%s') % (id, j, oneSent.split(' ')[0].replace('It', myid_tag_dict[id]).strip(), oneSent.split(' ', 1)[1], '.')
				elif oneSent.split(' ')[0] == 'It\'s':
					oneSent = ('%d_%d	%s %s%s') % (id, j, oneSent.split(' ')[0].replace('It\'s', myid_tag_dict[id].strip() + '\'s'), oneSent.split(' ', 1)[1],'.')
				elif oneSent.split(' ')[0] == 'Its':
					oneSent = ('%d_%d	%s %s%s') % (id, j, oneSent.split(' ')[0].replace('Its', myid_tag_dict[id].strip() + '\'s'), oneSent.split(' ', 1)[1],'.')
				else:
					oneSent = ('%d_%d	%s%s') % (id, j, oneSent, '.')
				# print oneSent + '    after bbbbbbbbbbbbbb'
			allSent.append(oneSent)
			file_w.write(oneSent + '\n')
		print i
	file.close()
main()