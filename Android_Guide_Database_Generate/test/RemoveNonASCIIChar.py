#remove non ascii char
def remove_file_non_ascii_and_line_break_char_with_new_id():
    fileSent=open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out.txt')
    fileNewSent=open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out_ascii.txt','w')
    j=1
    for i,oneSent in enumerate(fileSent) :

        oneSent=''.join([i if (ord(i) < 128) and (i is not '\n') else ' ' for i in oneSent])
        eachSent = oneSent.split('\t')
        id=str(j)
        oneSent=id+'\t'+''.join(eachSent[1:])

        fileNewSent.write(oneSent)
        fileNewSent.write('\n')
        j=j+1

    fileSent.close()
    fileNewSent.close()
    return


def remove_file_non_ascii():
    fileSent = open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out.txt')
    fileNewSent = open('/Users/Grand/Downloads/HDSKG/tempdata/all_rel_section_out_ascii.txt', 'w')
    j=1
    for i,oneSent in enumerate(fileSent) :
        oneSent.replace('\\n',' ')

        oneSent=''.join([i if (ord(i) < 128) and (i is not '\n') else ' ' for i in oneSent])

        fileNewSent.write(oneSent)
        fileNewSent.write('\n')

    fileSent.close()
    fileNewSent.close()
    return



remove_file_non_ascii()