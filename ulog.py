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
        for topic in topics:
            print(topic.name)
        if topics:
            print('all topic get')
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

def plot_ATT(ATT):
    fig, axs = plt.subplots(3, 1, figsize=(10,10), sharex=True)
    axs[0].plot(ATT[0])
    axs[0].set_title('Roll')
    axs[1].plot(ATT[1])
    axs[1].set_title('Pitch')
    axs[2].plot(ATT[2])
    axs[2].set_title('Yaw')
    plt.tight_layout()
    plt.show()


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
    print(len(q_w))
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


def plot_everything(data_series,titles,labels_in=None,legends_in=None):
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
            # 对于第一个数据系列，我们在主Y轴上绘制
            p, = host.plot(series['timestamps'], series['data'], color=colors[i])
            host.spines['left'].set_color(colors[i])  # 设置 Y 轴颜色与线的颜色一样
            if labels and i < len(labels):  # 如果标签列表不为空且i没有超过标签的数量
                host.set_ylabel(labels[i])
            else:  # 如果标签列表为空或者i超过了标签的数量
                host.set_ylabel('Data series {}'.format(i+1))
        else:
            # 对于其他的数据系列，我们创建一个新的Y轴并绘制
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
    if legends:
        host.legend(lines, legends)
    mplcursors.cursor(hover=True)

    # 显示图形
    plt.show()

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
        for topic in topics:
            print(topic.name)
        if topics:
            print('all topic get')
            return log, topics
        else:
            print('no topic')


class ulog_data_ploter:
    def __init__(self, times_list, datas_list, labels, title, legends):
        self.times_list = times_list
        self.datas_list = datas_list
        self.labels = labels
        self.title = title
        self.legends = legends

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
        plot_everything(data_series,self.title,self.labels,self.legends)

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
    time_skip = round((time_end - time_start)/1000000 , 2)
    P_count = round(P_avg * time_skip / 1000, 2) 


    # print('平均速度为: ' + str(V_avg) + 'W')
    print('平均功率为: ' + str(P_avg) + 'W')
    # print(f'最大功率为: {max_power}')
    print('功耗为：' + str(P_count) + 'kJ')

    print('飞行时间为: ' +str(time_skip)+'s')
    # 创建一个 Tkinter 对象，它是一个窗口
    root = tk.Tk()
    # 这行代码让窗口在打开文件对话框后就自动关闭
    root.withdraw()
    messagebox.showinfo("提示", f"起飞后的平均功率、功耗是：{P_avg} W,{P_count} kJ")

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
    print(vehicle_power)
    return Cur,timestamps 

def get_afterburad_ORANG(log):
    vehicle_mot2 = log.get_dataset('actuator_outputs',instance=1)
    print(vehicle_mot2)
    timestamps = vehicle_mot2.data['timestamp']
    pwm = np.array(vehicle_mot2.data['output[1]'])
    print(pwm)

    return pwm, timestamps

def get_afterburad_CUAV(log):
    vehicle_mot2 = log.get_dataset('actuator_outputs')
    print(vehicle_mot2)
    timestamps = vehicle_mot2.data['timestamp']
    pwm = np.array(vehicle_mot2.data['output[8]'])
    print(pwm)

    return pwm, timestamps


if __name__ == "__main__":
    log_addr = get_addr()
    log,topic = get_log(log_addr,True)

    ATT,time_ATT = get_ATT(log)

    Cur,Cur_t = get_curr(log)
    count_power_onsumption(log,100)

    after_bured,time_after = get_afterburad_CUAV(log)

    [roll,pitch,yaw] = ATT
    V_H , _ , time_V_H = get_velocity(log)

    # ch1 , time_ch1 = get_RC_pwm(log,1)

    BAT,time_bat = get_Power(log)



    # title = 'angle_speed_afterbupitch_V_rner_curr_alt'
    # datas_list =[pitch,V_H,Cur,after_bured]
    # times_list = [time_ATT,time_V_H,Cur_t,time_after]
    # labels = ['degree','m/s','A','unknow','us']
    # legends = ['pitch_angle','speed','curr','AB']   

    # plotter = ulog_data_ploter(times_list, datas_list, labels, title, legends)
    # plotter.plot()
    
    ###
    title = 'pitch_V_Afterburner'
    datas_list =[pitch,V_H,after_bured]
    times_list = [time_ATT,time_V_H,time_after]
    labels = ['degree','m/s','us']
    legends = ['pitch_angle','speed','AB']

    plotter = ulog_data_ploter(times_list, datas_list, labels, title, legends)
    plotter.plot()


    # ###
    # title = 'flight power with or without Afterburner & speed'
    # labels = ['W','us','m/s']
    # legends = ['flight power','ch12','speed']
    # times_list = [time_bat,time_ch12,time_V_H]
    # datas_list = [BAT[2],ch12,V_H]
    
    # plotter = ulog_data_ploter(times_list, datas_list, labels, title, legends)
    # plotter.plot()

