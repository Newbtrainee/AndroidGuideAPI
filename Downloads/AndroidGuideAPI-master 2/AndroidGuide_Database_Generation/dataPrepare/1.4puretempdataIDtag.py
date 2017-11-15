import os

import re

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


data_path=os.pardir+"/tempdata"

fmytag=open(data_path+'/androidAPI_id_tag.csv','r',encoding='utf-8')
fpuremytag=open(data_path+'/fixing_id_tag.csv','w',encoding='utf-8')
# foriginmytag=open(data_path+'/androidAPI_orginal_id_tag.csv','w',encoding='utf-8')

#对于tag考虑长度限制  目前限制48
taglength=100

mytaglist=[]

a1re = re.compile(r'\(.*?\)')
a2re = re.compile(r'\{.*?\}')

a4re = re.compile(r'\n+')
a5re = re.compile(r'\s+')
a6re = re.compile(r'\.+')
a7re = re.compile(r'^\.*?\.$')
a8re=re.compile(r'\t+')

onlyletterdigital = re.compile(r'[^a-zA-Z0-9_\-\s\.\\:$]')
onlyletterstart=re.compile(r'^(\d+(\.|\s)?)+')


for mi, line in enumerate(fmytag) :
    line=a4re.sub(' ', line)
    line=a8re.sub(' ',line)
    line=a5re.sub(' ', line)

    thisline=str(re.split(',',line)[1]).strip()





    if ('https://'  not in thisline) :
        if ('http://' not in thisline):
            thisline = thisline.replace('/', ' ')
            thisline = thisline.replace(':', ' ')
            thisline = onlyletterstart.sub('', thisline).strip()
            thisline = onlyletterdigital.sub('', thisline).strip()


    print(thisline)
    thisline = thisline.replace('\'', ' ')


    thisline = a4re.sub(' ', thisline)
    thisline = a6re.sub('.', thisline)
    thisline = a1re.sub('', thisline)
    thisline = a2re.sub('', thisline)

    thisline = a5re.sub(' ', thisline)


    thisline = thisline.strip()
    thisline=thisline.strip('.')
    thisline=thisline.strip('?')
    thisline=thisline.strip()




    # mythisline=''.join([c if (c.isalnum() or (c is '_') or (c is ' ') or (c is '.')) else '' for c in thisline ])
    # print(mythisline)



    thisline = thisline.strip()
    words = []
    if (len(thisline) < taglength) and (len(thisline) > 2):
        firstlevels = re.split(' ', thisline)
        for fstr in firstlevels:
            # fstr = onlyletterstart.sub('', fstr.strip())

            secondlevel = re.split('_', fstr.strip('.'))

            for sstr in secondlevel:
                # keep camel case form!!!!
                # strlist=camel_case_split(str(sstr))
                # for x in strlist:
                #     words.append(str(x))
                if sstr is not "":
                    words.append(sstr)
        thisline = "-".join(words)

        print(thisline)
        mytaglist.append(thisline)

fmytag.close()

#tag清除重复
mytaglist=list(set(mytaglist))

tagid=1

for srings in mytaglist:
    print("tagid:" + str(tagid))
    tagkeywords = str(tagid) + "," + srings
    fpuremytag.write(tagkeywords.strip())
    fpuremytag.write('\r')
    tagid += 1

fpuremytag.close()





