import pyulog
from scipy.spatial.transform import Rotation
import numpy as np
import math
import matplotlib.pyplot as plt
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
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

#使用pyulog获取日志文件，并返回所有数据主题
def get_log(log_addr, topics=None):
    if 'ulg' not in log_addr:
        return
    
    log = pyulog.ULog(log_addr)
    
    if topics is None:
        print('No Topic')
        return log
    else:
        # 获取所有的数据主题
        topics = log.data_list
        # renamed = False  # 初始化为False
        count = 0
        # for topic in topics:
        #     # print(topic.name)
        if topics:
            # print('all topic get')
            return log, topics
        else:
            print('no topic')


def Quat2Angle(q_x, q_y, q_z, q_w):
    q = np.array([q_x, q_y, q_z, q_w])
    rot = Rotation.from_quat(q.T)
    euler_angles = rot.as_euler('xyz', degrees=True)
    roll = euler_angles[0]
    pitch = euler_angles[1]
    yaw = euler_angles[2]
    ATT = [roll,pitch,yaw]
    return ATT

# def plot_ATT(ATT):
#     fig, axs = plt.subplots(3, 1, figsize=(10,10), sharex=True)
#     axs[0].plot(ATT[0])
#     axs[0].set_title('Roll')
#     axs[1].plot(ATT[1])
#     axs[1].set_title('Pitch')
#     axs[2].plot(ATT[2])
#     axs[2].set_title('Yaw')
#     plt.tight_layout()
#     plt.show()


def get_ATT(log):
    roll = []
    pitch =[]
    yaw = []
    # 获取 vehicle_attitude 主题
    vehicle_attitude = log.get_dataset('vehicle_attitude')
    timestamps = vehicle_attitude.data['timestamp']
    q_w = vehicle_attitude.data['q[0]']
    q_x = vehicle_attitude.data['q[1]']
    q_y = vehicle_attitude.data['q[2]']
    q_z = vehicle_attitude.data['q[3]']
    for i in range(len(q_w)):
        ATT_temp = Quat2Angle(q_x[i],q_y[i],q_z[i],q_w[i])
        roll.append(ATT_temp[0])
        pitch.append(ATT_temp[1])
        yaw.append(ATT_temp[2])
    # print(len(q_w))
    return [roll,pitch,yaw],timestamps

def get_set_point_ATT(log):
    roll = []
    pitch =[]
    yaw = []
    # 获取 vehicle_attitude 主题
    vehicle_attitude = log.get_dataset('vehicle_attitude_setpoint')
    timestamps = vehicle_attitude.data['timestamp']
    q_w = vehicle_attitude.data['q_d[0]']
    q_x = vehicle_attitude.data['q_d[1]']
    q_y = vehicle_attitude.data['q_d[2]']
    q_z = vehicle_attitude.data['q_d[3]']
    for i in range(len(q_w)):
        ATT_temp = Quat2Angle(q_x[i],q_y[i],q_z[i],q_w[i])
        roll.append(ATT_temp[0])
        pitch.append(ATT_temp[1])
        yaw.append(ATT_temp[2])
    # print(len(q_w))
    return [roll,pitch,yaw],timestamps


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
    return v_Hor, vz, timestamps

def get_RC_pwm(log,channel):
    
    if int(channel) > 18 or int(channel) < 0:
        print('通道输入超限')
        return 
    strs = 'values' + '[' + str(int(channel) - 1) + ']'
    rc_input_all = log.get_dataset('input_rc')
    rc_input_channel = rc_input_all.data[strs]
    timestamps = rc_input_all.data['timestamp']

    return rc_input_channel,timestamps


def plot_everything(data_series,titles,labels_in=None,legends_in=None,log=None):
    if labels_in != None:
        labels = labels_in
    else:
        labels = []
    if legends_in != None:
        legends = legends_in
    else:
        legends = []  
    fig, host = plt.subplots()
    fig.subplots_adjust(right=0.75)

    # 存储每个Y轴和对应的数据系列
    axes = [host]

    # 创建其他的Y轴并绘制数据
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']  # 颜色列表
    lines = []  # 创建一个空列表

    for i, series in enumerate(data_series):
        if i == 0:
            # 对于第一个数据系列，需要在主Y轴上绘制
            p, = host.plot(series['timestamps'], series['data'], color=colors[i])
            host.spines['left'].set_color(colors[i])  # 设置 Y 轴颜色与线的颜色一样
            if labels and i < len(labels):  # 如果标签列表不为空且i没有超过标签的数量
                host.set_ylabel(labels[i])
            else:  # 如果标签列表为空或者i超过了标签的数量
                host.set_ylabel('Data series {}'.format(i+1))
        else:
            # 对于其他的数据系列，需要创建一个新的Y轴并绘制
            ax = host.twinx()
            ax.spines['right'].set_position(('axes', 1 + i*0.05))  # 将Y轴向右移动
            ax.spines['right'].set_color(colors[i % len(colors)])  # 设置 Y 轴颜色与线的颜色一样
            p, = ax.plot(series['timestamps'], series['data'], color=colors[i % len(colors)])
            if labels and i < len(labels):  # 如果标签列表不为空且i没有超过标签的数量
                ax.set_ylabel(labels[i])
            else:  # 如果标签列表为空或者i超过了标签的数量
                ax.set_ylabel('Data series {}'.format(i+1))

        lines.append(p)
        plt.title(titles)
    # 设置图例
    add_mission(log)
    if legends:
        host.legend(lines, legends)
    mplcursors.cursor(hover=True)

    return fig



