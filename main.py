import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import prettytable as pt
import time
import os
from compress import *
from math import *
import pdb

#get the original time series
ts = pd.read_csv('data.csv')
original_series = list(ts['power (W)'])

#write the original series to a file and get the size
f = open('original_series.txt', 'w')
for item in original_series:
    f.write(str(item))
    f.write('\n')
f.close()
original_size = os.path.getsize('original_series.txt')

#set tolerance
tolerances = [0.3]

#performance lists
compression_time = dict()
compression_ratio = dict()
rmse = dict()

#set file paths
filepath1 = './files/compressed_tolerance_'
filepath2 = './files/decompressed_tolerance_'

#decompressed lists
decom_lists = []

#compress for all tolerance
for tolerance in tolerances:
    #compress and write the result list to file 
    start = time.time()
    compressed_list = compress(original_series, tolerance)
    write_to_file(compressed_list, filepath1 + str(tolerance) + '.txt')
    end = time.time()
    compression_time[tolerance] = end - start

    #calculate compression ratio
    compressed_size = os.path.getsize(filepath1 + str(tolerance) + '.txt')
    compression_ratio[tolerance] = compressed_size / original_size

    #decompress
    decompressed_list = decompress(filepath1 + str(tolerance) + '.txt')
    decom_lists.append(decompressed_list)
    #save the decompressed list in file
    f = open(filepath2 + str(tolerance) + '.txt', 'w')
    for item in decompressed_list:
        f.write(str(item))
        f.write('\n')
    #calculate rmse
    s = 0
    for i in range(len(decompressed_list)):
        d = abs(float(decompressed_list[i]) - float(original_series[i]))
        s += d * d
    std = sqrt(s / len(decompressed_list))
    std /= (max(original_series) - min(original_series))
    rmse[tolerance] = std

#print the results in prettytable
tb = pt.PrettyTable()
tb.field_names = ['tolerance', 'compression time', 'compression ratio', 'RMSE']
for i in tolerances:
    tb.add_row([i, compression_time[i], compression_ratio[i], rmse[i]])
print(tb)

#plot time series
x = list(range(len(original_series)))
plt.subplot(len(decom_lists) + 1, 1, 1)
plt.plot(x, original_series)
plt.title('original series')
index = 2
for l in decom_lists:
    plt.subplot(len(decom_lists) + 1, 1, index)
    plt.plot(x, l)
    plt.title('tolerance = ' + str(tolerances[index - 2]))
    plt.tight_layout()
    index += 1
plt.show()
