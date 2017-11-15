import re
from urllib.parse import urljoin

import bs4
import os
import os.path

try:
    from BeautifulSoup import BeautiulSoup
except ImportError:
    from bs4 import BeautifulSoup, NavigableString


    # 获取指定目录下的所有文件


def getfilenamelist(mypath):
    filesNamelist = []
    for root, dirs, files in os.walk(mypath):
        for name in files:
            # 使用的文件类型可以在这里列举
            for ext in ['.html']:
                if name.endswith(ext):
                    filesNamelist.append(root + '/' + name)
    return filesNamelist


# end the function getfilenamelist




data_path=os.pardir+"/tempdata"
# print(data_path)

# two line for temp comments

# prefcsv=open(data_path+'/androidAPIinput1.csv','w', encoding='utf-8')

fmytag=open(data_path+'/androidAPI_id_tag.csv','w',encoding='utf-8')
ffulltaginfo=open(data_path+'/androidAPI_id_tag_full_info.csv','w',encoding='utf-8')

filenamefile=open(data_path+'/filenamelist.csv')

# 读取所有html文件的文件名，放置在一个list中
mypath = '/Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com'
currenturl='https://developer.android.com'


# one line for temp comments

taglength=100

taglist = []
fulltaginfolist = []

filenumber = 0
writeid = 1

a1re = re.compile(r'\(.*?\)')
a2re = re.compile(r'\{.*?\}')

a4re = re.compile(r'\n+')
a5re = re.compile(r'\s+')

alinebreakre = re.compile(r'\n+')
ablankre = re.compile(r'\s+')
adotre = re.compile(r'\.+')
atabre=re.compile(r'\t+')
totalfiles=len(filesNamelist)
print(totalfiles)