def get_addr():
    # 创建一个 Tkinter 对象，它是一个窗口
    root = tk.Tk()
    # 这行代码让窗口在打开文件对话框后就自动关闭
    root.withdraw()
    messagebox.showinfo("提示", "请选择一个 .ulg 文件")
    # 打开文件对话框，并获取用户选择的文件路径
    log_addr = filedialog.askopenfilename()
    # 接下来，你就可以使用这个文件路径了
    if log_addr:
        print('get')
    else:
        print("Don't get plz  try again")
        messagebox.showerror('错误!', '请选择正确文件!!')
        sys.exit()
        return
    return log_addr

def get_folder_address():
    # 创建一个 Tkinter 窗口，但立即隐藏它
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("提示", "请选择一个 .ulg 文件夹")
    # 打开一个文件夹选择对话框
    folder_addr = filedialog.askdirectory()

    # 检查是否选择了文件夹
    if folder_addr:
        print('已获取文件夹')
    else:
        messagebox.showerror('错误!', '请选择正确文件!!')
        sys.exit()
        return
    adr_lists = []
    # 检查文件夹是否存在
    if os.path.isdir(folder_addr):
        # 获取文件夹中的所有文件
        files = os.listdir(folder_addr)

        # 遍历文件并打印它们的地址
        count = 0
        for file in files:
            
            if '.ulg' in str(file):
                file_addr = os.path.normpath(os.path.join(folder_addr, file))
                adr_lists.append(file_addr)
                # print('文件地址：', file_addr)
            else:
                count = count + 1
    else:
        print("无效的文件夹地址")
        if count > 0:
            print('文件有残缺')
    # print(adr_lists)

    return adr_lists

def get_log(log_addr, topics=None):
    if 'ulg' not in log_addr:
        return
    log = pyulog.ULog(log_addr)
    
    if topics is None:
        print('No Topic')
        return log
    else:
        # 获取所有的数据主题
        topics = log.data_list
        # renamed = False  # 初始化为False
        count = 0
        # for topic in topics:
            # print(topic.name)
        if topics:
            # print('all topic get')
            return log, topics
        else:
            print('no topic')


class ulog_data_ploter:
    def __init__(self, times_list, datas_list, labels, title, legends,log):
        self.times_list = times_list
        self.datas_list = datas_list
        self.labels = labels
        self.title = title
        self.legends = legends
        self.log = log

    def check_data(self):
        if len(self.times_list) != len(self.datas_list):
            print('应该提供长度相等的两组数据')
            return False
        else:
            for t, d in zip(self.times_list, self.datas_list):
                if len(t) != len(d):
                    print(len(t),len(d))
                    print('这组数据长度不相等，请重新提供')
                    print(d)
                    return False
        return True
    
    def plot(self):
        if not self.check_data():
            return
        data_series = [{'timestamps': t, 'data': d} for t, d in zip(self.times_list, self.datas_list)]
        plot_everything(data_series,self.title,self.labels,self.legends,self.log)

def get_Power(log):
    vehicle_power = log.get_dataset('battery_status')
    timestamps = vehicle_power.data['timestamp']
    Vot = np.array(vehicle_power.data['voltage_v'])
    Cur = np.array(vehicle_power.data['current_a'])
    
    P = Vot * Cur
    BAT = [Vot,Cur,P]
    # print('......')
    # print(timestamps)
    return BAT,timestamps

def count_power_onsumption(log,pre_fly_power=None):
    vehicle_power = log.get_dataset('battery_status')
    timestamps = vehicle_power.data['timestamp']
    Vot = np.array(vehicle_power.data['voltage_v'])
    Cur = np.array(vehicle_power.data['current_a'])
    Vot_mean = np.median(Vot)
    Vot_max = np.max(Vot)
    Vot_min = np.min(Vot)
    if pre_fly_power == None:
        pre_fly_power = 5
    else:
        pre_fly_power = int(pre_fly_power)
    P = Vot * Cur
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

    print(f'平均电压为:{Vot_mean}')
    print(f'平均功率为:  {str(P_avg)} W')
    print(f'最大功率为: {max_power}W')
    print('消耗为：' + str(P_count) + 'mah')
    #BAT_INFO 消耗毫安值、最大电压、最小电压、平均电压、最大功率、平均功率
    bat_info = [P_count,Vot_max,Vot_min,Vot_mean,max_power,P_count]
    return bat_info
    

