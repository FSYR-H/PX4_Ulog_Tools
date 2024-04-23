import pyulog
import rasterio.sample
from scipy.spatial.transform import Rotation
import numpy as np
import math
import mplcursors
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import time
from tkinter import filedialog, messagebox
import sys
import os
import geopandas as gpd
import contextily as cx
from scipy.signal import savgol_filter
from pyulog import ULog
import csv

def display_messagebox(): 
	tk.messagebox.showinfo(title='display_messagebox',
		message='This is a showinfo_messagebox')  

def get_addr():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("提示", "请选择一个 .ulg 文件")
    log_addr = filedialog.askopenfilename()
    if log_addr:
        print('get')
    else:
        print("Don't get plz  try again")
        messagebox.showerror('错误!', '请选择正确文件!!')
        sys.exit()
        return
    return log_addr

def get_folder_address():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("提示", "请选择一个 .ulg 文件夹")
    folder_addr = filedialog.askdirectory()
    if folder_addr:
        print('已获取文件夹地址：', folder_addr)
    else:
        messagebox.showerror('错误!', '请选择正确文件!!')
        sys.exit()
        return
    adr_lists = []

    if os.path.isdir(folder_addr):
        files = os.listdir(folder_addr)
        count = 0
        for file in files:
            
            if '.ulg' in str(file):
                file_addr = os.path.normpath(os.path.join(folder_addr, file))
                adr_lists.append(file_addr)

            else:
                count = count + 1
    else:
        print("无效的文件夹地址")
        if count > 0:
            print('文件有残缺')
    return adr_lists

def get_log(log_addr, topics=None):
    if 'ulg' not in log_addr:
        return
    log = pyulog.ULog(log_addr)
    
    if topics is None:
        print('No Topic')
        return log
    else:
        topics = log.data_list
        count = 0
        if topics:
            return log, topics
        else:
            print('no topic')

def add_mission(log):
    mission_num = 3
    Window = 5
    vehicle_mission = log.get_dataset('vehicle_status')
    mission_flag = vehicle_mission.data['nav_state']
    timestamps = vehicle_mission.data['timestamp']
    print(len(mission_flag),len(timestamps))
    index_flag = []
    show_range = []
    for index in range(len(mission_flag)):
        if mission_flag[index] == 3:
            print('mission_start')
            index_flag.append(timestamps[index])
            show_range.append(3)
            break
    #找到拐点
    index = 0
    while index < len(mission_flag)-Window:
        temp = Window
        for j in range(index,index+Window):
            dt = float(float((mission_flag[index+5] - mission_flag[index])) / float((timestamps[index+5] - timestamps[index])))
            if dt != 0 and (mission_flag[index] != mission_num and mission_flag[index+1] == mission_num) or (mission_flag[index] == mission_num and mission_flag[index+1] != mission_num):
                temp = temp - 1
                if temp == 0:
                    index_flag.append(timestamps[index+4])
                    show_range.append(mission_flag[index+4])
                    index += Window - 1  # 跳过接下来的4个点
                    break
        index += 1
    if len(index_flag) % 2 != 0:
        print('mission标志检测失败,正在删除第一个')
        del index_flag[0]
 

    
    #     plt.axvspan(index_flag[i], index_flag[i+1], facecolor='g', alpha=0.2)

    return index_flag


def get_curr(log):
    if log == None:
        return
    
    vehicle_power = log.get_dataset('battery_status')
    timestamps = vehicle_power.data['timestamp']
    
    Cur = np.array(vehicle_power.data['current_a'])
    Cur = savgol_filter(Cur, 50, 5, mode= 'nearest')
    #1830 -> 1386
    return Cur,timestamps 

def follw_index(index_flag,data,timestamps):

    new_timestamps = []
    new_data = []
    for i in range(0,len(index_flag),2):
        start = index_flag[i]
        end = index_flag[i+1]
        for count_a in range(len(timestamps)):
            if timestamps[count_a] > start:
                break
        for count_b in range(len(timestamps)-1,0,-1):
            if timestamps[count_b] < end:
                break
        new_timestamps.extend(timestamps[count_a:count_b+1])
        new_data.extend(data[count_a:count_b+1])
    # print(len(new_data),len(new_timestamps))
    return new_data,new_timestamps

def get_A20(log_addr):

    ulog = ULog(log_addr)
    # 获取参数
    params = ulog.initial_parameters
    # 打印所有参数
    A20=[]
    for param_name, param_value in params.items():
        if 'A20' in param_name:
            A20.append(round(param_value,2))
    return A20[1:]

def get_afterburad_CUAV(log):
    pwm_min = 1000
    pwm_max = 2000
    vehicle_mot2 = log.get_dataset('actuator_outputs')

    timestamps = vehicle_mot2.data['timestamp']
    pwms = np.array(vehicle_mot2.data['output[8]'])
    thr = []
    for pwm in pwms:
        thr.append(round((pwm - pwm_min) / (pwm_max - pwm_min) * 100 ,2))
    return thr, timestamps


