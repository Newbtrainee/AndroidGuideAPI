import re
from urllib.parse import urljoin

import bs4
import os
import os.path

try:
    from BeautifulSoup import BeautiulSoup
except ImportError:
    from bs4 import BeautifulSoup



data_path=os.pardir+"/tempdata"
# print(data_path)
fcsv=open(data_path+'/LHWandroidAPIinput.csv','r', encoding='utf-8')
fmytag=open(data_path+'/androidAPI_id_tag.csv','w',encoding='utf-8')
ffulltaginfo=open(data_path+'/androidAPI_id_tag_full_info.csv','w',encoding='utf-8')
file_w_allDoc = open(data_path+'/AndroidAPI_Doc_out.txt','w',encoding='utf-8')
file_w_allSent = open(data_path+'/AndroidAPI_allSent.txt','w',encoding='utf-8')

#对于tag考虑长度限制  目前限制48
taglength=100

taglist=[]
fulltaginfolist=[]

# 读取所有html文件的文件名，放置在一个list中

filenumber = 0
writeid = 1


a1re = re.compile(r'\(.*?\)')
a2re = re.compile(r'\{.*?\}')
#a3re = re.compile(r'\[.*?\]')
alinebreakre = re.compile(r'\n')
ablankre = re.compile(r'\s+')
adotre = re.compile(r'\.+')
atabre=re.compile(r'\t+')


for mi, line in enumerate(fcsv) :


    print(mi)
    mycontents=[]
    mycontents=re.split(',', line)
    id = mycontents[0]
    filenames=mycontents[1]
    onewiki=mycontents[2:]
    onewiki = ','.join(onewiki)

    #replace(' …', '')
    # replace(' ↔', '')
    # replace('’', '\'')
    # replace('®', '')
    # replace('™', '')
    # replace('ü', 'u')
    # replace('“', '\'')
    # replace('”', '\'')
    #  tm C  r  &gt; &lt; &#xA;
    onewiki = onewiki.replace('\,', ',')
    onewiki = onewiki.replace('&gt;', ' ')
    onewiki = onewiki.replace('&lt;', ' ')
    onewiki = onewiki.replace('&#xA;', ' ')
    onewiki = onewiki.replace('|', ' ')
    onewiki = onewiki.replace('…', ' ')
    onewiki = onewiki.replace('↔', ' ')
    onewiki = onewiki.replace('’', ' ')
    onewiki = onewiki.replace('®', '')
    onewiki = onewiki.replace('™', '')
    onewiki = onewiki.replace('ü', ' ')
    onewiki = onewiki.replace('“', '\'')
    onewiki = onewiki.replace('”', '\'')

    # < style >.toggleable {padding: .25em 1em;}.toggleme {padding: 1em 1em 0 2em; line - height: 1 em;}.toggleable a {text - decoration: none;}.toggleable.closed.toggleme {display: none;}  # body-content .toggle-img { margin:0; } </style>
    pattern = '%s(.*?)%s' % (re.escape('<style>'), re.escape('</style>'))
    onewiki = re.sub(pattern, '', onewiki)


    html=BeautifulSoup(onewiki,'html.parser')

    try:

        if html is not None:

            # #由于预处理时忘记给新加的'.'后面添加空格这是专用的代码，只用这一会，以后可以删除
            # # for h1
            # for res in html.findAll('h1'):
            #     res.append(' ')
            # # for h2
            # for res in html.findAll('h2'):
            #     res.append(' ')
            # # for h3
            # for res in html.findAll('h3'):
            #     res.append(' ')
            # # for h4
            # for res in html.findAll('h4'):
            #     res.append(' ')
            # # for h5
            # for res in html.findAll('h5'):
            #     res.append(' ')
            # # for h6
            # for res in html.findAll('h6'):
            #     res.append(' ')
            #
            # # for dt
            # for res in html.findAll('dt'):
            #     res.append(' ')
            # #专用代码结束


            #抽取 tag (标题和方法名)
            h1content = html.findAll('h1')
            h2content = html.findAll('h2')
            h3content = html.findAll('h3')
            h4content = html.findAll('h4')
            h5content = html.findAll('h5')
            h6content = html.findAll('h6')

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

            alist = html.findAll('a', {'href': True})
            if alist is not None:
                for x in alist:
                    tempatext = str("".join(x.find_all(text=True))).strip()
                    alink = x.get("href").strip()

                    # 去除（）及里面内容
                    if tempatext is not None:
                        tempatext = a1re.sub('', tempatext)
                        tempatext = a2re.sub('', tempatext)
                        # tempatext = a3re.sub('', tempatext)
                        tempatext=adotre.sub('', tempatext)
                        tempatext = tempatext.replace('.', ' ')
                        tempatext = alinebreakre.sub(' ', tempatext)
                        tempatext = ablankre.sub(' ', tempatext)
                        #对于tag考虑长度限制  目前限制48
                        if (tempatext.strip() is not "") and (len(tempatext.strip())<taglength) :
                            taglist.append(tempatext)
                            if alink is not None:
                                if alink is not "":
                                    fulltaginfolist.append(tempatext +','+filenames+ ',' +urljoin('https://developer.android.com/',alink))

            #每个网页中得到的tag清除重复link
            fulltaginfolist=list(set(fulltaginfolist))

            #每个网页中得到的tag去重复的keywords
            taglist = list(set(taglist))


            #parepare text
            #delete example code in pages
            [x.extract() for x in html.findAll('pre')]

            #< style type = "text/css" >
            [x.extract() for x in html.findAll('style', {"type": "text/css"})]




            text = (' '.join(html.findAll(text=True)).strip())

            # 清除非ASCII符号
            text = ''.join([i if ord(i) < 128 else ' ' for i in text])
            # dirty = text
            #
            # temptext = re.sub(r'[\0\200-\377]', '', dirty)



            text=text.replace('you’re', 'you are').replace('What’s ', 'What is').replace('it’s', 'It is').replace('It’s', 'It is')

            text=atabre.sub(' ',text)
            text = ablankre.sub(' ', text)

            file_w_allDoc.write(str(id)+'\t'+text)
            file_w_allDoc.write('\n')

            text = text.replace(' .', '. ')
            # split: '. ' then split '? '
            allsentences=text.split('. ')
            sentencecount=0
            # print(allsentences)

            for senidex, onesentence in enumerate(allsentences):
                onesentence=onesentence.replace(':',' ')
                onesentencelist = onesentence.split(' ')
                onesentencslen = len(onesentencelist)
                if onesentence.strip('.').strip() in "In this document":
                    continue

                if (onesentencslen < 3):
                    continue

                if '?' in onesentence:
                    newones = onesentence.split('?')
                    qlen = len(newones)
                    for qn, qsentencs in enumerate(newones):
                        qlist=qsentencs.split(' ')
                        qsentencslen=len(qlist)

                        if qsentencs.strip('.').strip() in "In this document":
                            continue

                        if (qsentencslen < 3):
                            continue
                        theline = (('%s_%s\t%s') % (str(id).strip(), str(sentencecount).strip(), qsentencs.strip()))
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
                        theline = (('%s_%s\t%s%s') % (str(id).strip(), str(sentencecount).strip(), onesentence.strip(), '.'))
                        # print(theline)
                        sentencecount += 1
                        file_w_allSent.write(theline)
                        file_w_allSent.write('\n')

    except:
        continue

fcsv.close()
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
