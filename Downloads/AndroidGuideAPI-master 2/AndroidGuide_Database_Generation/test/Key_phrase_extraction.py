# coding:utf-8
from functools import cmp_to_key

from selenium import webdriver
import pymysql
import pymysql.cursors
import re

# extract data using webdriver
def start():
    executable_path = ' /usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs'  # phantomjs engine, used as browser
    # /usr/local/Cellar/phantomjs/2.1.1
    driver = webdriver.PhantomJS(executable_path=executable_path)
    # driver = webdriver.Firefox()   # can use firefox or other brower as well
    extract_ele(driver)


# extract by xpath
def extract_ele(driver):
    file_w = open('./../DataAndResultFromAndroid/key_phrase/text_out.txt', 'w')
    file_r = open('./../DataAndResultFromAndroid/key_phrase/filenamelist_training.csv')

    for one_line in file_r:
        all_url = one_line.split('\r')
        all_url.remove('')

        for one_url in all_url:
            url_id = one_url.split(',')[0]
            goal_website = one_url.split('/guideAPI/')[1]
            # goal_website = 'developer.android.com/training/accessibility/accessible-app.html'
            driver.get('https://' + goal_website)

            basic_xpath = '//*[@id="body-content"]/div[2]'

            header_list = []
            api_list = []
            header_h1 = driver.find_elements_by_xpath('//*[@id="body-content"]/div[1]/h1')
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

            print(para_total_count, h2_total_count, h3_total_count)

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

            key = cmp_to_key(lambda x, y: x[1] - y[1])
            header_list = sorted(header_list, cmp=key)
            print(header_list)
            print(api_list)
            for one_api in api_list:
                file_w.write(url_id + ', ')
                file_w.write(one_api[0].encode('ascii', 'ignore') + ', ')
                write_flag = 0
                for i, one_header in enumerate(header_list):
                    # find api's section based on sequence mark
                    if one_api[1] < one_header[1]:
                        file_w.write(header_list[i - 1][0] + ', ')
                        write_flag = 1
                        break
                if not write_flag:
                    file_w.write(header_list[-1][0] + ', ')
                file_w.write('https://' + goal_website + '\n')

        break

    file_w.close()
    file_r.close()




# select the triple
def triple_selection():
    file_triple = open('./../DataAndResultFromAndroid/key_phrase/allCand5.txt')
    file_key_phrase = open('./../DataAndResultFromAndroid/key_phrase/text_out.txt')

    phrase_list = []
    section_list = []
    url_list = []
    p_uid_list = []
    for one_phrase in file_key_phrase:
        phrase_u_id = one_phrase.split(', ')[0]
        pure_phrase = one_phrase.split(', ')[1].split('(')[0]
        pure_phrase = pure_phrase.replace('$', r'\$').replace('*', r'\*').replace('+', r'\+').replace('.', r'\.')\
            .replace('[', r'\[').replace(']', r'\]').replace('?', r'\?').replace('|', r'\|').replace('\'', r'\'')\
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


#{'subject_ori': 'administrators', 'relation_ori': 'configure', 'object_ori': 'app', 'subject': 'administrators', 'relation': 'configure', 'object': 'app', 'subject_stand': 'administrator', 'relation_stand': 'configure', 'object_stand': 'app', 'start_index': 14, 'end_index': 21, 'originalSent_len': 27, 'pos': 'NNS VB NN', 'relationType': 'NonTaxo', 'rel_id': '11352_27_1'}

        entity1 = one_triple['subject_ori']
        relation = one_triple['relation_ori']
        entity2 = one_triple['object_ori']
        entity_u_id = one_triple['rel_id'].split('_')[0]
        # print entity1, relation, entity2

        for i, one_phrase in enumerate(phrase_list):
            if entity_u_id == p_uid_list[i] \
                    and (re.search('\\b' + one_phrase + '\\b', entity1) or re.search('\\b' + one_phrase + '\\b', entity2)):
                section = section_list[i]
                url = url_list[i]
                schema_list.append((entity1, relation, entity2, section, url))
                print(entity_u_id)
                print(p_uid_list[i])
                print (entity1, relation, entity2, section, url)
                print(one_phrase)
                break

    file_key_phrase.close()
    file_triple.close()
    print(schema_list)
    print(len(schema_list))
    return schema_list





# operate mysql database
def generate_data():
    conn = pymysql.connect(host='localhost', port=3306, user='lhw', db='AndroidGuideAPI')
    cur = conn.cursor()
    cur.execute("delete from entities")
    schema_list = triple_selection()
    sqli = "insert into entities values(%s,%s,%s,%s,%s,%s)"
    for i, one_schema in enumerate(schema_list):
        cur.execute(sqli, (i + 1, one_schema[0], one_schema[1], one_schema[2], one_schema[3], one_schema[4]))
    cur.close()
    conn.commit()
    conn.close()





# === start programer ====
start()

triple_selection()

generate_data()