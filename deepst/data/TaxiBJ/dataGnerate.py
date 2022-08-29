import h5py
import pickle
import time
import datetime
import os
import numpy as np

year = 2013
month = 5
grid_size = 32
time_slot = 30
data_type = "InOut"

city = "New York"
raw_data_path = r"E:\project\work\NYC_data\raw_data\yellow_tripdata_%d-%02d.csv" % (year, month)
regions = {
    "New York": {
        "x": (-74, -73.9),
        "y": (40.7, 40.8)
    }
}


def nyc_inout(filename, month, grid_size, time_slot, data_type):
    day_sum = [31, 28, 31, 30, 31, 30]
    num_time_slots = (24 * 60) // time_slot
    data = np.zeros(shape=(sum(day_sum) * num_time_slots, 2, grid_size, grid_size))
    date = [("%d%02d%02d%02d" % (year, month + 1, day, time_index)).encode("utf8") for month, end_day in enumerate(day_sum) for day in range(1, end_day + 1) for
            time_index in
            range(1, num_time_slots + 1) ]
    print(date)

    def line_parse(line: str):
        data_list = line.strip().split(",")

        # 区域索引
        def gps2index(x, y):
            gap_x = (regions[city]["x"][1] - regions[city]["x"][0]) / grid_size
            gap_y = (regions[city]["y"][1] - regions[city]["y"][0]) / grid_size
            if regions[city]["x"][0] < x < regions[city]["x"][1] and regions[city]["y"][0] < y < regions[city]["y"][1]:
                index_x = int((x - regions[city]["x"][0]) / gap_x)
                index_y = int((y - regions[city]["y"][0]) / gap_y)
            else:
                return -1, -1
            return index_x, index_y

        out_index = gps2index(float(data_list[5]), float(data_list[6]))
        in_index = gps2index(float(data_list[9]), float(data_list[10]))

        # 时间索引
        def time2index(str_t):
            str_format = "%Y-%m-%d %H:%M:%S"
            t = datetime.datetime(*(time.strptime(str_t, str_format)[0:6]))
            # if t.day > end_day:
            #     return -1
            day = t.timetuple()[7]
            minutes = ((day - 1) * 24 + t.hour) * 60 + t.minute
            return minutes // time_slot

        out_time = time2index(data_list[1])
        in_time = time2index(data_list[2])
        return in_time, in_index, out_time, out_index

    with open(filename, "r", encoding="utf8") as f:
        f.readline()
        f.readline()
        content = f.readline()
        while content != "":
            try:
                in_time, in_index, out_time, out_index = line_parse(content)
                if in_index != (-1, -1) and in_time != -1:
                    data[in_time][0][in_index[0]][in_index[1]] += 1
                if out_index != (-1, -1) and out_time != -1:
                    data[out_time][1][out_index[0]][out_index[1]] += 1
                content = f.readline()
            except Exception as e:
                print(e)
                print(content)
                content = f.readline()

    if not os.path.exists("../dataset/nyc"):
        os.makedirs("../dataset/nyc")
    with open("Nyc%02d_M%dx%d_T%d_%s.pl" % (month, grid_size, grid_size, time_slot, data_type), "wb") as f:
        pickle.dump(data, f)
    f = h5py.File("Nyc%02d_M%dx%d_T%d_%s.h5" % (month, grid_size, grid_size, time_slot, data_type))
    f.create_dataset("data", data=data)
    f.create_dataset("date", data=date)
    f.close()


if __name__ == '__main__':
    # r"E:\project\work\NYC_data\raw_data\02\1.csv"
    nyc_inout("/export/data/wangze/NYC/yellow_tripdata_2015-06.csv", 5, 10, 20, data_type)
