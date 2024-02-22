import subprocess
import os

# 指定你要打包的 Python 文件的路径
python_file_path = 'test.py'

# 构造 pyinstaller 命令
command = f'pyinstaller --onefile --clean --icon=123123.ico --noconsole --name PX4_tools {python_file_path}'

# 使用 subprocess 运行命令
subprocess.run(command, shell=True)