def get_alt(log):
    if log == None:
        return
    vehicle_att = log.get_dataset('vehicle_gps_position')
    timestamps = vehicle_att.data['timestamp']
    alt = np.array(vehicle_att.data['alt'])
    return alt,timestamps

def get_curr(log):
    if log == None:
        return
    vehicle_power = log.get_dataset('battery_status')
    timestamps = vehicle_power.data['timestamp']
    Cur = np.array(vehicle_power.data['current_a'])
    Cur = savgol_filter(Cur, 50, 5, mode= 'nearest')
    # print(vehicle_power)
    return Cur,timestamps 

def get_afterburad_ORANG(log):
    vehicle_mot2 = log.get_dataset('actuator_outputs',instance=1)
    print(vehicle_mot2)
    timestamps = vehicle_mot2.data['timestamp']
    pwm = np.array(vehicle_mot2.data['output[1]'])
    # print(pwm)

    return pwm, timestamps

def get_afterburad_CUAV(log):
    pwm_min = 1000
    pwm_max = 00
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
        
def analysis_flight_time(log):
    vehicle_mots = log.get_dataset('actuator_outputs')
    timestamps = vehicle_mots.data['timestamp']
    pwms = np.array(vehicle_mots.data['output[1]'])
    flag = analysis_flight_times(log)
    if flag == 0:
        flight_time = 0
    else:
        for i in range(len(pwms)):
            if int(pwms[i]) > 1000:
                time_start = timestamps[i]
                break
        time_end = 0
        for i in range(len(pwms)-1,1,-1):
            if int(pwms[i]) < 1100:
                time_end = timestamps[i]
                break
        if time_end == 0:
            time_end = timestamps[-1]
            # print(min(pwms))
        flight_time = round((time_end - time_start) / 1000000,2)
    return flight_time

def analysis_att_d(log,flag):
    ATT1,time_ATT = get_set_point_ATT(log)
    ATT2,time_ATT = get_ATT(log)
    rpy_d_z = [0,0,0]
    rpy_d_f = [0,0,0]
    if analysis_flight_times(log) != 0:
        r_d = []
        p_d = []
        y_d = [] 
        ATT_D = [r_d,p_d,y_d]
        
        arg = 150
        for j in range(3):
            for i in range(len(ATT1[j])):
                if ATT1[j][i] != 0:
                    temp = round(((ATT1[j][i] - ATT2[j][i]) / ATT1[j][i] * 100),2)
                else:
                    temp = round((ATT1[j][i] - ATT2[j][i]) * 100,2)
                if temp > arg and temp > 0:
                    rpy_d_z[j] += 1
                elif abs(temp) > arg and temp < 0:
                    rpy_d_f[j] += 1

        for i in range(3):
            rpy_d_z[i] = round((rpy_d_z[i]/len(ATT1[0])*100),2)
            rpy_d_f[i] = round((rpy_d_f[i]/len(ATT1[0])*100),2)
    if flag == True:
        rpy_d = rpy_d_z
    else:
        rpy_d = rpy_d_f
    return rpy_d

def analysis_flight_times(log):
    v_h ,_ ,_ = get_velocity(log)
    if max(v_h) > 2:
        flag = 1
    else:
        flag = 0
    return flag

def analysis_flight_roads(log):
    roads = 0
    if analysis_flight_times(log) == 1:
        v_hor,_,_ = get_velocity(log)
        median_v_Hor = np.median(v_hor)
        time = analysis_flight_time(log)
        roads = median_v_Hor * time / 1000
    return round(roads,2)


def analysis_flight_hold_thr(log):
    if analysis_flight_times(log) == 1:
        thr, _= get_hold_thr(log)
        avg_thr = np.median(thr)
        return avg_thr

def add_mission(log,analysis=None):
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
        print('mission标志检测失败')
        return 

    if analysis == None:
        for i in range(0,len(index_flag),2):
            plt.axvspan(index_flag[i], index_flag[i+1], facecolor='g', alpha=0.2)
    return index_flag




if __name__ == "__main__":
    folder_addr_list = get_folder_address()
    flight_times = 0
    flight_time = 0
    overshot_r = []
    overshot_p = []
    overshot_y = []
    p_c = []
    road = 0
    avg_thr = []
    for log_addr in  folder_addr_list:
        log,topic = get_log(log_addr,True)

        flight_time += analysis_flight_time(log) 
        print(f'单次飞行时间为:{analysis_flight_time(log)}s')

        flight_times += analysis_flight_times(log)
        road_temp = analysis_flight_roads(log)
        print(f'里程为: {road_temp}Km')
        road += road_temp

        avg_thr.append(analysis_flight_hold_thr(log))

        #仅计算超过2km的单位消耗
        if road_temp > 2:
            cost = count_power_onsumption(log)
            runed = road_temp
            temp = round(cost[0]/runed,2)
            p_c.append(temp)


    print(f'有效飞行时间: {round(flight_time/60)}min')
    print(f'有效飞行架次: {flight_times} 次')
    print(f'有效累计里程: {road}km')
    print(f'平均单位里程消耗: {np.median(p_c)} mah/km',)





  
