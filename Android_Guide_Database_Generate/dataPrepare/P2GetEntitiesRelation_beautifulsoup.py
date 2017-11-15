# compare_exact_string
import re

import bs4
import pymysql
import time
from bs4 import BeautifulSoup, NavigableString, Tag


def c_e_s(checkword, checkString):
    ablankre = re.compile(r'\s+')
    alinebreakre = re.compile(r'\n+')
    checkString=alinebreakre.sub(' ',checkString)
    checkString=ablankre.sub(' ',checkString)
    checkword=alinebreakre.sub(' ',checkword)
    checkword = ablankre.sub(' ', checkword)
    str1list = checkword.split()
    str2list = checkString.split()
    flag = True
    for word in str1list:
        if word not in str2list:
            flag = False
            break;
    return flag


def remove_non_ascii_and_line_break(oneSent):
    oneSent.replace('\\n', ' ')
    oneSent = ''.join([i if (ord(i) < 128) and (i is not '\n') else ' ' for i in oneSent])
    return oneSent


def sentence_in_section(sentence, sectionText):

    ablankre = re.compile(r'\s+')
    alinebreakre = re.compile(r'\n+')

    sectionText = alinebreakre.sub(' ', sectionText)
    sectionText = ablankre.sub(' ', sectionText)
    sentence = alinebreakre.sub(' ', sentence)
    sentence = ablankre.sub(' ', sentence.strip(' '))

    sentenceword = sentence.split()
    sectionTextword = sectionText.split()
    count = 0

    thecontinue=0
    maxthecontinue=0


    for word in sentenceword:
        if word not in sectionTextword:
            count = count + 1
            thecontinue=0
        else:
            thecontinue=thecontinue+1
            maxthecontinue=max(maxthecontinue,thecontinue)

    caculate=count * (1.0) / len(sentenceword)
    concaculate = 1-(maxthecontinue * (1.0) / len(sentenceword))
    #the words in the section more then caculate is small
    #less words continiue match  then concaculate is smal
    return (caculate,concaculate)


