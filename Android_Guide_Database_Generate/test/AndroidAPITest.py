import re
from urllib.parse import urljoin


import bs4
import os
import os.path
from urllib.request import urlopen



try:
    from BeautifulSoup import BeautiulSoup
except ImportError:
    from bs4 import BeautifulSoup, NavigableString

data_path=os.pardir+"/tempdata"
# print(data_path)



def strip_tags(soup, invalid_tags):

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(str(c), invalid_tags)
                s += str(c)

            tag.replaceWith(s)

    return soup


sentencewordscount=1
taglength=100

writeid = 1
id=1



a1re = re.compile(r'\(.*?\)')
a2re = re.compile(r'\{.*?\}')
#a3re = re.compile(r'\[.*?\]')
a4re = re.compile(r'\n+')
a5re = re.compile(r'\s+')

# a1re = re.compile(r'\(.*?\)')
# a2re = re.compile(r'\{.*?\}')
#a3re = re.compile(r'\[.*?\]')


alinebreakre = re.compile(r'\n+')
ablankre = re.compile(r'\s+')
adotre = re.compile(r'\.+')
atabre=re.compile(r'\t+')



#
# with open('/Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com/reference/android/view/SurfaceView.html', 'r',encoding='utf-8') as fhtml:
#     html_code = fhtml.read()
    # test filename='/Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com/reference/android/view/SurfaceView.html'


# page=urlopen('https://developer.android.com/reference/android/view/SurfaceView.html').read()


# page=urlopen('file:///Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com/reference/android/view/SurfaceView.html').read()

filenames='file:///Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com/training/index.html'

# test file name list:
#  https://developer.android.com/training/basics/intents/sending.html
# file:///Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com/training/index.html
# file:///Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com/reference/android/view/SurfaceView.html

# page=urlopen('https://developer.android.com/training/basics/intents/sending.html').read()

filenames='/Users/Grand/Downloads/sitesucker/guideAPI/developer.android.com/training/basics/intents/sending.html'

page=open(filenames,'r',encoding='utf-8')


# BeautifulSoup can use different parsers to handle HTML input.The HTML input  here is a little broken, and the default HTMLParser parser doesn't handle it very well.
#
# Use the html5lib parser instead:
#
# >> > len(BeautifulSoup(r.text, 'html').find('td', attrs={'class': 'eelantext'}).find_all('p'))
# 0
# >> > len(BeautifulSoup(r.text, 'lxml').find('td', attrs={'class': 'eelantext'}).find_all('p'))
# 0
# >> > len(BeautifulSoup(r.text, 'html5lib').find('td', attrs={'class': 'eelantext'}).find_all('p'))
# 22

# soup = BeautifulSoup(page, "html.parser")
# fhtml.close()
soup = BeautifulSoup(page,"html5lib")







# try:
if soup.body is not None:
    if soup.find('div',{"class":"jd-descr","itemprop":"articleBody"}) is not None:
        the_contents_of_body=soup.find('div',{"class":"jd-descr","itemprop":"articleBody"})
    elif soup.find(attrs={"id": "body-content"}) is not None:
        the_contents_of_body=soup.find(attrs={"id": "body-content"})
    else:
        the_contents_of_body = soup.find('body', {"class": "gc-documentation"})
else:
    the_contents_of_body=soup.find(attrs={"id": "body-content"})
    if the_contents_of_body is None:
        the_contents_of_body = soup.find(attrs={"itemprop": "articleBody"})
        if the_contents_of_body is None:
            # <div class="wrap clearfix" id="body-content">
            the_contents_of_body = soup.find('body', {"class": "gc-documentation"})

# 清除换行符

print(the_contents_of_body)




the_contents_of_body_without_body_tags = ''.join(['%s' % x for x in the_contents_of_body.contents])
# print('==========================\n')

# print(str(the_contents_of_body_without_body_tags))


# linestext=''.join([ '%s' % x for x in the_contents_of_body_without_body_tags])
# linestext = the_contents_of_body.prettify()
linestostring=the_contents_of_body_without_body_tags


lineslist = linestostring.splitlines(False)
i = 0
while i < len(lineslist):
    lineslist[i] = lineslist[i].strip()
    i += 1
linestostring = ''.join(lineslist)





#准备内容 写入准备数据文件
content = str(writeid) +"," + linestostring

