# operate mysql database

import pymysql


def insert_waring_data(warning_list):

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='AndroidGuideAPI')
    cur = conn.cursor()

    # try:
    cur.execute("delete from Warning")

    sqli = "insert into Warning values(%s,%s,%s,%s,%s,%s,%s,%s)"


    for i, one_schema in enumerate(warning_list):
        cur.execute(sqli, (i + 1, one_schema[0], one_schema[1], one_schema[2], one_schema[3], one_schema[4], one_schema[5],one_schema[6]))
        # except:


    # print("Error: unable write data to table")


    cur.close()
    conn.commit()
    conn.close()
    return
    # =====================

def get_all_relation_data():
    all_relation_list = []
    conn = pymysql.connect(host='localhost', port=3306, user='root',passwd='root', db='AndroidGuideAPI')
    cur = conn.cursor()
    # try:
    cur.execute("select id, EntityOne, Relation, EntityTwo,  RelationSection, RelationURL, RelationText, URLid, Sentenceid, Relationid, POSinfo, SectionType from EntitiesRelation")
    results = cur.fetchall()

    for row in results:
        index = row[0]
        EntityOne = row[1]
        Relation = row[2]
        EntityTwo = row[3]
        RelationSection = row[4]
        RelationURL = row[5]
        RelationText = row[6]
        URLid = row[7]
        Sentenceid = row[8]
        Relationid = row[9]
        POSinfo=row[10]
        SectionType=row[11]

        all_relation_list.append((index, EntityOne, Relation, EntityTwo, RelationSection, RelationURL, RelationText, URLid,  Sentenceid, Relationid,POSinfo,SectionType))


# except:
#     print("Error: unable read data from table")

    cur.close()
    conn.close()

    return all_relation_list

    # =====================


