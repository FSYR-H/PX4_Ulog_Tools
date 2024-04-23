from pyulog import ULog


# 加载 ULog 文件
ulog = ULog("log_136_2024-4-16-17-58-08.ulg")

# 获取参数
params = ulog.initial_parameters

# 打印所有参数
for param_name, param_value in params.items():
    if 'A20' in param_name:
        print(f"{param_name}: {param_value}")
