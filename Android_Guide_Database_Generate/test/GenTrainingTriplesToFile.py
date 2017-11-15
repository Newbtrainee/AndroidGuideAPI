
#check file content at line
def collect_training_triple_file():

    filefilenameid = open('/Users/Grand/Downloads/HDSKG/tempdata/uni_filenamelist_training.csv')
    fileallSent= open('/Users/Grand/Downloads/HDSKG/tempdata/AndroidAPI_allSent_ascii.txt')
    fileallRelation = open('/Users/Grand/Downloads/HDSKG/tempdata/androidAPIallCand5.txt')

    fileunitrainingAllSent=open('/Users/Grand/Downloads/HDSKG/tempdata/uni_AndroidAPI_training_Sent_ascii.txt','w')
    fileunitrainingAllRelation=open('/Users/Grand/Downloads/HDSKG/tempdata/uni_AndroidAPI_training_Cand5_ascii.txt','w')



# filefilenameid
    filenameid_list = []

    for line in filefilenameid:
        data = line.split(',')
        filenameid_list.append(data[0])

    filefilenameid.close()


# fileallSent
    uni_training_allsentence = []

    for line in fileallSent:
        data = line.split('\t')
        key, value = data[0], data[1]
        fileid=key.split('_')[0]
        if fileid in filenameid_list:
            uni_training_allsentence.append(line)

    fileallSent.close()

#uni_training_allsentence
    for line in uni_training_allsentence:
        fileunitrainingAllSent.write(line)

    fileunitrainingAllSent.close()


# fileallRelation
    uni_training_Cand5=[]

    for j,one_triple in enumerate(fileallRelation):

        if type(one_triple) is str or type(one_triple) is bytes:
            #Python 3 renamed the unicode type to str, the old str type has been replaced by bytes
            one_triple = eval(one_triple.strip('\n'))
        # all triple example:
        # {'subject_ori': 'administrators', 'relation_ori': 'configure', 'object_ori': 'app', 'subject': 'administrators', 'relation': 'configure', 'object': 'app', 'subject_stand': 'administrator', 'relation_stand': 'configure', 'object_stand': 'app', 'start_index': 14, 'end_index': 21, 'originalSent_len': 27, 'pos': 'NNS VB NN', 'relationType': 'NonTaxo', 'rel_id': '11352_27_1'}

        entity_url_id = one_triple['rel_id']
        entity_url_id=entity_url_id.split('_')[0]
        if entity_url_id in filenameid_list:
            uni_training_Cand5.append(str(one_triple))

    fileallRelation.close()

# fileunitrainingAllRelation
    for line in uni_training_Cand5 :
        fileunitrainingAllRelation.write(line)
        fileunitrainingAllRelation.write('\n')


    fileunitrainingAllRelation.close()

    return


#running code :
collect_training_triple_file()