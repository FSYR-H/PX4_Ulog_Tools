import subprocess
import os

# 指定你要打包的 Python 文件的路径
python_file_path = 'D:\\丰翼科技\\脚本\\git_px4\\PX4_Ulog_Tools\\ulogs_tools.py'

# 构造 pyinstaller 命令 无命令行
command = f'pyinstaller --onefile --clean --icon=D:\\丰翼科技\\脚本\\git_px4\\PX4_Ulog_Tools\\123123.ico --noconsole --name PX4_logs_tools {python_file_path}'

# command = f'pyinstaller --onefile --clean --icon=D:\\丰翼科技\\脚本\\git_px4\\PX4_Ulog_Tools\\123123.ico --name PX4_logs_tools {python_file_path}'

# 使用 subprocess 运行命令
subprocess.run(command, shell=True)

# import sys
# print(sys.version)