print(writeid)
print(content)

taglist=[]
fulltaginfolist=[]



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
        temptext = str("".join(header)).strip()
        if temptext is "":
            continue
        if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
            taglist.append("".join(temptext))

    # for h2
    for res in h2content:
        header = res.find_all(text=True)
        temptext = str("".join(header)).strip()
        if temptext is "":
            continue
        if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
            taglist.append("".join(temptext))

    # for h3
    for res in h3content:
        header = res.find_all(text=True)
        temptext = str("".join(header)).strip()
        if temptext is "":
            continue
        if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
            taglist.append("".join(temptext))

    # for h4
    for res in h4content:
        header = res.find_all(text=True)
        temptext = str("".join(header)).strip()
        if temptext is "":
            continue
        if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
            taglist.append("".join(temptext))

    # for h5
    for res in h5content:
        header = res.find_all(text=True)
        temptext = str("".join(header)).strip()
        if temptext is "":
            continue
        if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
            taglist.append("".join(temptext))

    # for h6
    for res in h6content:
        header = res.find_all(text=True)
        temptext = str("".join(header)).strip()
        if temptext is "":
            continue
        if (temptext.strip() is not "") and (len(temptext.strip()) < taglength):
            taglist.append("".join(temptext))

    alist = the_contents_of_body.findAll('a', {'href': True})
    if alist is not None:
        for x in alist:
            tempatext = str("".join(x.find_all(text=True))).strip()
            alink = x.get("href").strip()

            # 去除（）及里面内容
            if tempatext is not None:
                tempatext = a1re.sub('', tempatext)
                tempatext = a2re.sub('', tempatext)
                # tempatext = a3re.sub('', tempatext)
                tempatext = adotre.sub('.', tempatext)
                tempatext = tempatext.replace('.', ' ')
                tempatext = alinebreakre.sub(' ', tempatext)
                tempatext = ablankre.sub(' ', tempatext)
                # 对于tag考虑长度限制  目前限制48
                if (tempatext.strip() is not "") and (len(tempatext.strip()) < taglength):
                    taglist.append(tempatext)
                    if alink is not None:
                        if alink is not "":
                            fulltaginfolist.append(
                                tempatext + ',' + filenames + ',' + urljoin('https://developer.android.com/', alink))

    # 每个网页中得到的tag清除重复link
    fulltaginfolist = list(set(fulltaginfolist))
    print(fulltaginfolist)

    # 每个网页中得到的tag去重复的keywords
    taglist = list(set(taglist))
    print(taglist)

    # parepare text
    # delete example code in pages
    [x.extract() for x in the_contents_of_body.findAll('pre')]

    # < style type = "text/css" >
    [x.extract() for x in the_contents_of_body.findAll('style', {"type": "text/css"})]

    text = (' '.join(the_contents_of_body.findAll(text=True)).strip())


    #保留 短线 ，150； 破折号 ， 151,

    # 清除非ASCII符号
    text = ''.join([i if (ord(i) > 150 or  ord(i)< 151 or ord(i)<128)  else ' ' for i in text])
    # dirty = text
    #
    # temptext = re.sub(r'[\0\200-\377]', '', dirty)



    text = text.replace('you’re', 'you are').replace('What’s ', 'What is').replace('it’s', 'It is').replace('It’s',
                                                                                                            'It is')


    text = atabre.sub(' ', text)
    text = ablankre.sub(' ', text)

    print(str(id) + '\t' + text)


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
                theline = (('%s_%s\t%s') % (str(id).strip(), str(sentencecount).strip(), qsentencs.strip()))
                if (qn + 1 == qlen):
                    if qsentencs.strip() is not "":
                        theline = theline + '.'
                        theline = theline.replace('..', '.')
                        sentencecount += 1
                        print(theline)

                else:
                    theline = theline + '?'
                    sentencecount += 1
                    print(theline)

        else:
            if onesentence.strip() is not "":
                theline = (('%s_%s\t%s%s') % (str(id).strip(), str(sentencecount).strip(), onesentence.strip(), '.'))
                # print(theline)
                theline = theline.replace('..', '.')
                sentencecount += 1
                print(theline)



# print(linestostring)

writeid += 1

# except:
#     pass

# three line for temp comments
