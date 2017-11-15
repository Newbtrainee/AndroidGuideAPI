# coding:utf-8
from functools import cmp_to_key

from selenium import webdriver
import pymysql
import pymysql.cursors
import re

# extract data using webdriver
def start():
    executable_path = '/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs'  # phantomjs engine, used as browser
    # /usr/local/Cellar/phantomjs/2.1.1
    driver = webdriver.PhantomJS(executable_path=executable_path)
    # driver = webdriver.Firefox()   # can use firefox or other brower as well
    extract_ele(driver)
    return

# extract by xpath
def extract_ele(driver):
    file_keyPhrase = open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out.txt', 'w')
    file_filenamelist = open('/Users/Grand/Downloads/HDSKG/tempdata/filenamelist.csv')



    for one_line in file_filenamelist:
        one_line=one_line.rstrip('\n').rstrip('\r')
        # all_url.remove('')



        urlsplit=one_line.split(',')
        url_id = urlsplit[0]
        print("processing file :"+one_line)
        # goal_website = (one_url.split('/guideAPI/')[1]).strip('\n')
        goal_website = (''.join(urlsplit[1:])).strip('\n')
        # goal_website = 'developer.android.com/training/accessibility/accessible-app.html'
        # driver.get('https://' + goal_website)
        driver.get( goal_website)

        basic_xpath = '//*[@id="body-content"]/div[2]'
        basic_headerpath = '//*[@id="body-content"]/div[1]'


        findtext = driver.find_elements_by_xpath('//*[@id="body-content"]/div[1]')
        if findtext is not None:
            basic_xpath = '//*[@id="body-content"]/div[2]'
            basic_headerpath = '//*[@id="body-content"]/div[1]'
        else :
            findtext = driver.find_elements_by_xpath('//*[@itemprop="articleBody"]/div[1]')
            if findtext is not None:
                basic_xpath = '//*[@itemprop="articleBody"]/div[2]'
                basic_headerpath = '//*[@itemprop="articleBody"]/div[1]'
            else:
                findtext = driver.find_elements_by_xpath('//*[@class="gc-documentation"]/div[1]')
                if findtext is not None:
                    basic_xpath = '//*[@class="gc-documentation"]/div[2]'
                    basic_headerpath = '//*[@class="gc-documentation"]/div[1]'
                else:
                    continue


        header_list = []
        api_list = []
        header_h1 = driver.find_elements_by_xpath(basic_headerpath+'/h1')
        if header_h1 != [] and header_h1[0].text != '':
            header_list.append((header_h1[0].text, 0, 'h1'))
            # (header's name, its sequence mark, type)
            # sequence mark is for confirming api belongs to which section
        else:
            header_list.append(('unknow header1', 0, 'h1'))
            # some webs do not have h1 or the xpath is wrong

        # count the total num of p, h2, h3 for loop later
        para_last_sibling = driver.find_elements_by_xpath(basic_xpath + '/p[last()]/preceding-sibling::p | ' +basic_xpath + '/p[last()]')

        para_total_count = len(para_last_sibling)

        h2_last_sibling = driver.find_elements_by_xpath(basic_xpath + '/h2[last()]/preceding-sibling::h2 | ' +basic_xpath + '/h2[last()]')

        h2_total_count = len(h2_last_sibling)

        h3_last_sibling = driver.find_elements_by_xpath(basic_xpath + '/h3[last()]/preceding-sibling::h3 | ' +basic_xpath + '/h3[last()]')

        h3_total_count = len(h3_last_sibling)

        print("paras:"+para_total_count, "h2 count:"+h2_total_count,"h3 count:"+ h3_total_count)

        for i in range(1, para_total_count + 1):
            api_code = driver.find_elements_by_xpath(basic_xpath + '/p[' + str(i) + ']//code')
            for one_api in api_code:
                if one_api.text != '':
                    api_list.append((one_api.text, i - 1))          # i - 1 is sequence mark

        for i in range(1, h2_total_count + 1):
            header_h2 = driver.find_element_by_xpath(basic_xpath + '/h2[position() = ' + str(i) + ']')
            if header_h2.text != '':
                sibling_h2 = driver.find_elements_by_xpath(basic_xpath + '/h2[position() = '
                                                           + str(i) + ']/preceding-sibling::p')
                position_h2 = len(sibling_h2)           # this is how sequence mark comes from,
                # use num of preceding-sibling p tags
                header_list.append((header_h2.text, position_h2, 'h2'))

        for i in range(1, h3_total_count + 1):
            header_h3 = driver.find_element_by_xpath(basic_xpath + '/h3[position() = ' + str(i) + ']')
            if header_h3.text != '':
                sibling_h3 = driver.find_elements_by_xpath(basic_xpath + '/h3[position() = '
                                                           + str(i) + ']/preceding-sibling::p')
                position_h3 = len(sibling_h3)
                header_list.append((header_h3.text, position_h3, 'h3'))

        #python 3  there no "cmp" parameter for sort
        header_list.sort(key=takeListSecond)

        print(len(header_list))
        print(len(api_list))
        for one_api in api_list:
            file_keyPhrase.write(url_id + ', ')
            file_keyPhrase.write(one_api[0] + ', ')
            write_flag = 0
            for i, one_header in enumerate(header_list):
                # find api's section based on sequence mark
                if one_api[1] < one_header[1]:
                    file_keyPhrase.write(header_list[i - 1][0] + ', ')
                    write_flag = 1
                    break
            if not write_flag:
                file_keyPhrase.write(header_list[-1][0] + ', ')
            file_keyPhrase.write('https://' + goal_website.replace('/Users/Grand/Downloads/sitesucker/guideAPI/','') + '\n')

            # break

    file_keyPhrase.close()
    file_filenamelist.close()
    return



