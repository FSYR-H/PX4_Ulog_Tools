import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 假设你已经有了一个fig对象
fig1 = plotter.plot()

# 创建一个2x2的GridSpec对象
gs = gridspec.GridSpec(2, 2, figure=fig1)

# 将fig1转化为4个子图
ax1 = fig1.add_subplot(gs[0, 0])
ax2 = fig2.add_subplot(gs[0, 1])


# 现在你可以在这四个子图上进行绘图
ax1.plot([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
ax2.scatter([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
ax3.bar([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
ax4.pie([0.1, 0.2, 0.3