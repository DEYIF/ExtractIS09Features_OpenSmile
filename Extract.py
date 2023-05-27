import os
import csv
import os
import csv
import numpy as np
import pandas as pd
# 设置配置文件
pathConfig = r"E:\opensmile-3.0-win-x64\config\is09-13\IS09_emotion.conf"
# 设置exe的路径：
pathExcuteFile = r"E:\opensmile-3.0-win-x64\bin\SMILExtract.exe"
# 设置wav的路径：
pathAudioRoot = r"E:\opensmile-3.0-win-x64\BerlinDB" # wav文件所在文件夹位置
# 过度文件夹 用于保存原始的csv特征
file_path = r"E:\opensmile-3.0-win-x64\BerlinDB_IS09\OriginalData"
#修改过的csv文件保存文件夹
modified_path=r"E:\opensmile-3.0-win-x64\BerlinDB_IS09"

def excuteCMD(excutefile,config,audio,output):#调用cmd运行OpenSmile工具包
    cmd=excutefile+" -C "+config+" -I "+audio+" -csvoutput "+output
    return cmd

def readLabel(wavLabel):#读取出音频文件的label标签
    if wavLabel == 'W':
        lab = 1
    elif wavLabel == 'T':
        lab = 2;
    elif wavLabel == 'A':
        lab = 3;
    elif wavLabel == 'F':
        lab = 4;
    elif wavLabel == 'E':
        lab = 5;
    elif wavLabel == 'N':
        lab = 6;
    elif wavLabel == 'L':
        lab = 7;
    return lab

def csvModify(namefront,Label,Subject,eachName):#将opensmile生成的csv文件修改成合适的格式，再加上label与subject
    with open(namefront) as df:
        df_csv=csv.reader(df)#打开原始数据csv文件
        header=next(df_csv) # 删除第一行（标题）
        l = []#将数据保存到list中进行操作
        for row in df_csv:
            l = row[0].split(';')[2:]  # 以‘;’进行分割，并去掉前两个元素 得到一条语音的特征
            #将label与subject编号转为list类型
            label=[Label]
            subject=[Subject]
            l=label+l+subject#将标签label与受试者编号subject与特征值合并为一列
            l=np.array(l)
            l=l.reshape(1, np.size(l, 0))#转置操作
    csvFile = pd.DataFrame(data=l)
    csvName=eachName + '.csv'
    csvFile.to_csv(csvName,header=None,index=None,encoding='utf-8')#生成csv文件

for wav in os.listdir(pathAudioRoot):#wav是带扩展.wav的文件名
    pathaudio=os.path.join(pathAudioRoot,wav)#pathaudio是.wav文件的路径
    Subject=int(wav[0:2])#Subject编号为音频文件前两位数字
    Label=readLabel(wav[5:6])#Label标签与最后的字母对应
    csv_filedir = os.path.join(file_path, wav[0:-4]) + '.csv'  # 保存csv特征文件的路径(原始数据)
    os.system(excuteCMD(pathExcuteFile,pathConfig,pathaudio,csv_filedir)) # 使用os.system运行OpenSmile
    Eachname='myIS09_lab'+str(Label)+'_sub'+str(Subject)+'_'+wav[3:5]+wav[2]+wav[5:7]#csv文件的文件名
    csvModify(csv_filedir,Label,Subject,Eachname)#修改原始数据