def checkAnyRelationToSection():

    file_filenamelist = open('/Users/Grand/Downloads/HDSKG/tempdata/filenamelist.csv')
    file_triple = open('/Users/Grand/Downloads/HDSKG/tempdata/androidAPIallCand5_ascii.txt')
    file_allsentence = open('/Users/Grand/Downloads/HDSKG/tempdata/AndroidAPI_allSent_ascii.txt')
    file_keyPhrase = open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out.txt', 'w')

    alinebreakre = re.compile(r'\n+')
    alineblankre = re.compile(r'\s+')



    #get all sentences
    dict_allsentence = {}


    # count1=0
    for line in file_allsentence:
        # #debug
        # count1=count1+1
        # if count1==10000:
        #     break

        data = re.split(r'\t+', line.strip('\t').rstrip('\r').rstrip('\n'))
        if len(data) == 2:
            key, value = data[0], data[1]
            dict_allsentence[key] = value

    file_allsentence.close()

    #get all relation
    dict_allrelation={}

    # count1=0
    for j, one_triple in enumerate(file_triple):
        # #debug
        # count1=count1+1
        # if count1==10000:
        #     break

        if type(one_triple) is str or type(one_triple) is bytes:
            # Python 3 renamed the unicode type to str, the old str type has been replaced by bytes
            one_triple = eval(one_triple.strip('\n'))

        # all triple example:
        # {'subject_ori': 'administrators', 'relation_ori': 'configure', 'object_ori': 'app', 'subject': 'administrators', 'relation': 'configure', 'object': 'app', 'subject_stand': 'administrator', 'relation_stand': 'configure', 'object_stand': 'app', 'start_index': 14, 'end_index': 21, 'originalSent_len': 27, 'pos': 'NNS VB NN', 'relationType': 'NonTaxo', 'rel_id': '11352_27_1'}

        sentence_id = one_triple['rel_id'].rsplit('_', 1)[0]

        if sentence_id in dict_allsentence:

            entity1 = one_triple['subject_ori']
            relation = one_triple['relation_ori']
            entity2 = one_triple['object_ori']
            entity_url_id = one_triple['rel_id'].split('_')[0]
            sentence_id = one_triple['rel_id'].rsplit('_', 1)[0]
            sentence_text = dict_allsentence[sentence_id]
            relation_id = one_triple['rel_id']
            posInfo=one_triple['pos']

            # dict.setdefault('19', {})['19_1_1'] = ('19', 78, 'tup5-2', '19_1_1')
            dict_allrelation.setdefault(entity_url_id,{})[relation_id]=(entity1,relation,entity2,entity_url_id,sentence_id,sentence_text,posInfo,relation_id)

    file_triple.close()





    all_schema_list=[]

    # count1=0
    #for each file check the realtion position
    for one_line in file_filenamelist:

        # #debug
        # count1=count1+1
        # if count1==500:
        #     break

        one_line = one_line.rstrip('\n').rstrip('\r')
        urlsplit = one_line.split(',')
        url_id = urlsplit[0]
        print("processing file :" + one_line)
        url=(''.join(urlsplit[1:])).strip('\n')
        wwwurl='https://' + url.replace('/Users/Grand/Downloads/sitesucker/guideAPI/', '')

        if url_id not in dict_allrelation:
            continue

        currentRelations=dict_allrelation[url_id]



        with open(url, 'r', encoding='utf-8') as fhtml:
            html_code = fhtml.read()
            # test filename='/Users/Grand/Downloads/HDSKG/tagwiki_dataPreProcess/index.html'


        soup = BeautifulSoup(html_code, "html.parser")
        fhtml.close()

        pageheaderlist=[]
        schema_list = []

        # remove scripts  of this html file
        [s.extract() for s in soup.findAll('script')]

        # <nav class="dac-nav">
        [s.extract() for s in soup.findAll('nav', {"class": "dac-nav"})]

        # remove <table class="jd-sumtable-expando responsive">
        [s.extract() for s in soup.findAll('table', {"class": "jd-sumtable-expando responsive"})]
        #

        # remove <table class="jd-sumtable-expando responsive">
        [s.extract() for s in soup.findAll('table', {"class": "jd-sumtable-expando"})]
        #
        # #remove <div class="sum-details-links">
        # [s.extract() for s in soup.findAll('div',{"class":"sum-details-links"})]
        #
        # < div class="data-reference-resources-wrapper">
        [s.extract() for s in soup.findAll('div', {"class": "data-reference-resources-wrapper"})]

        # <div id="api-info-block">
        [s.extract() for s in soup.findAll('div', {"id": "api-info-block"})]

        # <div class="api-level">
        [s.extract() for s in soup.findAll('div', {"class": "api-level"})]


        # comments of this html file
        for element in soup(text=lambda text: isinstance(text, bs4.element.Comment)):
            element.extract()

        news=soup.find('div', {"class": "jd-descr", "itemprop": "articleBody"})
        if news is None:
            news = soup.find(attrs={"id": "body-content"})
            if news is None:
                continue


        #get all h3,h2,h1 sectioin and their text content
        section_count=0
        for header in news.find_all('h3'):
            nextNode = header
            headerName = str("".join(header.find_all(text=True))).strip().rstrip('.')
            temptext = ""
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    break
                if isinstance(nextNode, NavigableString):
                    if nextNode.strip() is not "":
                        temptext = temptext + '\n' + nextNode.strip()
                if isinstance(nextNode, Tag):
                    if nextNode.name == "h2" or nextNode.name == "h3" or nextNode.name == "h1":
                        break
                    # print("the h3 title: " + headerName)
                    # print(nextNode.name)
                    temptext = temptext + '\n' + nextNode.get_text().strip()

            if (temptext.strip() is not ""):
                # print("the h3 title: " + headerName)
                # print(alinebreakre.sub('\n', alineblankre.sub(' ', temptext.strip('\n'))))
                section_count=section_count+1
                pageheaderlist.append((headerName,alinebreakre.sub('\n', alineblankre.sub(' ', temptext.strip('\n'))),'h3',section_count))

        for header in news.find_all('h2'):
            nextNode = header
            headerName = str("".join(header.find_all(text=True))).strip().rstrip('.')
            temptext = ""
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    break
                if isinstance(nextNode, NavigableString):
                    if nextNode.strip() is not "":
                        temptext = temptext + '\n' + nextNode.strip()
                if isinstance(nextNode, Tag):
                    if nextNode.name == "h2" or nextNode.name == "h3" or nextNode.name == "h1":
                        break
                    # print("the h3 title: " + headerName)
                    # print(nextNode.name)
                    temptext = temptext + '\n' + nextNode.get_text().strip()

            if (temptext.strip() is not ""):
                # print("the h2 title: " + headerName)
                section_count = section_count + 1
                pageheaderlist.append((headerName, alinebreakre.sub('\n', alineblankre.sub(' ', temptext.strip('\n'))),'h2', section_count))

        for header in soup.find_all('h1'):
            nextNode = header
            headerName = str("".join(header.find_all(text=True))).strip().rstrip('.')
            temptext = ""
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    break
                if isinstance(nextNode, NavigableString):
                    if nextNode.strip() is not "":
                        temptext = temptext + '\n' + nextNode.strip()
                if isinstance(nextNode, Tag):
                    if nextNode.name == "h2" or nextNode.name == "h3" or nextNode.name == "h1":
                        break
                    # print("the h3 title: " + headerName)
                    # print(nextNode.name)
                    temptext = temptext + '\n' + nextNode.get_text().strip()

            if (temptext.strip() is not ""):
                # print("the h1 title: " + headerName)
                # print(alinebreakre.sub('\n', alineblankre.sub(' ', temptext.strip('\n'))))
                section_count = section_count + 1
                pageheaderlist.append((headerName, alinebreakre.sub('\n', alineblankre.sub(' ', temptext.strip('\n'))),'h1', section_count))

        # data.sort(key=lambda tup: tup[1])
        pageheaderlist.sort(key=lambda tup:tup[3])
        #check each relation in which section
        countschemlist=0
        for one_triple_currentpage in currentRelations:

            minratio=(1.0,1.0)
            firstflag=True
            relation_id=currentRelations[one_triple_currentpage][7]
            for one_section in pageheaderlist:
                if firstflag:
                    use_section = one_section
                    firstflag=False
                phrase_headername = one_section[0]
                phrase_headertext=one_section[1]
                phrase_headertype=one_section[2]
                currentratio=sentence_in_section(currentRelations[one_triple_currentpage][5],phrase_headertext)
                if (currentratio[0]< minratio[0]) or (currentratio[1] < minratio[1]):
                    minratio=currentratio
                    use_section=one_section
                    if minratio[0]==0.0 and minratio[1]==0.0 :
                        break


            #下次修改代码要将" ， 要将字段分割符改变为\t\t
            if relation_id in currentRelations[one_triple_currentpage][7]:
                countschemlist=countschemlist+1

                entity1 = remove_non_ascii_and_line_break(str(currentRelations[relation_id][0]))
                relation = remove_non_ascii_and_line_break(str(currentRelations[relation_id][1]))
                entity2 = remove_non_ascii_and_line_break(str(currentRelations[relation_id][2]))
                relationsection = remove_non_ascii_and_line_break(str(use_section[0]))
                relationurl = wwwurl
                relationtext = remove_non_ascii_and_line_break(str(currentRelations[relation_id][5]))
                urlid = currentRelations[relation_id][3]
                sentenceid = currentRelations[relation_id][4]
                relationid = currentRelations[relation_id][7]
                POSinfo = currentRelations[relation_id][6]
                sectiontype = use_section[2]

                schema_list.append((entity1,relation,entity2,relationsection,relationurl,relationtext,urlid,sentenceid,relationid,POSinfo,sectiontype,countschemlist))



        schema_list = list(set(schema_list))
        print(len(schema_list))
        schema_list.sort(key=lambda tup:tup[10])
        #write into database
        # write into text file
        for each_line in schema_list:
            all_schema_list.append(each_line)
            file_keyPhrase.write(each_line[0]+'\t\t'+each_line[1]+'\t\t'+each_line[2]+'\t\t'+each_line[3]+'\t\t'+each_line[4]+'\t\t'+each_line[5]+'\t\t'+each_line[6]+'\t\t'+each_line[7]+'\t\t'+each_line[8]+'\t\t'+each_line[9]+'\t\t'+each_line[10])
            file_keyPhrase.write('\n')

    file_keyPhrase.close()
    file_filenamelist.close()
    print(time.strftime("%H:%M:%S"))


    return  all_schema_list






    # operate mysql database
