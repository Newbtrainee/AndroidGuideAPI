# import threading
# import time
# def haha(max_num):
#     for i in range(max_num):
#         time.sleep(1)
#         print(i)
#
#     recommand_list = []
#     print("processing ...")
#     fulllen = len(all_warning_list) * len(all_Entities_list)
#
#     count = 1
#     for warning in all_warning_list:
#
#         wrelationid = warning[7]
#
#         for entity in all_Entities_list:
#             print("realtion No. :" + str(count) + " / " + str(fulllen))
#             count = count + 1
#
#             if c_e_s(entity[1].lower(), warning[3].lower()) and (c_e_s(entity[1].lower(), all_Relation_list[wrelationid][1].lower()) or c_e_s(entity[1].lower(),all_Relation_list[wrelationid][3].lower())):
#                 recommand_list.append((warning[0], entity[0], all_Relation_list[wrelationid][0]))
#
#     recommand_list = list(set(recommand_list))
# """
# 创建一个列表，用于存储要启动多线程的实例
# """
# threads=[]
# for x in range(3):
#     t=threading.Thread(target=haha,args=(5,))
#     #把多线程的实例追加入列表，要启动几个线程就追加几个实例
#     threads.append(t)
# for thr in threads:
#     #把列表中的实例遍历出来后，调用start()方法以线程启动运行
#     thr.start()
# for thr in threads:
#     """
#     isAlive()方法可以返回True或False，用来判断是否还有没有运行结束
#     的线程。如果有的话就让主线程等待线程结束之后最后再结束。
#     """
#     if thr.isAlive():
#         thr.join()
#
#
import multiprocessing
from multiprocessing import Pool
import os, time, random

from numpy import iterable


def long_time_task(name,p,list):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    mystring='Task %s runs %0.2f seconds.' % (name, (end - start))
    print(mystring)
    for x in p:
        list.append(str(x)+"task%s" % (name))

    return list



if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    multiprocessing.freeze_support()
    cpus = multiprocessing.cpu_count()
    pool=multiprocessing.Pool()
    # p = Pool(4)
    p=((11,12,13,14,15,16),(21,22,23,24,25,26), (31, 32, 33, 34, 35, 36),(41, 42, 43, 44, 45, 56))
    list = []
    results=[]
    for i in range(0,cpus):
        result=pool.apply_async(long_time_task, args=(i,p[i],list,),callback=list.append)
        results.append(result)
    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()

    for x in list:
        for y in x:
            print(y)

    print(cpus)
    for result in results:
        print(result)

    print('All subprocesses done.')


#
# def chunkIt(seq, num):
#     avg = len(seq) / float(num)
#     out = []
#     last = 0.0
#
#     while last < len(seq):
#         out.append(seq[int(last):int(last + avg)])
#         last += avg
#
#     return out
#
#
# mylist=((1,2,3,4,5),(11,22,33,44,55),(31,32,33,34,35))
#
# my=chunkIt(mylist,3)
# print(len(my))
# pt=my[2]
# for x in pt:
#     print(x)

# def task(pid):
#     # do something
#     return result
# def main():
#     multiprocessing.freeze_support()
#     pool = multiprocessing.Pool()
#     cpus = multiprocessing.cpu_count()
#     results = []
#     for i in xrange(0, cpus):
#         result = pool.apply_async(task, args=(i,))
#         results.append(result)
#     pool.close()
#     pool.join()
#     for result in results:
#         print(result.get())

