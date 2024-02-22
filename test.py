import pyulog
from scipy.spatial.transform import Rotation
import numpy as np
import math
import matplotlib.pyplot as plt
import mplcursors




#使用pyulog获取日志文件，并返回所有数据主题
def get_log(log_addr,topics=None):
    log = pyulog.ULog(log_addr)
    if topics==None:
        return log
    else:
        # 获取所有的数据主题
        topics = log.data_list
        # for t in topics:
        #     print(t.name)
        if topics:
            print('all topic get')
            return log,topics
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
    plt.figure()

    # 画出数据，使用timestamps作为x轴
    plt.plot(timestamps, v_Hor)

    # 设置标题和标签
    plt.title('Speed_m/s')
    plt.xlabel('Time')
    plt.ylabel('v_Hor')

    # 显示图像
    plt.show()
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

import matplotlib.pyplot as plt
import numpy as np

# 假设你的时间戳和数据是以下形式：

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
            ax.spines['right'].set_position(('axes', 1 + i*0.1))  # 将Y轴向右移动
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



if __name__ == "__main__":
    log_addr = 'log_61_2024-2-6-16-27-02.ulg'
    log,topic = get_log(log_addr,True)

    ATT,time_ATT = get_ATT(log)
    pitch = ATT[1]
    V_H , _ , time_V_H = get_velocity(log)
    ch2 , time_ch2 = get_RC_pwm(log,2)
    ch12 , time_ch12 = get_RC_pwm(log,12)
    data_series = [
        {'timestamps': time_ATT, 'data': pitch},
        {'timestamps': time_V_H, 'data': V_H},
        {'timestamps': time_ch12, 'data': ch12},
       
        # 添加更多的数据系列...
    ]
    labels = ['degree','m/s','us']
    legends = ['pitch_angle','speed','Afterburner']
    
    title = 'angle_speed_afterburner'
    plot_everything(data_series,title,labels,legends)