def generate_data(schema_list):

    conn = pymysql.connect(host='localhost', port=3306, user='root',passwd='root', db='AndroidGuideAPI')

    cur = conn.cursor()
    cur.execute("delete from EntitiesRelation")
    sqli = "insert into EntitiesRelation values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for i, one_schema in enumerate(schema_list):
        if len(one_schema[0])>999 or len(one_schema[2])>999:
            continue
        if len(one_schema[3])>999 or len(one_schema[4])>999 or len(one_schema[5])>2999 or len(one_schema[9])>999:
            continue
        cur.execute(sqli, (i + 1, one_schema[0], one_schema[1], one_schema[2], one_schema[3], one_schema[4], one_schema[5], one_schema[6], one_schema[7], one_schema[8], one_schema[9], one_schema[10]))
    cur.close()
    conn.commit()
    conn.close()
    return



# select the triple from file
def triple_selection_fromfile():

    file_key_phrase = open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out_ascii.txt')


    #allrelaton  example:  "(t1,t2,...)"
    #('Android', 'runs on', 'billions', 'Build for a Multi-Screen World', 'https://developer.android.com/index.html', 'Android runs on billions of handheld devices around the world, and it now supports these exciting, new form-factors. ', '1', '1_10', '1_10_1', 'NNP VBZ IN NNS', 'h1')

    schema_list = []
    for one_phrase in file_key_phrase:
        one_phrase=one_phrase.lstrip('(').lstrip('\'').rstrip('\n').strip().rstrip(')').rstrip('\'')
        groupphrase=one_phrase.split('\', \'')

        if len(groupphrase)<11 :
            print("wrong number of elements")
            print(groupphrase)
        entity1 = groupphrase[0]
        relation = groupphrase[1]
        entity2 = groupphrase[2]

        relationsection = groupphrase[3]
        relationurl = groupphrase[4]
        relationtext = groupphrase[5]
        urlid = groupphrase[6]
        sentenceid = groupphrase[7]
        relationid = groupphrase[8]
        if not (sentenceid.replace('_','')).isdigit():
            print(sentenceid)
            print(groupphrase)
        POSinfo = groupphrase[9]
        sectiontype = groupphrase[10]
        schema_list.append((entity1,relation,entity2,relationsection,relationurl,relationtext,urlid,sentenceid,relationid,POSinfo,sectiontype))

    file_key_phrase.close()

    print(len(schema_list))
    return schema_list



#running
#check and write to file
#checkAnyRelationToSection()
schema_list = checkAnyRelationToSection()

#read from file
#schema_list = triple_selection_fromfile()

#write database
generate_data(schema_list)
