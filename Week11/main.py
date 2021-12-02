import os
import pickle
import time
from multiprocessing import Process, Queue

import jieba

jieba.setLogLevel(log_level=11)


def findfiles(rootdirpath, queue):
    for root, dirs, files in os.walk(rootdirpath):
        for file in files:
            queue.put(os.path.join(root, file))


def mapper(filepath, queue, filename):
    file = filepath
    while True:
        print(file, ' {}'.format(os.getpid()))
        with open(file, 'r', encoding='gb18030') as f:
            dic = {}
            ReadLine = f.readline()
            while ReadLine:
                if ReadLine[0:9] == "<content>":
                    words = jieba.lcut(ReadLine)
                    if len(words) == 1:
                        continue
                    else:
                        for word in words:
                            dic[word] = dic.get(word, 0) + 1
                else:
                    pass
                ReadLine = f.readline()
        index_1 = file.index("\\")
        index_2 = file.index(".")
        tmp_name = "BUAA_21/Week11/Temp/" + file[index_1+1:index_2] + ".json"
        pickle.dump(dic, open(tmp_name, 'wb'), protocol=3)
        queue.put([tmp_name, os.getpid()])

        try:
            file = filename.get(block=False)
        except:
            print("The process will be terminated.")
            break


def reducer(queue):
    total_dic = {}
    tmp_name = queue.get()

    if tmp_name is None:
        print("The dictionary queue is empty")
        return

    while tmp_name is not None:
        new_dic = pickle.load(open(tmp_name[0], 'rb'))
        os.remove(tmp_name[0])
        if new_dic is None:
            print("The dictionary is empty")
            return
        else:
            temp = {}
            for key in total_dic.keys() | new_dic.keys():
                temp[key] = sum(d.get(key, 0) for d in (new_dic, total_dic))
            total_dic = temp

            try:
                tmp_name = queue.get(block=False)
            except:
                print("\nThe dictionary queue is empty.\n")
                dic_name = "BUAA_21/Week11/Dic/dic.txt"
                total_dic = sorted(
                    total_dic.items(), key=lambda item: item[1], reverse=True)
                with open(dic_name, 'w', encoding='utf-8') as f:
                    f.write(str(total_dic))
                break


if __name__ == '__main__':

    start = time.time()

    filename = Queue()
    q = Queue()

    rootdirpath = "BUAA_21/Week11/Sample"

    findfiles(rootdirpath, filename)

    process_number = 6
    readfile_process_list = []

    for i in range(process_number):
        try:
            task = filename.get(block=False)
        except:
            break
        readfile_process = Process(target=mapper, args=(task, q, filename))
        readfile_process.daemon = True
        readfile_process_list.append(readfile_process)
    print("Len of the readfileprocess list is %d" % len(readfile_process_list))

    analysis_process = Process(target=reducer, args=(q,))
    analysis_process.daemon = True

    for file_process in readfile_process_list:
        file_process.start()
    for file_process in readfile_process_list:
        file_process.join()

    analysis_process.start()
    analysis_process.join()

    end = time.time()
    print("\n--------%d Process----------" % process_number)
    print('Running time: %.2f Seconds\n' % (end-start))
    print("\nmain\n")
