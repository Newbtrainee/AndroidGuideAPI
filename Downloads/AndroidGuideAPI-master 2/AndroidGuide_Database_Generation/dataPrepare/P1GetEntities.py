# coding:utf-8
## quick get entities from crawl data : androidAPI_id_tag_full_info_training
import urllib.parse
from functools import cmp_to_key


from selenium import webdriver
import pymysql
import pymysql.cursors
import re



# operate mysql database
def generate_data():
    conn = pymysql.connect(host='localhost', port=3306, user='root',passwd='root', db='AndroidGuideAPI')
    cur = conn.cursor()
    cur.execute("delete from entities")
    schema_list = entity_selection()
    sqli = "insert into entities values(%s,%s,%s,%s,%s,%s,%s,%s)"
    for i, one_schema in enumerate(schema_list):
        cur.execute(sqli, (i + 1, one_schema[0].encode('utf-8'), one_schema[1].encode('utf-8'), one_schema[2].encode('utf-8'), one_schema[3].encode('utf-8'), one_schema[4].encode('utf-8'), one_schema[5].encode('utf-8'), one_schema[6].encode('utf-8')))
    cur.close()
    conn.commit()
    conn.close()


# select the triple
def entity_selection():
    file_id_tag = open('/Users/Grand/Downloads/HDSKG/tempdata/androidAPI_id_tag_full_info_copy.csv')

    file_filelist= open('/Users/Grand/Downloads/HDSKG/tempdata/filenamelist_copy.csv')


    filename_list={}
    for filenameline in file_filelist:
        filenames=filenameline.split(',',1)
        if len(filenames)==2 :
            key,value=filenames[1].strip('\n'),filenames[0]
            filename_list[key]=value





    phrase_list = []
    section_list = []
    url_list = []
    p_uid_list = []
    dict_pair={}

    schema_list = []

    for one_id_tag_line in file_id_tag:
        # print(one_id_tag_line)
        phrase_u_id = one_id_tag_line.split('\t,')[0]
        pure_phrase = one_id_tag_line.split('\t,')[1]
        pure_url=one_id_tag_line.split('\t,')[2]
        #pure_url = urllib.parse.unquote(pure_url).decode('utf8')
        groups=one_id_tag_line.split('\t,')
        pure_section=(''.join(groups[3:])).strip('\n')
        #pure_section = urllib.parse.unquote(pure_section).decode('utf8')

        if pure_phrase.isdigit() :
            continue
        breakphrase=pure_phrase.split(' ')
        if len(breakphrase)>1 :
            continue



        pure_parent=''
        pure_type=''
        pure_original=''
        classname=''

        #the first step , just get the entities from  the reference
        #next steps , it can add more from guide/topic/example/training ....
        if "http" not in pure_section:
            #h1 h2 ...
            if ("https://developer.android.com/reference" in pure_url):
                pure_type = pure_section
                pure_section=pure_url+'#'+pure_phrase
                phrase_list.append(pure_phrase)
                section_list.append(pure_section)
                url_list.append(pure_url)
                p_uid_list.append(phrase_u_id)
                page_position = ''
                page_url = ''

                pure_parent=''
                pure_original = pure_phrase
                # get the type of entity(class, method , filed ),  entity parent
                print(phrase_u_id)

                schema_list.append((pure_phrase, pure_section.strip('\n'), pure_url.strip('\n'), pure_parent, pure_type, pure_original,filename_list[pure_url.strip('\n')]))

        elif ("https://developer.android.com/reference" in pure_section):

            if pure_section not in section_list:
                phrase_list.append(pure_phrase)
                section_list.append(pure_section)
                url_list.append(pure_url)
                p_uid_list.append(phrase_u_id)
                page_position=''
                page_url=''
                #get the type of entity(class, method , filed ),  entity parent
                if '#' in pure_section:

                    pageinfo=pure_section.split('#')
                    page_url=pageinfo[0]
                    classname=page_url.rsplit('/',1)[1]
                    if '.' in classname:
                        classname=classname.rsplit('.',1)[0]

                    pure_parent=classname

                    page_position=pageinfo[1]
                    pure_original=page_position
                    if '(' in page_position:
                        pure_type='Method'
                    else:
                        pure_type='Field'
                else:
                    classname = pure_section.rsplit('/', 1)[1]
                    if '.' in classname:
                        classname = classname.rsplit('.',1)[0]
                    pure_original=classname
                    pure_type='Class'

                print(phrase_u_id)


                schema_list.append((pure_phrase,pure_section.strip('\n'),pure_url.strip('\n'),pure_parent,pure_type,pure_original,filename_list[pure_url.strip('\n')]))

    file_id_tag.close()
#    print(schema_list)
    print(len(schema_list))
    return schema_list






generate_data()

#entity_selection()