def takeListSecond(elem):
    return elem[1]


# compare_exact_string
def c_e_s(checkword, checkString):
    ablankre = re.compile(r'\s+')
    checkString=ablankre.sub(' ',checkString)
    checkword = ablankre.sub(' ', checkword)
    str1list = checkword.split()
    str2list = checkString.split()
    flag = True
    for word in str1list:
        if word not in str2list:
            flag = False
            break;
    return flag

# select the triple
def triple_selection():
    file_triple = open('/Users/Grand/Downloads/HDSKG/tempdata/androidAPIallCand5_ascii.txt')
    file_key_phrase = open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out.txt')
    file_allsentence = open('/Users/Grand/Downloads/HDSKG/tempdata/AndroidAPI_allSent_ascii.txt')

    #allSent example:  "id \t text"
    #11352_27	Go further to support business use of your app by enabling restrictions that administrators can use to remotely configure your app: Manage Devices and Apps.


    dict_allsentence={}

    for line in file_allsentence:
        data=re.split(r'\t+', line.rstrip('\t').rstrip('\r').rstrip('\n'))
        if len(data)==2:
            key,value=data[0],data[1]
            dict_allsentence[key]=value

    phrase_list = []
    section_list = []
    url_list = []
    p_uid_list = []
    for one_phrase in file_key_phrase:
        phrase_u_id = one_phrase.split(', ')[0]
        pure_phrase = one_phrase.split(', ')[1].split('(')[0]
        pure_phrase = pure_phrase.replace('$', r'\$').replace('*', r'\*').replace('+', r'\+').replace('.', r'\.') \
            .replace('[', r'\[').replace(']', r'\]').replace('?', r'\?').replace('|', r'\|').replace('\'', r'\'') \
            .replace('\"', r'\"')
        p_uid_list.append(phrase_u_id)
        pure_section = one_phrase.split(', ')[2]
        pure_url = one_phrase.strip('\r\n').split(', ')[3]
        phrase_list.append(pure_phrase)
        section_list.append(pure_section)
        url_list.append(pure_url)


    schema_list = []
    for j, one_triple in enumerate(file_triple):

        if type(one_triple) is str or type(one_triple) is bytes:
            #Python 3 renamed the unicode type to str, the old str type has been replaced by bytes
            one_triple = eval(one_triple.strip('\n'))

        #all triple example:
        #{'subject_ori': 'administrators', 'relation_ori': 'configure', 'object_ori': 'app', 'subject': 'administrators', 'relation': 'configure', 'object': 'app', 'subject_stand': 'administrator', 'relation_stand': 'configure', 'object_stand': 'app', 'start_index': 14, 'end_index': 21, 'originalSent_len': 27, 'pos': 'NNS VB NN', 'relationType': 'NonTaxo', 'rel_id': '11352_27_1'}

        entity1 = one_triple['subject_ori']
        relation = one_triple['relation_ori']
        entity2 = one_triple['object_ori']
        entity_url_id = one_triple['rel_id'].split('_')[0]

        sentence_id=one_triple['rel_id'].rsplit('_',1)[0]
        sentence_text=dict_allsentence[sentence_id]

        relation_id=one_triple['rel_id']


        # print entity1, relation, entity2

        for i, one_phrase in enumerate(phrase_list):
            #移除非ASCII符号
            one_phrase=''.join([i if (ord(i) < 128) and (i is not '\n') else ' ' for i in one_phrase])
            if entity_url_id == p_uid_list[i] and (c_e_s(one_phrase,entity1) or c_e_s(one_phrase,entity2)):
                section = section_list[i]
                url = url_list[i]
                schema_list.append((entity1, relation, entity2, section, url, sentence_text,entity_url_id,sentence_id,relation_id))
                # print(entity_url_id)
                print(p_uid_list[i])
                # print (entity1, relation, entity2, section, url,sentence_text,entity_url_id,sentence_id,relation_id)
                print(one_phrase)
                break

    file_key_phrase.close()
    file_triple.close()


    # print(schema_list)
    # remove duplicates
    schema_list=list(set(schema_list))

    print(len(schema_list))
    return schema_list





# operate mysql database
def generate_data():
    conn = pymysql.connect(host='localhost', port=3306, user='root',passwd='root', db='AndroidGuideAPI')
    cur = conn.cursor()
    cur.execute("delete from EntitiesRelation")
    schema_list = triple_selection()
    sqli = "insert into EntitiesRelation values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for i, one_schema in enumerate(schema_list):
        cur.execute(sqli, (i + 1, one_schema[0], one_schema[1], one_schema[2], one_schema[3], one_schema[4], one_schema[5], one_schema[6], one_schema[7], one_schema[8]))
    cur.close()
    conn.commit()
    conn.close()
    return





# === start programer ====
start()

#triple_selection()

generate_data()