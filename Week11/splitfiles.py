import time

def splitfiles():
    sourceFile = open('BUAA_21/Week11/news/news.dat', 'r',
                      encoding='gb18030')  # 打开原始大文件
    targetDir = 'BUAA_21/Week11/Files'  # 设置小文件的保存目录
    smallFileSize = 282400  # 设置每个小文件中的记录条数
    tempList = []  # 临时列表，用于暂存小文件中的记录内容
    fileNum = 1  # 小文件序号
    readLine = sourceFile.readline()  # 先读一行

    while (readLine):  # 循环
        lineNum = 1
        while (lineNum <= smallFileSize):  # 控制每个小文件的记录条数不超过设定值
            tempList.append(readLine)  # 将当前行的读取结果保存到临时列表中
            readLine = sourceFile.readline()  # 再读下一行
            lineNum += 1  # 行号自增
            if not readLine:
                break  # 如果读到空，则说明大文件读完，退出内层循环
        tempFile = open('BUAA_21/Week11/Files/'+str(fileNum) +
                        '.txt', 'w', encoding='gb18030')  # 将读取到的30条记录保存到文件中
        tempFile.writelines(tempList)
        tempFile.close()
        tempList = []  # 清空临时列表
        print('BUAA_21/Week11/Files/'+str(fileNum) +
              '.txt  创建于 '+str(time.asctime()))
        fileNum += 1  # 文件序号自增
    sourceFile.close()


if __name__ == '__main__':
    splitfiles()