def get_hold_thr(log):
    pwm_min = 1200
    pwm_max = 2000
    vehicle_mots = log.get_dataset('actuator_outputs')
    timestamps = vehicle_mots.data['timestamp']
    pwm = []
    for num_mot in range(8):
        str = f'output[{num_mot}]'
        pwm_test = np.array(vehicle_mots.data[str])
        pwm.append(np.array(vehicle_mots.data[str]))
    if len(pwm[0])*8 != int(len(pwm_test)*8):
        print("电机数据不完整")
        return -1
    else:
        for i in range(len(pwm)):
            for j in range(len(pwm[i])):
                # print('原始数据',pwm[i][j])
                pwm[i][j] = round((pwm[i][j] - pwm_min) / (pwm_max - pwm_min) * 100 ,2 )
                # print('等效数据',pwm[i][j])
        thr = []
        for i in range(len(pwm_test)):
            sum = 0
            
            for j in range(8):
                # print('#########')
                # print(pwm[j][i])
                sum = sum + pwm[j][i]
            avg = round(sum/8 , 2)
            # print('#########',avg)
            thr.append(avg)
        
    return thr , timestamps

def get_velocity(log):
    # 获取 vehicle_local_position 主题
    vehicle_local_position = log.get_dataset('vehicle_local_position')
    timestamps = vehicle_local_position.data['timestamp']
    vx = vehicle_local_position.data['vx']
    vy = vehicle_local_position.data['vy']
    vz = vehicle_local_position.data['vz']

    # 计算水平和垂直速度
    v_Hor = np.sqrt(vx**2 + vy**2)
    # v_Ver = ... # 如果需要计算垂直速度，可以在这里添加计算
    return v_Hor, timestamps

def count_power_onsumption_index(log,index,pre_fly_power=None):
    vehicle_power = log.get_dataset('battery_status')
    timestamps = vehicle_power.data['timestamp']
    Vot = np.array(vehicle_power.data['voltage_v'])
    Cur = np.array(vehicle_power.data['current_a'])

    Vot,timestamps = follw_index(index,Vot,timestamps)
    Cur,timestamps = follw_index(index,Cur,timestamps)

    Vot_mean = np.median(Vot)
    Vot_max = np.max(Vot)
    Vot_min = np.min(Vot)
    if pre_fly_power == None:
        pre_fly_power = 5
    else:
        pre_fly_power = int(pre_fly_power)
    P = np.array(Vot) * np.array(Cur)
    # 计算平均功率
    sum = 0 
    for p in P:
        if p > pre_fly_power:
            sum = sum + p
    P_avg = round(sum / len(P),2)

    for i in range(len(P)):
        if P[i] > pre_fly_power:
            time_start = timestamps[i]
            break
    for i in range(len(P)-1,1,-1):
        if P[i] > pre_fly_power:
            time_end = timestamps[i]
            break
            
    max_power = max(P)
    time_skip = round((time_end - time_start)/1000000/60/60 , 5) # 小时

    P_count = round(P_avg * time_skip * 1000 / Vot_mean , 2) 

    # print(f'平均电压为:{Vot_mean}')
    # print(f'平均功率为:  {str(P_avg)} W')
    # print(f'最大功率为: {max_power}W')
    # print('消耗为：' + str(P_count) + 'mah')

    #BAT_INFO 消耗毫安值、最大电压、最小电压、平均电压、最大功率、平均功率
    bat_info = [P_count,Vot_max,Vot_min,Vot_mean,max_power,P_count]
    return bat_info

if __name__ == '__main__':
    
    header = ['日志名称', '尾推前飞角度设定','尾推P值','尾推油门最大限定值','尾推油门最小限定值','巡航阶段尾推油门值', '巡航阶段多旋翼油门开度', '平均水平前飞速度','最大前飞速度','单位里程消耗（mah/km）']
    with open('test.csv', 'a', encoding='gbk', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
    line_str = []
    log_list = get_folder_address()

    for log_addr in log_list:
        log,topic = get_log(log_addr,True)

        index = add_mission(log)
        #平均前飞速度
        v_hor, time = get_velocity(log)
        v_hor, time_v = follw_index(index,v_hor,time)
        v_hor_avg = np.median(v_hor)


        #最大前飞速度
        try:
            v_hor_max = np.max(v_hor)
        except:
            print('vor空数组')
            continue
        ##跳过飞行速度不超2的

        if v_hor_avg < 1:
            continue
        #日志名称

        log_name = log_addr.split('\\')[-1]
        print(log_name)
        #获取巡航阶段时间戳标记
        
        curr,time = get_curr(log)
        curr,time = follw_index(index,time,curr)

        #A20参数 * 4
        A20 = get_A20(log_addr) #列表前4个
    

        #平均尾推油门
        thr, time = get_afterburad_CUAV(log)
        thr, time_thr = follw_index(index,thr,time)
        thr_avg = np.median(thr)


       #飞行中多旋翼电机开度
        thr_hold,time = get_hold_thr(log)
        thr_hold,time_thr_hold = follw_index(index,thr_hold,time)
        thr_hold_avg = np.median(thr_hold)


        ###单位里程消耗
        #消耗
        bat_info = count_power_onsumption_index(log,index)
        P_count = bat_info[0]
        
        #飞行时间:单位
        sum_time = 0
        us_to_s = 1000000
        for i in range(0,len(index),2):
            time = (index[i+1] - index[i]) / us_to_s
            sum_time = sum_time + time
        time_s = sum_time
        time_min = round(sum_time/60,2)
       
        #里程
        mileage_km = round(time_s * v_hor_avg/1000,2)
        

        ####单位里程能耗
        uec = round(P_count / mileage_km,2) 

        line_str=[log_name, A20[0], A20[1], A20[2], A20[3], thr_avg, thr_hold_avg, v_hor_avg, v_hor_max, uec, '\r']
        with open('test.csv', 'a', encoding='gbk', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(line_str)
    
    messagebox.showinfo('分析完成', '点击退出')

    sys.exit()