def generate_warning_data(all_relation_list):
    warning_define_list = [ 'error', 'exception' , 'throw' , 'thrown' , 'warning:' , 'warning', 'warn' ,'note', 'note:', 'note that' , 'notification that', 'for more information' , 'consider', 'see also', 'if' , 'condition', 'whether', 'can', 'can not' , 'can\'t' , 'could' , 'could\'t' , 'could not' , 'must' , 'must not' , 'must\'t' , 'mustn\'t' , 'should' , 'should not' , 'shouldn\'t' , 'may' , 'may not' , 'might' , 'might not' , 'will' , 'will not' , 'would' , 'would not', 'wouldn\'t' ]
    # ====
    #



    warningList = []
    # relation:  0index, 1EntityOne, 2Relation, 3EntityTwo, 4Section, 5URL, 6RelationText, 7URLid, 8Sentenceid, 9Relationid

    # generate warning list

    for one_relation in all_relation_list:
        for warningword in warning_define_list:
            WarningType = ' '
            warningTag=' '

            if (c_e_s(warningword , one_relation[2].lower())) or (c_e_s(warningword , one_relation[6].lower())):

                compareString = one_relation[6].lower()  # warning text
                # ?????
                #  type:  error: Exception: Warning: Note : condition (if): other
                # can, will, excption(throw, thrown),must,note,should, be not,may
                if c_e_s('error' , compareString):
                    WarningType = 'Error'
                    warningTag='error'

                elif ('exception' in compareString):
                    WarningType = 'Exception'
                    warningTag = 'exception'
                elif c_e_s('exception', compareString):
                    WarningType = 'Exception'
                    warningTag = 'exception'
                elif c_e_s('throw', compareString):
                    WarningType = 'Exception'
                    warningTag = 'throw'
                elif c_e_s('throws', compareString):
                    WarningType = 'Exception'
                    warningTag = 'throws'
                elif c_e_s('thrown', compareString):
                    WarningType = 'Exception'
                    warningTag = 'thrown'

                elif  c_e_s('warning:', compareString):
                    WarningType = 'Warning'
                    warningTag = 'warning:'
                elif c_e_s('warning', compareString):
                    WarningType = 'Warning'
                    warningTag = 'warning'
                elif c_e_s('warn', compareString):
                    WarningType = 'Warning'
                    warningTag = 'warn'


                elif c_e_s('note:', compareString):
                    WarningType = 'Note'
                    warningTag = 'note:'
                elif c_e_s('consider', compareString):
                    WarningType = 'Note'
                    warningTag = 'consider'
                elif c_e_s('note that', compareString):
                    WarningType = 'Note'
                    warningTag = 'note that'
                elif c_e_s('notification that', compareString):
                    WarningType = 'Note'
                    warningTag = 'notification that'
                elif c_e_s('for more information', compareString):
                    WarningType = 'Note'
                    warningTag = 'for more information'
                elif c_e_s('see also', compareString):
                    WarningType = 'Note'
                    warningTag = 'see also'


                elif c_e_s('if', compareString):
                    WarningType = 'Condition'
                    warningTag = 'if'
                elif c_e_s('condition', compareString):
                    WarningType = 'Condition'
                    warningTag = 'condition'
                elif c_e_s('whether', compareString):
                    WarningType = 'Condition'
                    warningTag = 'whether'


                elif c_e_s('can', compareString):
                    WarningType = 'Can'
                    warningTag = 'can'
                elif c_e_s('can\'t', compareString):
                    WarningType = 'Can'
                    warningTag = 'can\'t'
                elif c_e_s('could', compareString):
                    WarningType = 'Can'
                    warningTag = 'could'
                elif c_e_s('could\'t', compareString):
                    WarningType = 'Can'
                    warningTag = 'could\'t'
                elif c_e_s('can not', compareString):
                    WarningType = 'Can'
                    warningTag = 'can not'
                elif c_e_s('could not', compareString):
                    WarningType = 'Can'
                    warningTag = 'could not'


                elif c_e_s('must', compareString):
                    WarningType = 'Must'
                    warningTag = 'must'
                elif c_e_s('must\'t', compareString):
                    WarningType = 'Must'
                    warningTag = 'must\'t'
                elif c_e_s('mustn\'t', compareString):
                    WarningType = 'Must'
                    warningTag = 'mustn\'t'
                elif c_e_s('must not', compareString):
                    WarningType = 'Must'
                    warningTag = 'must not'


                elif c_e_s('should', compareString):
                    WarningType = 'Should'
                    warningTag = 'should'
                elif c_e_s('shouldn\'t', compareString):
                    WarningType = 'Should'
                    warningTag = 'shouldn\'t'
                elif c_e_s('should not', compareString):
                    WarningType = 'Should'
                    warningTag = 'should not'


                elif c_e_s('may', compareString):
                    WarningType = 'May'
                    warningTag = 'may'
                elif c_e_s('might', compareString):
                    WarningType = 'May'
                    warningTag = 'might'
                elif c_e_s('may not', compareString):
                    WarningType = 'May'
                    warningTag = 'may not'
                elif c_e_s('might not', compareString):
                    WarningType = 'May'
                    warningTag = 'might not'


                elif c_e_s('will', compareString):
                    WarningType = 'Will'
                    warningTag = 'will'
                elif c_e_s('would', compareString):
                    WarningType = 'Will'
                    warningTag = 'would'
                elif c_e_s('wouldn\'t', compareString):
                    WarningType = 'Will'
                    warningTag = 'wouldn\'t'
                elif c_e_s('will not', compareString):
                    WarningType = 'Will'
                    warningTag = 'will not'
                elif c_e_s('would not', compareString):
                    WarningType = 'Will'
                    warningTag = 'would not'

                else:
                    WarningType = 'Other'
                    warningTag = 'other'

                # AndroidGuideAPI.Warning:  index, WarningTag,WarningSection,WarningText,WarningType,WarningURL
                warningList.append((warningTag, one_relation[4], one_relation[6], WarningType, one_relation[5],one_relation[8],one_relation[9]))
                break

    warningList=list(set(warningList))
    return warningList


#compare_exact_string
def c_e_s(checkword, checkString):
    str1list=checkword.split()
    str2list=checkString.split()
    flag=True
    for word in str1list:
        if word not in str2list :
            flag=False
            break
    return flag


# running
def main():
    all_relation_list=get_all_relation_data()
    warning_list=generate_warning_data(all_relation_list)
    insert_waring_data(warning_list)
    return

main()