while filenumber < len(filesNamelist):
# while filenumber < 200:
    currentfilename=filesNamelist[filenumber]
    thecurrentflename = urljoin(currenturl,currentfilename.replace(mypath, ""))
    # print(currentfilename)
    # print(thecurrentflename)

    with open(currentfilename, 'r',encoding='utf-8') as fhtml:
        html_code = fhtml.read()
        # test filename='/Users/Grand/Downloads/HDSKG/tagwiki_dataPreProcess/index.html'

    print(filesNamelist[filenumber])
    soup = BeautifulSoup(html_code, "html5lib")
    fhtml.close()


    filenumber += 1


    # 只处理处理英文网页或为标定语言的网页
    # <html lang="en">
    # ANDROID_LANGUAGES = [
    #       'id','de','en','es','es-419','fr','pt-br','vi','tr','ru','th','ja','zh-cn','zh-tw','ko'
    #   ];

    root = soup.html.get('lang')
    if root is not None:
        if 'id' in root:
            continue
        if 'de' in root:
            continue
        if 'es' in root:
            continue
        if 'es-419' in root:
            continue
        if 'fr' in root:
            continue
        if 'pt-br' in root:
            continue
        if 'vi' in root:
            continue
        if 'tr' in root:
            continue
        if 'ru' in root:
            continue
        if 'th' in root:
            continue
        if 'ja' in root:
            continue
        if 'zh-cn' in root:
            continue
        if 'zh-tw' in root:
            continue
        if 'ko' in root:
            continue

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

    #
    # # <div class="dac-toast-group">
    # [s.extract() for s in soup.findAll('div',{"class":"dac-toast-group"})]
    #
    # # <div class="dac-modal" data-modal="api-unavailable" id="api-unavailable">
    # [s.extract() for s in soup.findAll('div',{"class":"dac-modal"})]
    #
    # # <div id="survey-box-wrapper">
    # [s.extract() for s in soup.findAll('div',{"id":"survey-box-wrapper"})]

    # # < li class ="nav-section" >
    # [s.extract() for s in soup.findAll('li',{"class":"nav-section"})]



    # # < footer class ="dac-footer " >
    # [s.extract() for s in soup.findAll('footer',{"class":"dac-footer"})]

    # comments of this html file
    for element in soup(text=lambda text: isinstance(text, bs4.element.Comment)):
        element.extract()

    # cc=soup.findAll('div',{"class":"api apilevel-1"})
    # print(cc)
    # pc=soup.findAll('p')
    # print(pc)


    # for h1
    for res in soup.findAll('h1'):
        res.append('. ')
    # for h2
    for res in soup.findAll('h2'):
        res.append('. ')
    # for h3
    for res in soup.findAll('h3'):
        res.append('. ')
    # for h4
    for res in soup.findAll('h4'):
        res.append('. ')
    # for h5
    for res in soup.findAll('h5'):
        res.append('. ')
    # for h6
    for res in soup.findAll('h6'):
        res.append('. ')

    # for th
    for res in soup.findAll('th'):
        res.append('. ')

    # for tr
    for res in soup.findAll('tr'):
        res.append('. ')

    # #for ul
    for res in soup.findAll('ul'):
        res.insert(0, NavigableString('. '))
    for res in soup.findAll('ul'):
        res.append('. ')

    # remove strong tag's  last '.'    string.replace(' and ', ", ", (string.count(' and ')-1))
    for res in soup.findAll('strong'):
        res.replace_with((''.join(str(res.contents).rsplit('.', 1))).lstrip('[').rstrip(']').strip('\''))

    try:
        if soup.body is not None:
            if soup.find('div', {"class": "jd-descr", "itemprop": "articleBody"}) is not None:
                the_contents_of_body = soup.find('div', {"class": "jd-descr", "itemprop": "articleBody"})
            elif soup.find(attrs={"id": "body-content"}) is not None:
                the_contents_of_body = soup.find(attrs={"id": "body-content"})
            else:
                the_contents_of_body = soup.find('body', {"class": "gc-documentation"})
        else:
            the_contents_of_body = soup.find(attrs={"id": "body-content"})
            if the_contents_of_body is None:
                the_contents_of_body = soup.find(attrs={"itemprop": "articleBody"})
                if the_contents_of_body is None:
                    # <div class="wrap clearfix" id="body-content">
                    the_contents_of_body = soup.find('body', {"class": "gc-documentation"})

        # 清除换行符
        linestostring = ''.join(['%s' % x for x in the_contents_of_body.contents])

        # linestext=' '.join([ '%s' % x for x in the_contents_of_body_without_body_tags.contents])
        lineslist = linestostring.splitlines(False)
        i = 0
        while i < len(lineslist):
            lineslist[i] = lineslist[i].strip()
            i += 1
        linestostring = ''.join(lineslist)
        # print(linestostring)


        if "Sorry, the page you seek does not belong to Android." in linestostring:
            continue
        if "How developers are finding success with Android and Google Play." in linestostring:
            continue




        #准备内容 写入准备数据文件
        content = str(writeid) + ","+thecurrentflename+"," + linestostring
        acontent= str(writeid) +"," + linestostring
        filenamesorder=str(writeid)+","+currentfilename
        print(writeid,"/",totalfiles)

        # print(linestostring)

        # six line for temp comments
        # prefcsv.write(acontent.strip())
        # prefcsv.write('\r')
        fcsv.write(content.strip())
        fcsv.write('\r')
        filenamefile.write(filenamesorder)
        filenamefile.write('\r')





        if the_contents_of_body is not None:

            # 抽取 tag (标题和方法名)
            h1content = the_contents_of_body.findAll('h1')
            h2content = the_contents_of_body.findAll('h2')
            h3content = the_contents_of_body.findAll('h3')
            h4content = the_contents_of_body.findAll('h4')
            h5content = the_contents_of_body.findAll('h5')
            h6content = the_contents_of_body.findAll('h6')

            # for h1
            for res in h1content:
                header = res.find_all(text=True)
                temptext = str("".join(header)).strip().rstrip('.')
                if temptext is "":
                    continue
                if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
                    temptext=alinebreakre.sub(' ',temptext)
                    taglist.append("".join(temptext))
                    fulltaginfolist.append("".join(temptext) + ',' + currentfilename + ',' + 'h1')

            # for h2
            for res in h2content:
                header = res.find_all(text=True)
                temptext = str("".join(header)).strip().rstrip('.')
                if temptext is "":
                    continue
                if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
                    temptext = alinebreakre.sub(' ', temptext)
                    taglist.append("".join(temptext))
                    fulltaginfolist.append("".join(temptext) + ',' + currentfilename + ',' + 'h2')

            # for h3
            for res in h3content:
                header = res.find_all(text=True)
                temptext = str("".join(header)).strip().rstrip('.')
                if temptext is "":
                    continue
                if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
                    temptext = alinebreakre.sub(' ', temptext)
                    taglist.append("".join(temptext))
                    fulltaginfolist.append("".join(temptext) + ',' + currentfilename + ',' + 'h3')

            # for h4
            for res in h4content:
                header = res.find_all(text=True)
                temptext = str("".join(header)).strip().rstrip('.')
                if temptext is "":
                    continue
                if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
                    temptext = alinebreakre.sub(' ', temptext)
                    taglist.append("".join(temptext))
                    fulltaginfolist.append("".join(temptext) + ',' + currentfilename + ',' + 'h4')

            # for h5
            for res in h5content:
                header = res.find_all(text=True)
                temptext = str("".join(header)).strip().rstrip('.')
                if temptext is "":
                    continue
                if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
                    temptext = alinebreakre.sub(' ', temptext)
                    taglist.append("".join(temptext))
                    fulltaginfolist.append("".join(temptext) + ',' + currentfilename + ',' + 'h5')

            # for h6
            for res in h6content:
                header = res.find_all(text=True)
                temptext = str("".join(header)).strip().rstrip('.')
                if temptext is "":
                    continue
                if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
                    temptext = alinebreakre.sub(' ', temptext)
                    taglist.append("".join(temptext))
                    fulltaginfolist.append("".join(temptext) + ',' + currentfilename + ',' + 'h6')

            alist = the_contents_of_body.findAll('a', {'href': True})
            if alist is not None:
                for x in alist:
                    tempatext = str("".join(x.find_all(text=True))).strip().rstrip('.')
                    alink = x.get("href").strip()

                    # 去除（）及里面内容
                    if tempatext is not None:
                        tempatext = a1re.sub('', tempatext)
                        tempatext = a2re.sub('', tempatext)

                        tempatext = adotre.sub('.', tempatext)

                        tempatext = alinebreakre.sub(' ', tempatext)
                        tempatext = ablankre.sub(' ', tempatext)
                        tempatext=tempatext.strip().rstrip('.')
                        # 对于tag考虑长度限制  目前限制100
                        if (tempatext.strip() is not "") and (len(tempatext.strip()) < taglength):
                            taglist.append(tempatext)
                            if alink is not None:
                                if alink is not "":
                                    fulltaginfolist.append(
                                        tempatext + ',' + currentfilename + ',' + urljoin(currenturl,alink))

            # 每个网页中得到的tag清除重复link
            fulltaginfolist = list(set(fulltaginfolist))
            # print(fulltaginfolist)

            # 每个网页中得到的tag去重复的keywords
            taglist = list(set(taglist))
            # print(taglist)

            # parepare text
            # delete example code in pages
            [x.extract() for x in the_contents_of_body.findAll('pre')]

            # < style type = "text/css" >
            [x.extract() for x in the_contents_of_body.findAll('style', {"type": "text/css"})]

            text = (' '.join(the_contents_of_body.findAll(text=True)).strip())

            # 保留 短线 ，150； 破折号 ， 151,

            # 清除非ASCII符号
            text = ''.join([i if (ord(i) > 150 or ord(i) < 151 or ord(i) < 128)  else ' ' for i in text])
            # dirty = text
            #
            # temptext = re.sub(r'[\0\200-\377]', '', dirty)



            text = text.replace('you’re', 'you are').replace('What’s ', 'What is').replace('it’s', 'It is').replace('It’s','It is')

            text = atabre.sub(' ', text)
            text = ablankre.sub(' ', text)

            file_w_allDoc.write(str(writeid) + '\t' + text)
            file_w_allDoc.write('\n')

            text = text.replace(' .', '. ')
            # split: '. ' then split '? '
            allsentences = text.split('. ')
            sentencecount = 0
            # print(allsentences)

            for senidex, onesentence in enumerate(allsentences):

                # onesentence = onesentence.replace(':', ' ')
                onesentencelist = onesentence.split(' ')
                onesentencslen = len(onesentencelist)
                if onesentence.strip('.').strip() in "In this document":
                    continue

                if (onesentencslen < sentencewordscount):
                    continue

                if '?' in onesentence:
                    newones = onesentence.split('?')
                    qlen = len(newones)
                    for qn, qsentencs in enumerate(newones):
                        qlist = qsentencs.split(' ')
                        qsentencslen = len(qlist)

                        if qsentencs.strip('.').strip() in "In this document":
                            continue

                        if (qsentencslen < sentencewordscount):
                            continue
                        theline = (('%s_%s\t%s') % (str(writeid).strip(), str(sentencecount).strip(), qsentencs.strip()))
                        if (qn + 1 == qlen):
                            if qsentencs.strip() is not "":
                                theline = theline + '.'
                                theline = theline.replace('..', '.')
                                sentencecount += 1
                                file_w_allSent.write(theline)
                                file_w_allSent.write('\n')


                        else:
                            theline = theline + '?'
                            sentencecount += 1
                            file_w_allSent.write(theline)
                            file_w_allSent.write('\n')

                else:
                    if onesentence.strip() is not "":
                        theline = (
                        ('%s_%s\t%s%s') % (str(writeid).strip(), str(sentencecount).strip(), onesentence.strip(), '.'))
                        # print(theline)
                        theline = theline.replace('..', '.')
                        sentencecount += 1
                        file_w_allSent.write(theline)
                        file_w_allSent.write('\n')

            writeid += 1
    except:
        continue

# three line for temp comments
fcsv.close()
# prefcsv.close()
filenamefile.close()
file_w_allDoc.close()
file_w_allSent.close()




#处理抽取的tag
print("doing each keywords")
#去重复的keywords
taglist=list(set(taglist))

#写入my_id_tag
tagid=1
tagkeywords=""
for srings in taglist:
    print("tagid:" + str(tagid))
    tagkeywords = str(tagid) + "," + srings
    fmytag.write(tagkeywords.strip())
    fmytag.write('\r')
    tagid += 1
fmytag.close()

#去重复的keywords
fulltaginfolist=list(set(fulltaginfolist))

#写入my_id_tag
tagid=1
tagkeywordslink=""
for srings in fulltaginfolist:
    print("link tagid:" + str(tagid))
    tagkeywordslink = str(tagid) + "," + srings
    ffulltaginfo.write(tagkeywordslink.strip())
    ffulltaginfo.write('\r')
    tagid += 1
ffulltaginfo.close()