import csv  




if __name__ == '__main__':
    header = ['日志名称', '尾推前飞角度设定','尾推P值','尾推油门最大限定值','尾推油门最小限定值','尾推油门值', '悬停油门值', '平均水平前飞速度','最大前飞速度','单位里程消耗（mah/km）']
    data = [1, 1, 'English12', 100,2031]
    for i in range(3):
        with open('score.csv', 'w', encoding='gbk', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            # write the data
            writer.writerow(data)
        