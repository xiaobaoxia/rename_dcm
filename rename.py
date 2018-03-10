# coding=utf-8
import pydicom
import os
import shutil
import datetime
import sys


dir_index = 0
patient_num = 1


def run(dir_path):
    path = os.getcwd()
    global patient_num, dir_index

    # 遍历三个文件夹
    for dir_one in os.listdir(dir_path):
        # 遍历同一患者的文件夹
        for dir_two in os.listdir(dir_path+'/'+dir_one):
            # 除去隐藏文件夹
            if dir_two.startswith('.'):
                continue
            # 同一患者的信息只需提取一次, 设置标记
            flag = True
            # 遍历每个dcm文件

            for file_name in os.listdir(dir_path+'/'+dir_one+'/'+dir_two):
                ds = pydicom.read_file(os.path.join(path, dir_path+'/'+dir_one+'/'+dir_two+'/'+file_name))
                if flag:
                    flag = False
                    PatientSex = ds.PatientSex
                    PatientBirthDate = ds.PatientBirthDate
                    now = datetime.date.today()
                    birth = datetime.datetime.strptime(PatientBirthDate, '%Y%m%d').date()
                    PatientAge = str(((now - birth).days // 365))
                    if int(PatientAge) < 100:
                        PatientAge = '0' + PatientAge
                    # 判断该类型文件夹是否已经存在
                    if not os.path.exists(dir_path+'/'+dir_one+'/'+ds.SeriesDescription):
                        os.rename(dir_path+'/'+dir_one+'/'+dir_two, dir_path+'/'+dir_one+'/'+ds.SeriesDescription)
                        dir_two = ds.SeriesDescription

                # 判断文件类型是否有公共部分, 如果没有移动文件
                if ds.SeriesDescription not in dir_two:
                    # 判断文件类型是否存在, 如果不存在创建文件夹
                    if not os.path.exists(dir_path+'/'+dir_one+'/'+ds.SeriesDescription):
                        os.mkdir(dir_path+'/'+dir_one+'/'+ds.SeriesDescription)
                    shutil.move(dir_path+'/'+dir_one+'/'+dir_two+'/'+file_name, dir_path+'/'+dir_one+'/'+ds.SeriesDescription)

            try:
                os.rmdir(dir_path+'/'+dir_one+'/'+dir_two)
                print('删除空文件夹')
            except Exception as e:
                pass

            dir_index += 1
            print('已完成%d个患者的%d个文件夹' % (patient_num, dir_index))
            print('-'*30)

        os.rename(dir_path+'/'+dir_one, dir_path+'/'+PatientAge+'Y'+PatientSex+PatientBirthDate)

        print('已完成%d个患者信息' % patient_num)
        patient_num += 1
        dir_index = 0
        print('-'*30)

    print('任务结束')

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Please enter the correct parameters like: python rename "文件夹名称"')
    else:
        run(sys.argv[1])
